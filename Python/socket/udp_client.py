import socket
import time

server_name = '127.0.0.1'
server_port = 12000
server_address = (server_name, server_port)

client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = input('input some message:\n')
msg = msg.encode()

for i in range(10_000_000):
    msg_i = msg[i*32:i*32+32]
    if msg_i:
        client_udp.sendto(msg_i, server_address)
        print(f'Sent msg_{i}:', msg_i)
        time.sleep(1)
    else:
        client_udp.sendto(b'SIGNAL_FIN', server_address)
        print('Sent SIGNAL_FIN')
        break

backdata, addr = client_udp.recvfrom(2048)
print(backdata)
client_udp.close()
