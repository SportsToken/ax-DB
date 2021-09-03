from AXdata import *
from Athlete_functions import *
import datetime

# QuestDB specifc
import time
import socket


DATA = Pull_new_data()
time = datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")

# QuestDB localhost
HOST = 'localhost'
PORT = 9009
# For UDP, change socket.SOCK_STREAM to socket.SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))
for athlete in MLB_athlete_list:
    athlete_data = Get_athlete_data(DATA, athlete)
    _id = athlete_data['PlayerID']
    name = athlete_data['Name']
    name = name.replace(' ', '_')
    name = name + ('_' + str(_id))

    WAR = Get_WAR_MLB(athlete_data)
    WAR = float(WAR*2000000)

    string = f'mlb,name={name} value={WAR}\n'

    # Send WAR Stats
    sock.sendall((string).encode())
    print('Data sent')

sock.close()
