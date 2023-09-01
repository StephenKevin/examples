import socket

server_port = 12000
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_udp.bind(('', server_port))
print(f'UDP server started! Bind on port {server_port}.\n')

data_cache = dict()
while True:
    msg, addr = server_udp.recvfrom(32)
    if addr not in data_cache:
        data_cache[addr] = b''
    print(f'receiving from {addr}:', msg)
    if msg == b'SIGNAL_FIN':
        back_msg = data_cache[addr].upper()
        server_udp.sendto(back_msg, addr)
        del data_cache[addr]
        del back_msg
        print('Sent back!')
    else:
        data_cache[addr] += msg
