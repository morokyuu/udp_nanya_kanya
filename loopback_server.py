from udp_sock import ReceiverPort
from udp_sock import SenderPort
import socket
import threading
import time
import random



class Server:
    def __init__(self):
        self.sender = SenderPort(port=4002, dest_ip="127.0.0.1")
        self.receiver = ReceiverPort(port=4001)
        self.receiver.sock.settimeout(1.0)
        self.alive = True
        self.th1 = threading.Thread(target=self.receive_thread,daemon=True)
        self.th1.start()

    def _sendback(self,data):
        ## sendback delay simulation
        delay_sim = random.choice([0.001,0.005,0.04,0.08,0.15,0.7])
        time.sleep(delay_sim)

        ## unpack bytearray 
        d = list(data)

        ## accidentially cmd change
        d[0] = random.choice([d[0]]*9 + [0x00]) # false will occer 10%
        #d[0] = random.choice([d[0]]*1 + [0x00]*9) # false will occer 10%

        ## increment last element of data
        d[-1] += 1

        self.sender.send(bytearray(d))
        print(f'sendback data={d}')

    def receive_thread(self):
        data = None
        while self.alive:
            try:
                data = self.receiver.recv()
            except socket.timeout:
                pass
            if data:
                print(f'received data={data}')
                self._sendback(data)
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

for _ in range(60):
    time.sleep(1)
    print(".",end='')

s.halt()
print("out")
