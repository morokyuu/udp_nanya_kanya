
from udp_sock import ReceiverPort

rp = ReceiverPort(port=4002)
while True:
    data = rp.recv()
    for d in data:
        print(f'{d:02x} ',end='')
    print("")
