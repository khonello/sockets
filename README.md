# Sockets

Start the server which by default listens on port 9696 which can be changed later by modifier the config file.
The server listens for connection from client programs ( also available as client.py ). After the starting the client program it attempt connnection with the server and after successful connection, the client server is requested to provide filename of python script to be reformatted based on the PEP3 standards. After server receives file it processess the file and return zip files which contains the respective processed output files. 
Note: The server must be started first else an error will be raised since you are attempting connection with a server which has not been started yet.

<h6 style="color:red"> Run on only windows system </h6>