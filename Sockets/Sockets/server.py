
import socket
import sys
import os
import queue
import subprocess
import threading
import pathlib
import zipfile


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

        os.makedirs(tmp_folder)
    except OSError:

        while socksQ.not_empty:

            sock = socksQ.get()
            mssg = 'Server ready to receive file...'.encode('utf-8')

            sock.send(mssg)
            raw_byte = sock.recv(buf)

            file = __import__('io').BytesIO(raw_byte);

            path = pathlib.Path(os.getcwd()).joinpath(tmp_folder) 
            tmp_file_path = path.joinpath(tmp_file)

            with open(tmp_file_path, 'wb') as f:
                if f.writable():
                    f.write(file.read())

                    err_path = path.joinpath('err.md'); out_path = path.joinpath('out.md')
                    err = open(err_path, 'w'); out = open(out_path, 'w')

                    subprocess.Popen(['black', tmp_file_path], stderr= err, stdout= out); subprocess.Popen(['pylint', tmp_file_path], stderr= err, stdout= out)
                    if err.closed and out.closed:
                        ...
                    else:
                        err.close(); out.close()

            # Three zipfiles to send

            zips_path = [tmp_file_path, err_path, out_path]

            try:

                #create zipfiles if not existed
                x_zip_files = [zipfile.ZipFile(f'{f}.zip', 'x').write(f) for f in zips_path]
                i = 0

                for _ in x_zip_files:
                    
                    with open(x_zip_files[i], 'rb') as f:

                        sock.send(f.read())
                    i+=1

                    __import__('time').sleep(2)

            except FileExistsError:

                #replace zipfiles if exists
                c_zip_files = [zipfile.ZipFile(f'{f}.zip', 'c').write(f) for f in zips_path]
                i = 0

                for _ in c_zip_files:

                    with open(c_zip_files[i], 'rb') as f:
                        
                        sock.send(f.read())
                    i+=1

                    __import__('time').sleep(2)

             
            sock.close()



try:
   PP = sys.argv[1]
except IndexError:
   PP = 9696

create_sock_args = ['127.0.0.1', PP, 4]
process_req_args = [2048, 'temp', 're-factored.py']


th1 = threading.Thread(target= create_sock, args= create_sock_args)
th2 = threading.Thread(target= process_req, args= process_req_args)


th1.start()
th2.start()


