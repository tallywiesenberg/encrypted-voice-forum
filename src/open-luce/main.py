import aioipfs
import asyncio
from aioipfs import AsyncIPFS

async def main():
    async with AsyncIPFS() as ipfs:
        version = await ipfs.version()
        print("IPFS Version:", version)

        # Example: Send a message to a pubsub topic
        res = await ipfs.pubsub.pub("open_luce", b"Hello, luce!")
        print("Published message:", res)

if __name__ == "__main__":
    asyncio.run(main())