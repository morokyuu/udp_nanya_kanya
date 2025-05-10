from udp_sock import ReceiverPort
from udp_sock import SenderPort
import threading
import time



class Server:
    def __init__(self):
        self.sender = SenderPort(port=4002, dest_ip="127.0.0.1")
        self.receiver = ReceiverPort(port=4001)
        self.alive = True
        self.th1 = threading.Thread(target=self.receive_thread,daemon=True)
        self.th1.start()

    def receive_thread(self):
        while self.alive:
            data = self.receiver.recv()
            self.sender.send(data)

    def halt(self):
        print("Server halt.")
        self.alive = False
        if self.th1:
            print("f1")
            self.th1.join()
        if self.sender:
            print("f2")
            self.sender.close()
        if self.receiver:
            self.receiver.close()
        print("finish")


s = Server()

for _ in range(3):
    time.sleep(1)
    print("time")

s.halt()
print("out")
