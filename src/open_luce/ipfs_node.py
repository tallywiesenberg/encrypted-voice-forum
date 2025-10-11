from dataclasses import dataclass
import subprocess
import aioipfs

@dataclass
class IPFSNode:
    name: str
    repo: str
    host: str
    port: int
    process: subprocess.Popen

    @property
    def api_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def client(self) -> aioipfs.AsyncIPFS:
        """
        Create a new AsyncIPFS client bound to this node.
        You should use it in an async context manager:
            async with node.client() as c:
                await c.id()
        """
        return aioipfs.AsyncIPFS(host=self.host, port=self.port)