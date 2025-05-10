from udp_sock import ReceiverPort
from udp_sock import SenderPort
import socket
import threading
import time



class Server:
    def __init__(self):
        self.sender = SenderPort(port=4002, dest_ip="127.0.0.1")
        self.receiver = ReceiverPort(port=4001)
        self.receiver.sock.settimeout(1.0)
        self.alive = True
        self.th1 = threading.Thread(target=self.receive_thread,daemon=True)
        self.th1.start()

    def receive_thread(self):
        data = None
        while self.alive:
            try:
                data = self.receiver.recv()
            except socket.timeout:
                pass
            if data:
                self.sender.send(data)
                data = None

    def halt(self):
        self.alive = False
        if self.th1:
            ## if recv is blocking control, thread cannot join().
            self.th1.join()
        if self.sender:
            self.sender.close()
        if self.receiver:
            self.receiver.close()
        print("Server halt.")


s = Server()

for _ in range(30):
    time.sleep(1)
    print("time")

s.halt()
print("out")
