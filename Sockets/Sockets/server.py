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

def str_to_list(arg):

    lst  = []
    lst[:0] = arg

    return lst

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
        os.mkdir(tmp_folder)
    except:
        ...
    finally:
            sock = socksQ.get()
            mssg = 'Server ready to receive file...'.encode('utf-8')

            sock.send(mssg)
            raw_byte = sock.recv(buf)

            file = __import__('io').BytesIO(raw_byte);

            path = pathlib.Path(os.curdir).joinpath(tmp_folder) 
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


            zips_path = [tmp_file_path, err_path, out_path]
            archive_path = path.joinpath('password-is-khonello.zip')

            #create zipfiles if not existed
            try:
                x_zip_file = zipfile.ZipFile(archive_path, 'w')

                for e in zips_path:

                   x_zip_file.write(e)
                x_zip_file.setpassword(b'khonello')

                with open(archive_path, 'rb') as f:

                    sock.send(f.read())


            #replace zipfiles if exists
            except FileExistsError:
                os.remove(archive_path)

                c_zip_file = zipfile.ZipFile(archive_path, 'w')

                for e in zips_path:

                   c_zip_file.write(e)
                c_zip_file.setpassword(b'khonello')

                with open(archive_path, 'rb') as f:

                    sock.send(f.read())
             
            sock.close()



try:
   PP = sys.argv[1]
except IndexError:
   PP = 9696

create_sock_args = ['127.0.0.1', PP, 4]
process_req_args = [4096, 'temp', 're-factored.py']


th1 = threading.Thread(target= create_sock, args= create_sock_args)
th2 = threading.Thread(target= process_req, args= process_req_args)


th1.start()
th2.start()


