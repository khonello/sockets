
import socket
import sys
import queue

q = queue.Queue(maxsize= 4)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 9595))
sock.listen(4)

clientSock, addr = sock.accept()
if (clientSock):

    q.put(clientSock, block= True)

    try:

        nm = sys.argv[1]
        print(f'Connection established from {addr} and Client name {nm}')
    except IndexError:
        print(f'Connection established from {addr} ')

    mssg = input('-> ').encode('utf-8', 'ignore')
    clientSock.send(mssg)

    newMssg = clientSock.recv(1024)
    if newMssg.decode('utf-8') == 'exit' or newMssg.decode('utf-8') == 'close':
        clientSock.close()

print(f'Connections received : {q.qsize()}')
sock.close()