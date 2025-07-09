import socket
from threading import Thread

class WiFiSocket(object):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected: bool = False

    def connect(self) -> None:
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
        except socket.error as e:
            print(f"Connection error: {e}")
            self.connected = False

    def send_data(self, data: bytes) -> None:
        if self.connected:
            try:
                self.socket.send(data)
            except socket.error as e:
                print(f"Send error: {e}")

    def receive_data(self, buffer_size: int = 1) -> bytes | None:
        if self.connected:
            buffer = b''
            while len(buffer) < buffer_size:
                chunk = self.socket.recv(buffer_size - len(buffer))
                if not chunk:
                    raise ConnectionError("Socket connection closed before receiving all data.")
                buffer += chunk
            return buffer
        return None

    def close(self) -> None:
        if self.connected:
            self.socket.close()
            self.connected = False