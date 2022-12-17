import socket
import sys
import os
import queue
import subprocess
import threading
import pathlib
import shutil
import tempfile
import psutil
import datetime
import asyncio
import time
from random import choice


addrssQ = queue.Queue(maxsize= 4)
socksQ = queue.Queue(maxsize= 4)

# def str_to_list(arg):

#     lst  = []
#     lst[:0] = arg

#     return lst

async def stats():

    fg = choice([str(x) for x in range(1,10)]+[y for y in __import__('string').ascii_uppercase][:6])

    os.system(f'color 0{fg}')
    print('server started successfully')

    ps = psutil.cpu_percent()
    freq = psutil.cpu_freq()

    users = psutil.users()[0]
    print(f"\ncpu usage {ps}\tcpu frequency {freq.current} [max :: {freq.max}]")

    await asyncio.sleep(1.0)
    print(f"user [{users.name}] terminal [{users.terminal}] host [{users.host}] started [{datetime.datetime.fromtimestamp(users.started).ctime()}]\n")

# Create function to listen to connections
async def create_sock(IP:str, port:int, conn:int, buf:int, tmp_folder:str, tmp_file:str, /):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, port))
    sock.listen(conn)

    while True:

        await stats()
        clientSock, addr = sock.accept()
       
        if clientSock:

            conn = f'connection from IP {addr[0]} on PORT {addr[1]}.'

            async def magic():
                for c in conn:
                    print(c, end= '')

                    sys.stdout.flush()
                    time.sleep(0.01)
                print('', end= '\n')
            await magic()
            
            if addrssQ.not_full and socksQ.not_full:

                addrssQ.put(addr)
                socksQ.put(clientSock)

                try:
                    os.mkdir(tmp_folder)
                except:
                    shutil.rmtree(os.path.abspath(tmp_folder))
                finally:
                        getsock = socksQ.get(block= True, timeout= None)
                        mssg = 'ready to receive file...'.encode('utf-8')

                        getsock.send(mssg)
                        async def foo():
                            global raw_byte

                            raw_byte = getsock.recv(buf)
                            print('receiving file...')

                        await foo()
                        
                        file = __import__('io').BytesIO(raw_byte)

                        path = pathlib.Path(os.curdir).joinpath(tmp_folder) 
                        tmp_file_path = path.joinpath(tmp_file).absolute()

                        with open(tmp_file_path, 'wb') as f:
                            fd = f.fileno()

                            if f.writable() and file.readable():
                                f.write(file.read())
                                os.fsync(fd)
                                    
                        black = subprocess.Popen(['black', '--target-version', 'py38', tmp_file_path], stderr= subprocess.PIPE, stdout= subprocess.PIPE)                                            # output not needed  
                        _, __ = black.communicate()

                        pylint = subprocess.Popen(['pylint', '--suggestion-mode=y', '--output-format=colorized', '--reports=y', tmp_file_path], stderr= subprocess.PIPE, stdout= subprocess.PIPE)   # output very important
                        stdout, stderr = pylint.communicate()  

                        if os.path.isfile(tmp_file_path):
                
                            err_path = path.joinpath('pylint_err.txt').absolute(); out_path = path.joinpath('pylint_out.txt').absolute()
                            err = open(err_path, 'w'); out = open(out_path, 'w')

                            if out.writable() and err.writable():
                                out.write(stdout.decode()); err.write(stderr.decode())

                                if not err.closed and not out.closed:
                                    err.close(); out.close() 

                        else:
                            sys.exit('Something went terribly wrong')


                        tmp_nam = os.path.basename(tempfile.mktemp())
                        archive_path = pathlib.Path(os.curdir).joinpath(f'{tmp_nam}.zip')

                        await asyncio.sleep(2.0)
                        async def for_try_block():
                
                            shutil.make_archive(tmp_nam, 'zip', path)
                            with open(archive_path, 'rb') as f:

                                getsock.send(f.read())
                                print('new file has been sent')
                            
                            getsock.close()

                            await asyncio.sleep(2.0)
                            os.system('cls')

                            os.remove(archive_path)
                            shutil.rmtree(path, ignore_errors= True)

                        #create zipfiles if not existed
                        try:
                            await for_try_block()

                        except FileExistsError:

                            os.remove(archive_path)
                            await for_try_block()

        else:
            mssg = 'There is too much traffic, try again later.'.encode('utf-8', 'ignore')

            clientSock.send(mssg)
            clientSock.close()

            await asyncio.sleep(1.0)
            os.system('cls')

try:
   PP = sys.argv[1]
except IndexError:
   PP = 9695

create_sock_args = ['127.0.0.1', PP, 4, 4096, 'temp', 're-factored.py']
asyncio.run((lambda arg: create_sock(*arg))(create_sock_args))