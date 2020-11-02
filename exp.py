#!/usr/bin/python3

import requests
import json
import dns.resolver
import tldextract

results = []
with open("blocked.txt") as infile, open("results.jsonl","w") as outfile:
    for row in infile:
        site = row.strip()
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
        results.append(data)

    for row in results:
        outfile.write(f"{json.dumps(row)}\n")