#!/usr/bin/python3

import asyncio
import httpx
import json
import dns.asyncresolver
import tldextract
import os
from sys import stderr, exc_info
import time

async def http_query(url):
    data = {}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data['status'] = response.status_code;
            data['content'] = response.content.decode('utf-8');
        except UnicodeDecodeError as err:
            data['content'] = response.content.decode('ISO-8859-1');
        except httpx.RequestError as err:
            print(url)
            print(err)
            data['error'] = str(err)
        except:
            print("UNCAUGHT HTTP ERROR",exc_info()[0])
    return data

async def dns_query(hostname):
    data = {}
    try:
        query = await dns.asyncresolver.resolve(hostname, 'A')
        response = query.response
        data['rcode'] = response.rcode()
        data['content'] = str(response)
    except dns.exception.DNSException as err:
        print(err)
        print("hostname")
        print(hostname)
        data['error'] = err.msg
    except:
        print("UNCAUGHT DNS ERROR",exc_info()[0])
    return data

async def main():
    timestamp = int(time.time())
    print("---", file=stderr)
    print("Starting experiment...", file=stderr)
    print(f"TIME:{timestamp}", file=stderr)
    print("---", file=stderr)
    outfile_name = f"results-{timestamp}.jsonl"
    file_count = 0
    while(os.path.exists(outfile_name)):
        file_count += 1
        outfile_name = f"results-{timestamp}_{file_count}.jsonl"

    with open("blocked.txt") as infile, open(outfile_name,"w") as outfile:
        os.chmod(outfile_name, 0o666)
        http_tasks = []
        dns_tasks = []
        sites = []
        for row in infile:
            site = row.strip()
            sites.append(site)
            print("---", file=stderr)
            print("Starting new site...", file=stderr)
            print(f"SITE:{site}", file=stderr)
            print("---", file=stderr)
            extracted_site = tldextract.extract(site)
            hostname = '.'.join([part for part in list(extracted_site) if len(part) > 0])
                
            # Perform http request to blocked url
            http_tasks.append(http_query(site))
            # Perform dns request to blocked url
            dns_tasks.append(dns_query(hostname))
        try:
            http_responses = await asyncio.gather(*http_tasks)
            dns_responses = await asyncio.gather(*dns_tasks)
        except asyncio.exceptions.InvalidStateError as err:
            print(err)

        for i, site in enumerate(sites):
            data = {'site':site, 'http':{}, 'dns':{}}
            data['http'].update(http_responses[i])
            data['dns'].update(dns_responses[i])
            outfile.write(json.dumps(data) + "\n")

        
    finish_timestamp = int(time.time())
    print("Finishing experiment...", file=stderr)
    print(f"TIME:{finish_timestamp}", file=stderr)
    print(f"DURATION:{finish_timestamp - timestamp}", file=stderr)
    print("---", file=stderr)

asyncio.run(main())
