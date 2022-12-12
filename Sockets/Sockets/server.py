import socket
import sys
import os
import queue
import subprocess
import threading
import pathlib
import shutil
import tempfile
import io

addrssQ = queue.Queue(maxsize= 4)
socksQ = queue.Queue(maxsize= 4)

def str_to_list(arg):

    lst  = []
    lst[:0] = arg

    return lst


# Create function to listen to connections
def create_sock(IP:str, port:int, conn:int):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, port))
    sock.listen(conn)

    print('server started successfully')
    while True:
        clientSock, addr = sock.accept()

        if clientSock:

            print(f'connection from IP {addr[0]} on PORT {addr[1]}.')
            if addrssQ.not_full and socksQ.not_full:

                addrssQ.put(addr)
                socksQ.put(clientSock)
            else:
                mssg = 'There is too much traffic, try again later.'.encode('utf-8', 'ignore')
                clientSock.send(mssg)
                clientSock.close()



def process_req(buf, tmp_folder, tmp_file):

    try:
        os.mkdir(tmp_folder)
    except:
        ...
    finally:
            sock = socksQ.get(block= True, timeout= None)
            mssg = 'ready to receive file...'.encode('utf-8')

            sock.send(mssg)
            raw_byte = sock.recv(buf)
            print('receiving file...')

            file = __import__('io').BytesIO(raw_byte)

            path = pathlib.Path(os.curdir).joinpath(tmp_folder) 
            tmp_file_path = path.joinpath(tmp_file).absolute()

            # with open(tmp_file, 'w') as txt:
            #     txt.write(file.read().decode().strip())

            with open(tmp_file_path, 'wb') as f:

                if f.writable() and file.readable():
                    f.write(file.read())

                    err_path = path.joinpath('pylint_err.txt').absolute(); out_path = path.joinpath('pylint_out.txt').absolute()
                    err = open(err_path, 'w'); out = open(out_path, 'w')
                    
                    black = subprocess.Popen(['black', '--target-version', 'py38', tmp_file_path], stderr= subprocess.PIPE, stdout= subprocess.PIPE)                                            # output not needed  
                    _, __ = black.communicate()

                    pylint = subprocess.Popen(['pylint', '--suggestion-mode=y', '--output-format=colorized', '--reports=y', tmp_file_path], stderr= subprocess.PIPE, stdout= subprocess.PIPE)   # output very important
                    stdout, stderr = pylint.communicate()  

                    if out.writable() and err.writable():
                        out.write(stdout.decode()); err.write(stderr.decode())

                    if not err.closed and not out.closed:
                        err.close(); out.close() 

            tmp_nam = os.path.basename(tempfile.mktemp())
            archive_path = pathlib.Path(os.curdir).joinpath(f'{tmp_nam}.zip')

            __import__('time').sleep(2.0)
            def for_try_block():
    
                shutil.make_archive(tmp_nam, 'zip', path)
                with open(archive_path, 'rb') as f:

                    sock.send(f.read())
                    print('new file has been sent')
                sock.close()

                os.remove(archive_path)
                shutil.rmtree(path, ignore_errors= True)

            #create zipfiles if not existed
            try:
                for_try_block()

            except FileExistsError:

                os.remove(archive_path)
                for_try_block()


try:
   PP = sys.argv[1]
except IndexError:
   PP = 9695

create_sock_args = ['127.0.0.1', PP, 4]
process_req_args = [4096, 'temp', 're-factored.py']


th1 = threading.Thread(target= create_sock, args= create_sock_args)
th2 = threading.Thread(target= process_req, args= process_req_args)

th1.start()
th2.start()


