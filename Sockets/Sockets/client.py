import sys
import socket


def conn(IP:str, port:int, buf:int, filename:str):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, port))

    def process_req(buf, file_name):

        mssg = sock.recv(1024).decode('utf-8')
        print(mssg)

        __import__('os').listdir(__import__('os').getcwd())

        script = input('Provide filename of python script to use. ')
        with open(script, 'rb') as f:
            sock.send(f.read())
        
        with open(file_name, 'wb') as f:
            if f.writable():
                raw_byte = sock.recv(buf)
                file = __import__('io').BytesIO(raw_byte)

                f.write(file)

    process_req(buf, filename)

try:
   PP = sys.argv[1]
except IndexError:
   PP = 9696

conn_args = []

conn_args[0] = '127.0.0.1'
conn_args[1] = PP
conn_args[2] = 2048
conn_args[3] = 'refactor.py'