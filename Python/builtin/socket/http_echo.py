# HTTP echo


import socket
import time

CLIENT_END = b'==CLIENT_END=='
CLIENT_END_LEN = len(CLIENT_END)
SERVER_END = b'==SERVER_END=='
SERVER_END_LEN = len(SERVER_END)

server_name = ''
server_port = 80
server_address = (server_name, server_port)

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_tcp.bind(server_address)

server_tcp.listen(10)

print('Server started! Bind on', server_address)

data_cache = dict()
while True:
    connection, addr = server_tcp.accept()
    print('Accepted TCP connect from', addr)
    if addr not in data_cache:
        data_cache[addr] = b''

    while True:
        # data stream. You can set any amount bytes as you like
        msg = connection.recv(1024)
        print('Received', msg)
        time.sleep(2)
        if msg:
            data_cache[addr] += msg
        else:
            print(data_cache[addr])
            connection.send(data_cache[addr])
            connection.close()
            break

