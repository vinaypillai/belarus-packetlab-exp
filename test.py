import httpx
import dns.asyncresolver
import asyncio

print(1)
async def query_domain(domain, i):
    async with httpx.AsyncClient() as client:
        print(f"{i}b")
        r = await client.get(domain)
        print(f"{i}c")
        r = await client.get(domain)
        print(f"{i}d")
        r = await client.get(domain)
        print(f"{i}e")
        r = await client.get(domain)
        print(f"{i}f")
        return i

async def query_dns(hostname, i):
    print(f"{i}c")
    r = await dns.asyncresolver.resolve(hostname)
    print(i)
    print(r)
    return i

tasks = []
async def test():
    counter = 0
    for i in range(10):
        print(f"{i}a")
        # tasks.append(asyncio.create_task(query_domain('https://www.example.com/', i)))    
        tasks.append(query_dns('example.com', i))
    a = await asyncio.gather(*tasks)   
    print(tasks)   
    print(a)   
asyncio.run(test())
print(4)