import sys
import socket
import logging

fmt = '%(levelname)s :: %(asctime)s :: %(message)s'
logging.basicConfig(format= fmt, level= logging.DEBUG, filename= 'log.txt', filemode= 'a')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 9595))

mssg = sock.recv(1024)
logging.info(mssg.decode('utf-8'))

print(mssg.decode('utf-8'))

newMssg = input('Enter command to close connection. ').encode('utf-8')
sock.send(newMssg)