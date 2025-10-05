import { createLightNode } from "@waku/sdk";
import WebSocket from "isomorphic-ws";
import { EventTarget, Event } from "event-target-shim";
import { createEncoder, createDecoder } from "@waku/sdk";
import { HealthStatus } from "@waku/sdk";
// Polyfills for Node
global.WebSocket = WebSocket;
global.Event = Event;
global.CustomEvent = class CustomEvent extends Event {
  constructor(type, options = {}) {
    super(type, options);
    this.detail = options.detail;
  }
};
// Optional: Patch EventTarget globally if needed
global.EventTarget = EventTarget;

// Start Waku
const node = await createLightNode({ defaultBootstrap: true });
await node.start();

console.log("✅ Waku Light Node started and connected to peers.");

// Choose a content topic
const ct = "/open-luce/0.1.0/test/proto"


// Create a message encoder and decoder
const encoder = node.createEncoder({ contentTopic: ct });
const decoder = node.createDecoder({ contentTopic: ct });

node.events.addEventListener("waku:health", (event) => {
    const health = event.detail;
    
    if (health === HealthStatus.SufficientlyHealthy) {
        // Show to the user they are connected
        console.log("connected")
    } else if (status === HealthStatus.MinimallyHealthy) {
        // Maybe put some clue to the user that while we are connected,
        // there may be issues sending or receiving messages
        console.log("while we are connected, there may be issues sending or receiving messages")
    } else {
        // Show to the user they are disconnected from the network
        console.log("disconnected")
    }
});