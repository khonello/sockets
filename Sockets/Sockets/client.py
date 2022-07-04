import sys
import socket
import os

def conn(*args, **kwargs):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args[0], args[1]))

    def process_req(buf, file_name):

        mssg = sock.recv(1024).decode('utf-8')
        print(mssg)

        dirs = os.listdir(os.getcwd())
        for x in dirs:  print(x)

        script = input('Provide filename of python script to use. ')
        if script[-2:] == 'py':
            with open(script, 'rb') as f:
                sock.send(f.read())


            for i in range(0,2):
                with open(f'{file_name}_{i}', 'wb') as f:
                    if f.writable():
                    
                        raw_byte = sock.recv(buf)

                        file = __import__('io').BytesIO(raw_byte)
                        f.write(file.read())

                        __import__('time').sleep(2)


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

IP = '127.0.0.1'; BUF = 2048; FILE = 'zip'
conn(IP, PP, BUF, FILE)