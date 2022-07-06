import sys
import socket
import os

def conn(*args, **kwargs):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args[0], args[1]))

    def process_req(buf, file_name):

        mssg = sock.recv(1024).decode('utf-8')
        print(mssg)

        dirs = os.listdir(os.curdir)
        for x in dirs:  print(x)

        script = input('Provide filename of python script to use. ')
        if script[-2:] == 'py':
            with open(script, 'rb') as f:
                sock.send(f.read())

            raw_byte = sock.recv(buf)
            file = __import__('io').BytesIO(raw_byte)

            with open(file_name, 'wb') as z:
                z.write(file.read())
        

            print('Receiving files...')

        else:
            print('The file type choosen is not supported')
            print('Terminating...')

            sock.close()


    process_req(args[2], args[3])

try:
   PP = int(sys.argv[1])
except IndexError:
   PP = 9696

IP = '127.0.0.1'; BUF = 4096; FILE = 'password-is-khonello.zip'
conn(IP, PP, BUF, FILE)