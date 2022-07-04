
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

        if clientSock:

            print(f'Connection from IP {addr[0]} on port {addr[1]}.')
            if addrssQ.not_full and socksQ.not_full:

                addrssQ.put(addr)
                socksQ.put(clientSock)
            else:
                mssg = 'There is too much traffic, try again later.'.encode('utf-8', 'ignore')
                clientSock.send(mssg)
                clientSock.close()



def process_req(buf, tmp_folder, tmp_file):
    try:
        os.mkdir(tmp_folder); os.chdir(tmp_folder)

    except FileExistsError:
        os.chdir(tmp_folder)

    while socksQ.not_empty:
        sock = socksQ.get()
        mssg = 'Server ready to receive file...'.encode('utf-8')

        sock.send(mssg)
        raw_byte = sock.recv(buf)

        file = __import__('io').BytesIO(raw_byte);
        with open(tmp_file, 'wb') as f:
            if f.writable():
                f.write(file.read())

                subprocess.Popen(['black', tmp_file])

        
        with open(tmp_file, 'rb') as f:
            if f.readable():

                sock.send(f.read())
                sock.close()



try:
   PP = sys.argv[1]
except IndexError:
   PP = 9696

create_sock_args = ['127.0.0.1', PP, 4]
process_req_args = [2048, 'temp', 'tempfile.py']


th1 = threading.Thread(target= create_sock, args= create_sock_args)
th2 = threading.Thread(target= process_req, args= process_req_args)

th1.start()
th2.start()


