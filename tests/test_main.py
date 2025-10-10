import os
import subprocess
import tempfile
import time
import pytest
import asyncio
import shutil
import json

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

@pytest.fixture(scope="session")
async def ipfs_daemons():
    tmp1 = tempfile.mkdtemp()
    tmp2 = tempfile.mkdtemp()

    # init both repos
    init_ipfs_repo(tmp1, 5001, 4001, 8080)
    init_ipfs_repo(tmp2, 5002, 4002, 8081)

    # start daemons
    d1 = subprocess.Popen(["ipfs", "daemon", "--enable-pubsub-experiment"], env={**os.environ, "IPFS_PATH": tmp1})
    d2 = subprocess.Popen(["ipfs", "daemon", "--enable-pubsub-experiment"], env={**os.environ, "IPFS_PATH": tmp2})

    # give them time to boot
    time.sleep(5)

    yield (tmp1, tmp2)  # test code can use IPFS_PATH=tmp1/tmp2 with aioipfs or subprocess

    # cleanup
    d1.terminate()
    d2.terminate()
    d1.wait()
    d2.wait()
    shutil.rmtree(tmp1)
    shutil.rmtree(tmp2)
    
async def test_message_sent(ipfs_daemons):
    repo1, repo2 = ipfs_daemons
    repo1.

async def test_ipfs_ping(ipfs_daemons):
    repo1, repo2 = ipfs_daemons
    out = subprocess.check_output(["ipfs", "id"], env={**os.environ, "IPFS_PATH": repo1})
    print("Daemon1:", out)
    out2 = subprocess.check_output(["ipfs", "id"], env={**os.environ, "IPFS_PATH": repo2})
    print("Daemon2:", out2)
    assert b"ID" in out and b"ID" in out2