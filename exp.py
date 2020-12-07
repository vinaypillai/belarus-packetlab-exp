#!/usr/bin/python3

import requests
import json
import dns.resolver
import tldextract
import os
from sys import stderr
import time

results = []
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
    for row in infile:
        site = row.strip()
        print("---", file=stderr)
        print("Starting new site...", file=stderr)
        print(f"SITE:{site}", file=stderr)
        print("---", file=stderr)
        data = {'site':site, 'http':{}, 'dns':{}}
        # Perform http request to blocked url
        try:
            r = requests.get(site)
            data['http']['status'] = r.status_code;
            data['http']['content'] = r.text
        except requests.exceptions.RequestException as err:
            data['http']['error'] = str(err)

        # Perform dns request to blocked url
        try:   
            extracted_site = tldextract.extract(site)
            hostname = '.'.join([part for part in list(extracted_site) if len(part) > 0])
            response = dns.resolver.resolve(hostname, 'A').response
            data['dns']['rcode'] = response.rcode()
            data['dns']['content'] = str(response)
        except dns.exception.DNSException as err:
            data['dns']['error'] = err.msg
        outfile.write(f"{json.dumps(data)}\n")
        outfile.flush()
        os.fsync(outfile)
finish_timestamp = int(time.time())
print("Finishing experiment...", file=stderr)
print(f"TIME:{finish_timestamp}", file=stderr)
print(f"DURATION:{finish_timestamp - timestamp}", file=stderr)
print("---", file=stderr)
