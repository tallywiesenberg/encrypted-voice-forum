import asyncio
from typing import Optional
import aioipfs

from open_luce.ipfs_node import IPFSNode

def multiaddr_to_url(addr: str, scheme: Optional[str] = None) -> tuple[str, int]:
    """Converts a multiaddr to a (host, port) tuple suitable for aioipfs.
    Assumes the multiaddr is in the form /ip4/<ip>/tcp/<port>.
    """
    # Example: "/ip4/127.0.0.1/tcp/5001"
    parts = addr.strip("/").split("/")
    # parts = ["ip4", "127.0.0.1", "tcp", "5001"]
    host = parts[1]
    port = int(parts[3])
    if scheme is None:
        return host, port
    return f"{scheme}://{host}", port


async def get_peer_id(client:aioipfs.AsyncIPFS) -> str:
    """
    Helper function to get the Peer ID of an IPFS node given its IPFS_PATH.
    """
    info = await client.id()
    return info['ID']

async def send_message_and_wait_for_receipt(client:IPFSNode, recipient_peer_id):
    """
    Simulates a message send and receipt by making a direct RPC call
    to another peer. This works for RPC-exposed endpoints.
    For custom messaging, you would need a custom service.
    """
    # Step 1: Get our own Peer ID for the sake of the example
    my_id = get_peer_id(client)
    print(f"I am peer: {my_id}")
    
    try:
        # Step 2: Directly "ask" the recipient node for its ID.
        # This RPC call is the "message" being sent. The response
        # from the recipient is the "receipt."
        print(f"Sending message (ID query) to peer: {recipient_peer_id}")
        
        # Note: This requires the recipient's RPC API to be publicly
        # accessible and discoverable.
        recipient_info = await client.id(peer=recipient_peer_id)
        
        # Step 3: Recipient sends a response back.
        recipient_id = recipient_info['ID']
        print(f"Received receipt from peer: {recipient_id}")
        
        if recipient_id == recipient_peer_id:
            print("Receipt verified. Message was successfully received.")
        else:
            print("Error: Received an ID that doesn't match.")
            
    except aioipfs.IPFSConnectionError as e:
        print(f"Error communicating with peer {recipient_peer_id}: {e}")
        print("The peer might be offline or unreachable.")
        
# You must replace this with the actual Peer ID of your other node
# Get this ID by running `ipfs id` on the other node.
if __name__ == "__main__":
    recipient_peer_id = 'Qm...'
    sender_client_location = '/ip4/127.0.0.1/tcp/5001'
    asyncio.run(send_message_and_wait_for_receipt(sender_client_location, recipient_peer_id))
