from udp_sock import ReceiverPort
from udp_sock import SenderPort
import socket
import threading
import time
import random


class Cmd_client:
    def __init__(self):
        self.sender = SenderPort(port=4001, dest_ip="127.0.0.1")
        self.receiver = ReceiverPort(port=4002)
    
    def send(self,cmd):
        timeout = [0.1,0.2,0.4,0.8]

        for i in range(len(timeout)):
            self.receiver.sock.settimeout(timeout[i])

            self.th1 = threading.Thread(target=self.receive_thread,args=(cmd,),daemon=True)
            self.th1.start()

            self.sender.send(cmd)
            print(f'send to {self.sender.port} cmd={cmd}')

            self.th1.join()

            if self.data:
                print(f"success: received data = {self.data}")
                break
        


    def receive_thread(self,cmd):
        self.data = None
        try:
            self.data = self.receiver.recv()
        except socket.timeout:
            print("\033[31m err: timeout \033[0m")

        if self.data and (not self.data[0] == cmd[0]):
            print(f"err: expected packet is cmd={cmd[0]} data = {self.data}")
            self.data = None


#    def halt(self):
#        self.alive = False
#        if self.th1:
#            ## if recv is blocking control, thread cannot join().
#            self.th1.join()
#        if self.sender:
#            self.sender.close()
#        if self.receiver:
#            self.receiver.close()
#        print("Server halt.")


cc = Cmd_client()
cc.send(bytearray([0x01,0xff,0x01]))


