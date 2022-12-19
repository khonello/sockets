import sys
import socket
import os
from random import choice

def conn(*args, **kwargs):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args[0], args[1]))

    def process_req(buf, file_name):
        
        fg = choice([str(x) for x in range(1,10)]+[y for y in __import__('string').ascii_uppercase][:6])
        os.system(f'color 0{fg}'); os.system('title khonello [ client ]')

        print('client has been started')
        print(sock.recv(4096).decode('utf-8'))

        dirs = os.listdir(os.curdir)
        for x in dirs:  print(x)

        def take_input():

            script = input('provide filename of python script to use. ')
            if script[-2:] == 'py':
                with open(script, 'rb') as f:
                    sock.send(f.read())

                raw_byte = sock.recv(buf)
                file = __import__('io').BytesIO(raw_byte)

                with open(file_name, 'wb') as f:

                    f.write(file.read())
                print('receiving files...')
                return

            else:
                print('the file type choosen is not supported')
                print('try again')

                return take_input()
        take_input()

        sock.close()


    process_req(args[2], args[3])

try:
   PP = int(sys.argv[1])
except IndexError:
   PP = 9696

IP = '127.0.0.1'; BUF = 4096; FILE = 'output.zip'
conn(IP, PP, BUF, FILE)