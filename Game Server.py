'''
Citations
https://kdchin.gitbooks.io/sockets-module-manual/content/
https://www.gitbook.com/book/qwewy/pygame-module-manual/details
https://qwewy.gitbooks.io/pygame-module-manual/content/chapter1/framework.html
https://www.reddit.com/r/pygame/comments/3y03c9/how_to_check_if_sprite_group_is
_empty/?st=jagatxz5&sh=ecede6cf
http://millionthvector.blogspot.com/p/free-sprites.html
https://www.youtube.com/watch?v=EF_8ZFSxgyQ
https://stackoverflow.com/questions/38028970/how-to-assign-sounds-to-channels-in-pygame
https://www.pygame.org/docs/
http://hpr2.org/post/conversation-wednesday-june-21st-2017
https://www.youtube.com/watch?v=t3eh6YiyCoQ
https://www.youtube.com/watch?v=W1xwTqgzQ_g
'''
####################################
# TP3
# by Calvin ZH Qiao
# AndrewID: zhuhanq 
####################################
'''
Game Goal
Collect "1", "1", "2" elements in each round from each boss to enter the  
112 planet
'''

import socket
import threading
from queue import Queue
import time

HOST = "localhost" # put your IP address here if playing on multiple computers
PORT = 50003
BACKLOG = 4

timer = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
    except:
      # we failed
      return

def serverThread(clientele, serverChannel):
  timer = 0
  
  while True:
    timer += 1
    # print("timer = ", timer)
    msg = serverChannel.get(True, None)
    # print("got here")
    # print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()

clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

names = ["PlayerOne", "PlayerTwo", "PlayerThree", "PlayerFour"]
# only plan to use first two players 

while True:
  # print(time.time())
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  myID = names[playerNum]
  # print(myID, playerNum)
  for cID in clientele:
    # print (repr(cID), repr(playerNum))
    clientele[cID].send(("newPlayer %s\n" % myID).encode())
    client.send(("newPlayer %s\n" % cID).encode())
  clientele[myID] = client
  client.send(("myIDis %s \n" % myID).encode())
  # print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1
