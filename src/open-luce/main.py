import asyncio
import aioipfs

# === SERVER SIDE ===
async def run_server(client):
    # Listen on localhost TCP 9090, exposed via /x/helloworld
    await client.p2p.listen("/x/luce", "/ip4/127.0.0.1/tcp/9090")
    print("✅ P2P service running at /x/luce (port 9090)")

    # Simple TCP handler that replies with "Hello World"
    async def handle_client(reader, writer):
        request = await reader.read(100)
        print("📩 Server received:", request.decode().strip())
        writer.write(b"Hello World\n")
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(handle_client, "127.0.0.1", 9090)
    return server


# === CLIENT SIDE ===
async def run_client(client, peer_id):
    async with client.p2p.dial_service(peer_id, "/x/helloworld") as ctx:
        print(f"🔗 Client connected to {ctx.maddr_host}:{ctx.maddr_port}")

        # Open TCP connection to proxied service
        reader, writer = await asyncio.open_connection(ctx.maddr_host, ctx.maddr_port)
        writer.write(b"Ping\n")
        await writer.drain()

        response = await reader.read(100)
        print("✅ Client got response:", response.decode().strip())

        writer.close()
        await writer.wait_closed()


# === MAIN ENTRY ===
async def main():
    client = aioipfs.AsyncIPFS()  # Assumes `ipfs daemon` is already running

    # Show our Peer ID
    id_info = await client.id()
    peer_id = id_info["ID"]
    print(f"🆔 Local Peer ID: {peer_id}")

    # Start server
    server = await run_server(client)

    # Wait a moment to ensure server is listening
    await asyncio.sleep(2)

    # Client dials the same local peer (loopback test)
    await run_client(client, peer_id)

    # Keep server running until interrupted
    async with server:
        await server.serve_forever()

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())