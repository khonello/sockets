import sys
import socket
import os


def conn(*args, **kwargs):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args[0], args[1]))

    def process_req(buf, file_name):

        mssg = sock.recv(1024).decode('utf-8')
        print(mssg)
        os.walk(os.getcwd(), topdown= False)

        script = input('Provide filename of python script to use. ')
        with open(script, 'rb') as f:
            sock.send(f.read())
        
        with open(file_name, 'wb') as f:
            if f.writable():
                raw_byte = sock.recv(buf)
                file = __import__('io').BytesIO(raw_byte)

                f.write(file.read())

    process_req(args[2], args[3])

try:
   PP = sys.argv[1]
except IndexError:
   PP = 9696

IP = '127.0.0.1'; BUF = 2048; FILE = 'refactor.py'
conn(IP, PP, BUF, FILE)