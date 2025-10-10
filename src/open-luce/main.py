import asyncio
import aioipfs

async def send_message_and_wait_for_receipt(client_location, recipient_peer_id):
    """
    Simulates a message send and receipt by making a direct RPC call
    to another peer. This works for RPC-exposed endpoints.
    For custom messaging, you would need a custom service.
    """
    async with aioipfs.AsyncIPFS(client_location) as c:
        # Step 1: Get our own Peer ID for the sake of the example
        my_id = (await c.id())['ID']
        print(f"I am peer: {my_id}")
        
        try:
            # Step 2: Directly "ask" the recipient node for its ID.
            # This RPC call is the "message" being sent. The response
            # from the recipient is the "receipt."
            print(f"Sending message (ID query) to peer: {recipient_peer_id}")
            
            # Note: This requires the recipient's RPC API to be publicly
            # accessible and discoverable.
            recipient_info = await c.id(peer=recipient_peer_id)
            
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
recipient_peer_id = 'Qm...'
client_location = '/ip4/127.0.0.1/tcp/5001'
asyncio.run(send_message_and_wait_for_receipt(client_location, recipient_peer_id))
