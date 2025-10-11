import asyncio
import os
import subprocess
import tempfile
import time
import aioipfs
import pytest
import pytest_asyncio
import shutil
import json
from open_luce.ipfs_node import IPFSNode
from open_luce.main import get_peer_id, send_message_and_wait_for_receipt, multiaddr_to_url


async def wait_for_ready(host, port, retries=10, delay=1):
    import aioipfs
    client = aioipfs.AsyncIPFS(host=host, port=port)
    for _ in range(retries):
        try:
            await client.id()
            await client.close()
            return
        except Exception:
            await asyncio.sleep(delay)
    raise RuntimeError(f"IPFS API {host}:{port} did not start")

def init_ipfs_repo(path, api_port, swarm_port, gateway_port):
    os.environ["IPFS_PATH"] = path
    subprocess.run(["ipfs", "init"], check=True)

    # Load and patch config
    cfg_file = os.path.join(path, "config")
    with open(cfg_file) as f:
        cfg = json.load(f)

    cfg["Addresses"]["API"] = f"/ip4/127.0.0.1/tcp/{api_port}"
    cfg["Addresses"]["Swarm"] = [f"/ip4/0.0.0.0/tcp/{swarm_port}"]
    cfg["Addresses"]["Gateway"] = f"/ip4/127.0.0.1/tcp/{gateway_port}"

    with open(cfg_file, "w") as f:
        json.dump(cfg, f)

    return cfg
        
@pytest_asyncio.fixture(scope="session")
async def ipfs_nodes():
    tmp1 = tempfile.mkdtemp()
    tmp2 = tempfile.mkdtemp()

    cfg1 = init_ipfs_repo(tmp1, 5101, 4101, 8180)
    cfg2 = init_ipfs_repo(tmp2, 5102, 4102, 8181)

    d1 = subprocess.Popen(["ipfs", "daemon", "--enable-pubsub-experiment"], env={**os.environ, "IPFS_PATH": tmp1})
    d2 = subprocess.Popen(["ipfs", "daemon", "--enable-pubsub-experiment"], env={**os.environ, "IPFS_PATH": tmp2})

    await wait_for_ready("127.0.0.1", 5101)
    await wait_for_ready("127.0.0.1", 5102)

    sender = IPFSNode("sender", tmp1, "127.0.0.1", 5101, d1)
    receiver = IPFSNode("receiver", tmp2, "127.0.0.1", 5102, d2)

    yield sender, receiver

    d1.terminate(); d2.terminate()
    d1.wait(); d2.wait()
    shutil.rmtree(tmp1); shutil.rmtree(tmp2)

@pytest.mark.asyncio
async def test_message_sent(ipfs_nodes):
    sender, receiver = ipfs_nodes

    async with sender.client() as s, receiver.client() as r:
        sid = await s.id()
        rid = await r.id()
        print(f"{sender.name} -> {sid['ID']}")
        print(f"{receiver.name} -> {rid['ID']}")
        await send_message_and_wait_for_receipt(s, rid['ID'])

@pytest.mark.asyncio
async def test_ipfs_ping(ipfs_nodes):
    sender, receiver = ipfs_nodes
    out = subprocess.check_output(["ipfs", "id"], env={**os.environ, "IPFS_PATH": sender.repo})
    print("Daemon1:", out)
    out2 = subprocess.check_output(["ipfs", "id"], env={**os.environ, "IPFS_PATH": receiver.repo})
    print("Daemon2:", out2)
    assert b"ID" in out and b"ID" in out2