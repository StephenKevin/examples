import socket

CLIENT_END = b'==CLIENT_END=='
CLIENT_END_LEN = len(CLIENT_END)
SERVER_END = b'==SERVER_END=='
SERVER_END_LEN = len(SERVER_END)

server_name = ''
server_port = 12000
server_addres = (server_name, server_port)

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_tcp.bind(server_addres)

server_tcp.listen(10)

print('Server started! Bind on', server_addres)

data_cache = dict()
while True:
    connection, addr = server_tcp.accept()
    print('Accepted TCP connect from', addr)
    if addr not in data_cache:
        data_cache[addr] = b''

    while True:
        msg = connection.recv(32)   # data stream. You can set any amount bytes as you like
        print('Received', msg)
        data_cache[addr] += msg
        if data_cache[addr].endswith(CLIENT_END):
            back_msg = data_cache[addr][:-CLIENT_END_LEN].upper() + SERVER_END
            print('Sent back:', back_msg)
            connection.send(back_msg)
            connection.close()
            break
