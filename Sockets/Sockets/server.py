
import socket
import sys
import os
import queue
import subprocess
import threading

addrssQ = queue.Queue(maxsize= 4)
socksQ = queue.Queue(maxsize= 4)

# Create function to listen to connections
def create_sock(IP:str, port:int, conn:int):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, port))
    sock.listen(conn)

    while True:
        clientSock, addr = sock.accept()
        if addrssQ.not_full() and socksQ.not_full():

            addrssQ.put(addr)
            socksQ.put(clientSock)
        else:
            mssg = 'There is too much traffic, try again later.'.encode('utf-8', 'ignore')
            clientSock.send(mssg)
            clientSock.close()



def process_req(buf, tmp_folder, tmp_file):
    os.mkdir(tmp_folder)

    while socksQ.not_empty:
        sock = socksQ.get()
        mssg = 'Server ready to receive file...'.encode('utf-8')

        sock.send(mssg)
        raw_byte = sock.recv(buf)

        file = __import__('io').BytesIO(raw_byte);

        os.chdir(tmp_folder)
        with open(tmp_file) as f:
            if f.writable():
                f.write(file)

        subprocess.Popen(['black', tmp_file])
        with open(tmp_file, 'rb') as f:
            if f.readable():

                sock.send(f.read())
                sock.close()

create_sock_args = []
process_req_args = []

try:
   PP = sys.argv[1]
except IndexError:
   PP = 9696

create_sock_args[0] = '127.0.0.1'
create_sock_args[1] = PP
create_sock_args[2] = 4

process_req_args[0] = 2048
process_req_args[1] = 'temp'
process_req_args[2] = 'py_script.py'


th1 = threading.Thread(target= create_sock, args= create_sock_args)
th2 = threading.Thread(target= process_req, args= process_req_args)