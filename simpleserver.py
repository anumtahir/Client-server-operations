import socket
import sys
import os
import datetime
import uuid
import platform
import time 
from os.path import isfile, join
import os.path
import shutil
import subprocess as sp

WELCOME_MSG = "*****************************\nWelcome to SIMPLE server v0.1\n*****************************\n" # Welcome message to display to client
VALID_COMMANDS = ["HELP", "EXIT", "TIME", "MAC", "IP", "LIST", "OS", "USERS", "HOROSCOPE", "SEND <filename>", "CREATE server <filename>", "CREATE client <filename>","RECEIVE <filename>", "DELETE server <filename>", "DELETE client <filename>"] # Commands available to client
BUF_LEN = 4028 #Length of datastream buffer - any more bytes sent would be received in the next recv() call
IP = 'localhost'

def clientExit(client_sock):
  print("Client has disconnected")
  client_sock.send("Alright, see you later!".encode("utf-8"))

def clientHelp(client_sock):
  help_msg = "Following commands are available: \n"
  for command in VALID_COMMANDS:
    help_msg+= '\t' + command + '\n'

  client_sock.send(help_msg.encode("utf-8"))

def clientHoroscope(client_sock):
  message ="Do you really think a simple server knows your destiny?\nA smart server, however, might be able to help you.\nFor now, I predict that your time will be better spent finishing the programming assignment!"
  client_sock.send(message.encode("utf-8"))

def server_time(client_sock):
  message = time.localtime()
  t = "Time is " + str(message[3])+ ":" + str(message[4])+ ":" + str(message[5])
  client_sock.send(t.encode("utf-8"))


def server_IP(client_sock):
   message = socket.gethostbyname_ex(IP)
   message = message[2]
   message = message[0]
   client_sock.send(message.encode("utf-8"))

def server_MAC(client_sock):
   message = uuid.getnode()
   message = (':'.join(['{:02x}'.format((message >> el) & 0xff) for el in range(0,8*6,8)][::-1]))
   client_sock.send(message.encode("utf-8"))

def server_OS(client_sock):
   message = platform.platform()
   client_sock.send(message.encode("utf-8"))

def flist(client_sock):
   message = os.listdir()
   file = ""
   for el in message:
       file = file + el + " : "
   client_sock.send(file.encode("utf-8"))

def users(client_sock):
   message = sp.getoutput('w')
   client_sock.send(message.encode("utf-8"))


def create_sfile(client_sock, filename):
   path = "server/"
   filepath = os.path.join(path, filename)
   if os.path.isfile(filepath):
     message = "File " + filename+ " already exists on server side"
     print(message)
   else:
     file = open(filepath, 'w')
     file.close()
     message = "File "+filename + " has been created on server side"
     print(message)
   client_sock.send(message.encode("utf-8"))


def create_cfile(client_sock, filename):
   path = "client/"
   filepath = os.path.join(path, filename)
   if os.path.isfile(filepath):
     message = "File " + filename+ " already exists on client side"
     print(message)              
   else:
     file = open(filepath, 'w')
     file.close()
     message = "File "+filename + " has been created on client side"
     print(message)             
   client_sock.send(message.encode("utf-8"))


def send_file(client_sock, filename):
   serverpath = "server/"
   clientpath = "client/"
   clientfilepath = os.path.join(clientpath, filename)
   serverfilepath = os.path.join(serverpath, filename)
   if os.path.isfile(serverfilepath):
     message = "File " +filename+ " already exists on server side"
     print(message)
   else:
     shutil.copy(clientfilepath, serverpath)
     message = "File " +filename+ " has been sent to server side"
     print(message)
   client_sock.send(message.encode("utf-8"))


def receive_file(client_sock, filename):
   clientpath = "client/"
   serverpath = "server/"
   serverfilepath = os.path.join(serverpath, filename)
   if os.path.isfile(serverfilepath):
     shutil.copy(serverfilepath, clientpath)
     message = "File " +filename+" received on client side"
     print(message)
   else:
     message = "File "+filename+" is not present on  server side"
     print(message)
   client_sock.send(message.encode("utf-8"))


def delete_sfile(client_sock, filename):
   serverpath = "server/"
   serverfilepath = os.path.join(serverpath, filename)
   if os.path.isfile(serverfilepath):
     os.remove(serverfilepath)
     message = "File " +filename+" has been deleted on server side"
     print(message)
   else:
     message = "File "+filename+" is not present on server side"  
     print(message)
   client_sock.send(message.encode("utf-8"))


def delete_cfile(client_sock, filename):
   clientpath = "client/"
   clientfilepath = os.path.join(clientpath, filename)
   if os.path.isfile(clientfilepath):
     os.remove(clientfilepath)
     message = "File " +filename+" has been deleted on client side"
     print(message)             
   else:
     message = "File "+filename+" is not present on client side"
     print(message)                   
   client_sock.send(message.encode("utf-8"))


def analyzeInput(client_sock, client_addr, data, serverPort):
  # acts as the traffic police for the user's input: verifies the input has a valid command and
  # forwards it to the right function for response 

  # verify that the input is valid
  if data == "HELP":
    clientHelp(client_sock)

  elif data == "EXIT":
    clientExit(client_sock)
    return False # exit command must signal the caller that user wants to exit

  elif data == "HOROSCOPE":
    clientHoroscope(client_sock)
    
  elif data == "TIME":
    server_time(client_sock)

  elif data == "IP":
    server_IP(client_sock)
  
  elif data == "MAC":
    server_MAC(client_sock)

  elif data == "OS":
    server_OS(client_sock)
  
  elif data == "LIST":
    flist(client_sock)

  elif data == "USERS":
    users(client_sock)

  else:
    input_token = data.split()
    if(input_token[0] == "CREATE"):
      if(input_token[1] == "server"):
        create_sfile(client_sock, input_token[2])
        return True
      elif(input_token[1] == "client"):
        create_cfile(client_sock, input_token[2])
        return True
    
    elif(input_token[0] == "SEND"):
      send_file(client_sock, input_token[1])
      return True
    
    elif(input_token[0] == "RECEIVE"):
      receive_file(client_sock, input_token[1])
      return True
  
    elif(input_token[0] == "DELETE"):
      if(input_token[1] == "server"):
        delete_sfile(client_sock, input_token[2])
        return True
      elif(input_token[1] == "client"):
        delete_cfile(client_sock, input_token[2])
        return True

    clientHelp(client_sock)
    print("invalid command from client: " + data)

  return True # signal the caller the user DOES NOT want to exit

def runServer(serverPort):
  serverPort = int(serverPort)
  print("...creating local listener socket")
  # Create socket here
  listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  print("...binding socket to port")
  # Bind socket to port here
  listeningSocket.bind((IP,serverPort))

  print("...starting to listen at port")
  # Listen for incoming connections
  listeningSocket.listen(1)

  print("...waiting for connection")
  # Accept connection here and store client socket (client_sock) and client address tuple (client_addr)
  clientSock, clientAddr = listeningSocket.accept()
 
 
  # Send client the welcome message and print client IP and port
  clientSock.send(WELCOME_MSG.encode())
  print("Client IP & Port is:  ", clientAddr,clientSock)
  
  while True:
    data = clientSock.recv(BUF_LEN).decode("utf-8")
    print("c: " + data)
    if not analyzeInput(clientSock, clientAddr, data, serverPort):
      break

  clientSock.close()



# Do error handling for arguments here and store port number in the variable portNumber
if (int(sys.argv[1]) < 1024):
	print("Usage: simpleclient.py  <hostname>  < port number between 1024 and 65535>")
	sys.exit()
portNumber = sys.argv[1]


# DO NOT CHANGE CODE UNDERNEATH
print("Starting to run server at port " + str(portNumber))

runServer(portNumber)

print("Let's do this again sometime")
