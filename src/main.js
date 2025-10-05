import { createLightNode } from "@waku/sdk";

async function main() {
  // 1. Create a light node
  const node = await createLightNode({ defaultBootstrap: true });
  await node.start();
  console.log("✅ Waku node started");

  // 2. Wait for at least one peer that supports LightPush
  console.log("🔗 Connected to a LightPush peer");

  // 3. Define content topic and message
  const contentTopic = "/test/1/chat";
  const messageText = "Hello from my Waku node 👋";

  // 4. Send message
  const protoMessage = DataPacket.create({
    timestamp: Date.now(),
    sender: "Alice",
    message: messageText,
});

// Serialise the message using Protobuf
const serialisedMessage = DataPacket.encode(protoMessage).finish();

  if (result.isOk) {
    console.log("📨 Message sent successfully:", messageText);
  } else {
    console.error("❌ Failed to send message:", result.error);
  }

  // Keep node running or shut down
  // await node.stop();  // uncomment if you want to stop
}

// Send the message, and get the id to track events
const messageId = reliableChannel.send(payload);
        
reliableChannel.addEventListener("sending-message-irrecoverable-error", (event) => {
    if (messageId === event.detail.messageId) {
      console.error('Failed to send message:', event.detail.error);
      // Show an error to the user
    }
})

reliableChannel.addEventListener("message-sent", (event) => {
    if (messageId === event.detail) {
        // Message sent, show '✔' to the user, etc
    }
})

reliableChannel.addEventListener("message-acknowledged", (event) => {
  if (messageId === event.detail) {
    // Message acknowledged by other participants, show '✔✔' to the user, etc
  }
})

main().catch(console.error);