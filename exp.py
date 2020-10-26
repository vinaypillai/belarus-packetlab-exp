#!/usr/bin/python3

import requests
import json
results = []
with open("blocked.txt") as infile, open("results.jsonl","w") as outfile:
    for row in infile:
        site = row.strip()
        data = {'site':site}
        try:
            r = requests.get(site)
            data['status'] = r.status_code;
            data['content'] = r.text
        except requests.exceptions.RequestException as err:
            data['error'] = str(err)
        results.append(data)

    for row in results:
        outfile.write(f"{json.dumps(row)}\n")