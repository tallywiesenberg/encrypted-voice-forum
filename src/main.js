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

main().catch(console.error);