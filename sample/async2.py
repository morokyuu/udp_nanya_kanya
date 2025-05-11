import asyncio
import random

async def send_command(cmd):
    print(f"send : {cmd}")
    await asyncio.sleep(random.choice([0.3,0.8,1.3]))
    print(f"recv : {cmd}_response")
    return f'{cmd}_response'

async def main():
    cmd = "CMD1"
    results = await asyncio.gather(send_command(cmd))
    for res in results:
        print(f'result: {res}')

asyncio.run(main())
