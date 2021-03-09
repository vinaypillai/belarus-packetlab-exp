import json
import dns
import tldextract
import os
from sys import stderr, exc_info
import time
import traceback
import sys
from multiprocessing.dummy import Pool
from dns import resolver, exception
import requests


def http_query(url):
    data = {}
    try:
        resp = requests.get(url, timeout=2)
        data["status"] = resp.status_code
        data["content"] = resp.text[:100] if len(resp.text) > 100 else resp.text
    except requests.exceptions.RequestException as err:
        print("HTTP exception request error: ", err)
        print("url: ", str(url))
        data["error"] = str(err)
        print(exc_info())
        traceback.print_exc(file=sys.stdout)
    # try:
    #     resp = httpx.get(url)
    #     data["status"] = resp.status_code
    #     data["content"] = resp.content.decode(resp.encoding)
    # except httpx.RequestError as err:
    #     print("HTTP exception request error: ", err)
    #     print("url: ", str(url))
    #     data["error"] = str(err)
    #     print(exc_info())
    #     traceback.print_exc(file=sys.stdout)
    except:
        print("UNCAUGHT HTTP ERROR", exc_info())
    return data


def dns_query(hostname):
    dns_resolver = dns.resolver.Resolver()
    data = {}
    try:
        resp = dns_resolver.resolve(hostname, "A").response
        data["rcode"] = resp.rcode()
        data["content"] = str(resp)
    except dns.exception.DNSException as err:
        print("DNS exception: ", err)
        print("hostname: ", hostname)
        data["error"] = err.msg
    except:
        print("UNCAUGHT DNS ERROR", exc_info())
    return data


def main():
    timestamp = int(time.time())
    print("---", file=stderr)
    print("Starting experiment...", file=stderr)
    print("TIME: {}".format(timestamp), file=stderr)
    print("---", file=stderr)
    outfile_name = "results-{}.jsonl".format(timestamp)
    file_count = 0
    while os.path.exists(outfile_name):
        file_count += 1
        outfile_name = f"results-{timestamp}_{file_count}.jsonl"

    http_sites = []
    dns_hostnames = []
    with open("blocked-test3.txt") as infile:
        for row in infile:
            site = row.strip()
            http_sites.append(site)
            extracted_site = tldextract.extract(site)
            hostname = ".".join(
                [part for part in list(extracted_site) if len(part) > 0]
            )
            dns_hostnames.append(hostname)

    http_resp = []
    dns_resp = []
    try:
        with Pool(10) as p:
            http_resp = p.map(http_query, http_sites)
            dns_resp = p.map(dns_query, dns_hostnames)
    except KeyboardInterrupt:
        pass

    with open(outfile_name, "w") as outfile:
        os.chmod(outfile_name, 0o666)
        for i, site in enumerate(http_sites):
            data = {"site": site, "http": {}, "dns": {}}
            data["http"].update(http_resp[i])
            data["dns"].update(dns_resp[i])
            outfile.write(json.dumps(data) + "\n")

    finish_timestamp = int(time.time())
    print("Finishing experiment...", file=stderr)
    print("TIME:{}".format(finish_timestamp), file=stderr)
    print("DURATION:{}".format(finish_timestamp - timestamp), file=stderr)
    print("---", file=stderr)


if __name__ == "__main__":
    main()
