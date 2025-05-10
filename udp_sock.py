import socket

class SenderPort:
    def __init__(self, port: int, dest_ip: str):
        self.port = port
        self.dest_ip = dest_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, cmd: bytearray):
        self.sock.sendto(cmd, (self.dest_ip, self.port))


class ReceiverPort:
    def __init__(self, port: int, dest_ip: str = '0.0.0.0'):
        self.port = port
        self.dest_ip = dest_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.dest_ip, self.port))
        print(f"Listening on {self.dest_ip}:{self.port}")

    def recv(self, buffer_size: int = 1024) -> str:
        data, addr = self.sock.recvfrom(buffer_size)
        return data

if __name__ == '__main__':
    sender = SenderPort(port=4001, dest_ip="127.0.0.1")
    sender.send(bytearray([0x64,0x66,0x67]))

#    receiver = ReceiverPort(port=4002)
#    msg = receiver.recv()

