"""class: DevSocket *experimental*"""
from socketserver import BaseRequestHandler, UnixStreamServer
import subprocess

from .config import Config


class DevSocketHandler(BaseRequestHandler):
    """handle all requests to the dev socket"""

    def handle(self):
        """handle requests sent to the socket"""
        mdk_command = str(self.request.recv(1024), "utf-8").strip("\n").split(" ")
        mdk_command.insert(0, "mdk")
        print(mdk_command)
        subprocess.call(mdk_command)


class DevSocket(UnixStreamServer):
    """initialize mdkshared socket"""
    def __init__(self):
        config = Config()
        self.socket_path = config.host_shared_path/config.shared_socket_name
        if self.socket_path.exists():
            self.socket_path.unlink()
        super(DevSocket, self).__init__( # type: ignore
            str(self.socket_path),
            DevSocketHandler,
        )
        self.serve_forever()
