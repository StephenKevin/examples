import socket


CLIENT_END = b'==CLIENT_END=='
CLIENT_END_LEN = len(CLIENT_END)
SERVER_END = b'==SERVER_END=='
SERVER_END_LEN = len(SERVER_END)

server_name = '127.0.0.1'
server_port = 12000
server_address = (server_name, server_port)

client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_tcp.connect(server_address)

msg = input('Input some message:\n')

msg = msg.encode()

for i in range(1_000_000):
    msg_i = msg[i*32:i*32+32]
    if msg_i:
        client_tcp.send(msg_i)
    else:
        client_tcp.send(CLIENT_END)
        break

full_back_msg = b''

while True:
    back_msg = client_tcp.recv(32)
    print('Received:', back_msg)
    full_back_msg += back_msg
    if full_back_msg.endswith(SERVER_END):
        client_tcp.close()
        print('Back msg:', full_back_msg[:-SERVER_END_LEN])
        break
