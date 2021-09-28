import socket
import requests
import json

# Constants
HEADER = ''
SDIO_URL = ''
HOST = ''
PORT = ''

def getData():
        response = requests.get(SDIO_URL, headers=HEADER)
        theData = response.json()
        return theData

def run():
    # Define the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define socket
    sock.connect((HOST, PORT)) # connect to socket
    # Loop the entire json
    try: # find potential errors
        str = 'words brah'
        sock.sendall((str).encode())
    except socket.error as e:
        print("Got error: %s" % (e))

    except: # print names of athletes not available
        print(athlete)
    sock.close() # close socket
# exec
    run()