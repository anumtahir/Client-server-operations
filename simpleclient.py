
import socket
import sys
import os
import re

BUF_LEN = 4028 #Length of datastream buffer - any more bytes sent would be received in the next recv() call

def getInfoFromServer(sock, user_input):
  # Write code here
   sock.sendall(user_input.encode("utf-8"))
   data = sock.recv(BUF_LEN).decode("utf-8")
   print(data)
  
  
def getExit(sock):
  sock.sendall("EXIT".encode("utf-8"))
  print("...exiting")
  data = sock.recv(BUF_LEN).decode("utf-8")
  print(data)

def analyzeInput(sock, user_input):
  if user_input == "HELP" or user_input == "HOROSCOPE":
    getInfoFromServer(sock, user_input)

  elif user_input == "EXIT":
    getExit(sock)
    return False

  elif user_input == "TIME":
    getInfoFromServer(sock, user_input)
  
  elif user_input == "IP":
    getInfoFromServer(sock, user_input)
  
  elif user_input == "MAC":
    getInfoFromServer(sock, user_input)

  elif user_input == "OS":
    getInfoFromServer(sock, user_input)  

  elif user_input == "LIST":
    getInfoFromServer(sock, user_input)
 
  elif user_input == "USERS":
    getInfoFromServer(sock, user_input)


  else:
    input_token = user_input.split()
    if(input_token[0]=="CREATE" and len(input_token)==3):
      if(input_token[1] =="server"):
        if re.search(r'[^A-Za-z0-9_\-\\]',input_token[2]):
          file = input_token[2]
          user_input = input_token[0]+" " +input_token[1]+" " + file
          getInfoFromServer(sock, user_input)
          return True
        else:
          print("Enter valid filename")
          return True
      elif(input_token[1]=="client"):
        if re.search(r'[^A-Za-z0-9_\-\\]',input_token[2]): 
          file = input_token[2]
          user_input = input_token[0]+" " +input_token[1]+" " + file 
          getInfoFromServer(sock, user_input) 
          return True
        else:
          print("Enter valid filename")
          return True  
    
    elif(input_token[0] == "SEND" and len(input_token)==2):
      clientpath = "client/"
      file = input_token[1]
      filepath = os.path.join(clientpath, file)
      if os.path.isfile(filepath):
        user_input = "SEND "+ file
        getInfoFromServer(sock, user_input)
        return True
      else:
        print("file " + file + " doesn't present on client side")  
        return True    
    
    elif(input_token[0] =="RECEIVE" and len(input_token)==2):
      clientpath = "client/"
      file = input_token[1]
      filepath = os.path.join(clientpath, file)
      if os.path.isfile(filepath):
        print("file " +file+" already exists on client side, want to keep or replaced?")
        decision = input("(R/K)")
        decision = decision.upper()
        if(decision == "K"):
          print("file " + file+ " not replaced")
          return True
        elif(decision == "R"):
          user_input = "RECEIVE " +file
          getInfoFromServer(sock, user_input)
          return True
      
      user_input = "RECEIVE " +file
      getInfoFromServer(sock, user_input)
      return True
    
    elif(input_token[0] == "DELETE" and len(input_token)==3):
      if(input_token[1] == "server"):
        file = input_token[2]
        user_input = input_token[0]+" " +input_token[1]+" " + file               
        getInfoFromServer(sock, user_input)
        return True    
      elif(input_token[1] =="client"):
        file = input_token[2]
        user_input = input_token[0]+" " +input_token[1]+" " + file             
        getInfoFromServer(sock, user_input)
        return True

    print("command not available")
    getInfoFromServer(sock, "HELP")

  return True

def runClient(serverName, serverPort):
  server_addr = (serverName, serverPort)
  print("...creating local connector socket")
  # Create socket (sock)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print("...connecting socket to " + serverName + ":" + str(serverPort))

  try:
    # Connect socket to server
    sock.connect((serverName, serverPort))
  except:
    # Exit with error message if connection error
    print("doesn't connect to server")

  # Receive the welcome message and print it
  welcome = sock.recv(1024).decode()
  print(welcome)
  while True:
    user_input = input("c: ")
    if len(user_input.split()) > 1:
      input_array = user_input.split()
      user_input = input_array[0].upper() + " " + ' '.join(input_array[1:]) # First word of input is case insensitive. It is always converted to upper case
    else:
      user_input = user_input.upper()
    print(user_input)
    if not analyzeInput(sock, user_input):
      break

  sock.close()
 
# Do error handling for arguments here
if (int(sys.argv[2]) < 1024 or sys.argv[1] != "localhost"):
        print("Usage: simpleclient.py  <localhost>  < port number between 1024 and 65535>")
        sys.exit()


  
# DO NOT CHANGE CODE UNDERNEATH
portNumber = int(sys.argv[2])
serverName = sys.argv[1]
print("Running client...")
print("Will try to connect to " + serverName + " at port " + str(portNumber))

runClient(serverName, portNumber)

print("Let's do this again sometime")
