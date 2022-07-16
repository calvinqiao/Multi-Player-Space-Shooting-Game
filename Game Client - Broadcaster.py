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
import math
import socket
import threading
from queue import Queue

HOST = "localhost" # put your IP address here if playing on multiple computers
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

import pygame, random
from pygamegame import PygameGame
from StartMenu import StartMenu
from SpaceShip import SpaceShip
from EnemyType1 import EnemyType1
from EnemyType2 import EnemyType2
from EnemyType3 import EnemyType3
from EnemyStation import EnemyStation
from BossType1 import BossType1
from Bullet import Bullet
from EnemyBullet import EnemyBullet
from Bomb import Bomb
from BossMissle import BossMissle
from Explosion import Explosion
from FirstAidStation import FirstAidStation
from BombSupplyStation import BombSupplyStation
from WeaponSupplyStation import WeaponSupplyStation
from FinalSceneCharacter1 import FinalSceneCharacter1
from FinalSceneCharacter2 import FinalSceneCharacter2

class Game(PygameGame):

    def init(self):
        self.randomSeeds = [1, 2, 3]
        # initialize other players
        self.otherSpaceships = dict()
        self.otherPlayersKeys = dict()
        self.currentOtherPlayer = ""
        self.otherPlayersBullets = dict()
        self.otherPlayersBombs = dict()
        self.otherPlayersBombNumbers = dict()
        self.allPlayers = pygame.sprite.Group()

        pygame.font.init() 
        
        self.pause = 0
        self.time = 0
        self.score, self.round, self.win = 0, 1, None
        self.bossType1Number = 0
        self.numPlayers = 1
        self.secondPlayer = 0
        self.mode = None
        self.advancedShooting = 0

        self.gameState = "startState" 
        self.thisPlayerAlive = 1
        
        StartMenu.init()
        startMenu = StartMenu(self.width//2, self.height//2)
        self.startMenuGroup = pygame.sprite.Group(startMenu)
        # initialize spaceship
        SpaceShip.init()
        ship = SpaceShip("thisPlayer", self.width//2, self.height*5//6)
        self.shipGroup = pygame.sprite.Group(ship)
        self.allPlayers.add(ship)
        # initialize enemy type 1 and enemy type 2
        EnemyType1.init()
        EnemyType2.init()
        EnemyType3.init()
        self.enemiesType1 = pygame.sprite.Group()
        self.enemiesType2 = pygame.sprite.Group()
        self.enemiesType3 = pygame.sprite.Group()
        # initialze enemy base station
        EnemyStation.init()
        self.enemyStations = pygame.sprite.Group()
        # initialize boss

        # initialize enemy type 2 bullets
        self.enemyBullets = pygame.sprite.Group()
        self.enemyType3Bullets = pygame.sprite.Group()
        # initialize spaceship bullets
        self.playerBullets = pygame.sprite.Group()
        # initialize spaceship bomb
        self.bombNums = 3
        Bomb.init()
        self.playerBombs = pygame.sprite.Group()
        
        # initialize boss
        BossType1.init()
        BossMissle.init()
        # does name boss1 need to be changed?
        self.bossType1Group = pygame.sprite.GroupSingle()
        # initialize explosions
        Explosion.init()
        self.explosions = pygame.sprite.Group()
        # initialize first aid stations
        FirstAidStation.init()
        self.firstAidStations = pygame.sprite.Group()
        self.bombSupplyStations = pygame.sprite.Group()
        self.weaponSupplyStations = pygame.sprite.Group()
        
        # initialize final scenes
        FinalSceneCharacter1.init()
        FinalSceneCharacter2.init()
        self.finalSceneCharacters1 = pygame.sprite.Group()
        self.finalSceneCharacters2 = pygame.sprite.Group()
        
        # music initial setting
        self.bgMusic = pygame.mixer.Sound('music/bgMusic.wav')
        self.channel1 = pygame.mixer.Channel(0) # argument must be int
        self.playBGMusic() ####### Need to uncomment this line later
        
    def playBGMusic(self):
        # channel2.play(explosionSound)
        # if self.playMusic == 1:
        self.channel1.play(self.bgMusic, loops = -1)
    
    def changeBGMusic(self, music):
        self.bgMusic = music
        self.playBGMusic()
        
    def text_objects(self, text,color):
        myfont = pygame.font.SysFont('Arial Rounded MT Bold', 30)
        textSurface = myfont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def processEvents(self):
        msg = ""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos), event.button)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouseReleased(*(event.pos))
            elif (event.type == pygame.MOUSEMOTION and
                  event.buttons == (0, 0, 0)):
                self.mouseMotion(*(event.pos))
            elif (event.type == pygame.MOUSEMOTION and
                  event.buttons[0] == 1):
                self.mouseDrag(*(event.pos))
            elif event.type == pygame.KEYDOWN:
                self._keys[event.key] = True
                self.keyPressed(event.key, event.mod)
                msg = "playerKeyDown %d\n" % (event.key)
            elif event.type == pygame.KEYUP:
                self._keys[event.key] = False
                self.keyReleased(event.key, event.mod)
                msg = "playerKeyUp %d\n" % (event.key)
            elif event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                self.playing = False
            if (msg != ""):
                # print ("sending: ", msg,)
                self.server.send(msg.encode())
    
    def mousePressed(self, x, y, button):
        if self.gameState == "gameState" or self.gameState == "in boss fight":
            self.gameStateMousePressed(x, y, button)
        elif self.gameState == "startState":
            self.startStateMousePressed(x, y, button)
        elif self.gameState == "endState":
            self.endStateMousePressed(x, y, button)
        elif self.gameState == "instructionState":
            self.instructionStateMousePressed(x, y, button)
        elif self.gameState == "pauseState":
            self.pauseStateMousePressed(x, y, button)

    
    def mouseMotion(self, x, y):
        if self.gameState == "gameState":
            self.gameStateMouseMotion(x, y)
            
    def keyPressed(self, keyCode, mod):
        if (self.pause == 0):
            if self.gameState == "gameState" or self.gameState == "in boss fight":
                self.gameStateKeyPressed(keyCode, mod)
            elif self.gameState == "startState":
                self.startStateKeyPressed(keyCode, mod)
            elif self.gameState == "endState":
                self.endStateKeyPressed(keyCode, mod)
            elif self.gameState == "instructionState":
                self.instructionStateKeyPressed(keyCode, mod)
            elif self.gameState == "pauseState":
                self.pauseStateKeyPressed(keyCode, mod)
            elif self.gameState == "finalState":
                self.finalStateKeyPressed(keyCode, mod)

    def timerFired(self, dt):
        # print("game state is ", self.gameState)
        self.time += 1
        # print("Other spaceships = ", self.otherSpaceships)
        # print("serverMsg size = ", serverMsg.qsize())
        # print("player nums is ", self.numPlayers)
        if self.gameState == "gameState" and self.secondPlayer == 1:
            self.numPlayers = 2
        while (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            try:
                # print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                # print("This command is ", command)

                if (command == "myIDis"):
                    myPID = msg[1]
                    self.shipGroup.sprites()[0].changePID(myPID)

                elif (command == "newPlayer"):
                    # print("Process newPlayer msg")
                    self.secondPlayer = 1
                    newPID = msg[1]
                    # print("Parsed newPID", end = '  ')
                    # print("new PID is ", newPID)
                    ship = SpaceShip(newPID, self.width//2, self.height*5//6)
                    group = pygame.sprite.Group(ship)
                    self.otherSpaceships[newPID] =  group 
                    self.allPlayers.add(ship)
                    self.otherPlayersKeys[newPID] = dict()
                    bulletsGroup = pygame.sprite.Group()
                    self.otherPlayersBullets[newPID] = bulletsGroup
                    bombsGroup = pygame.sprite.Group()
                    self.otherPlayersBombs[newPID] = bombsGroup
                    self.otherPlayersBombNumbers[newPID] = 3
                    self.time = 0
                    msg = "resetTimer %d\n" % (self.time)
                    self.server.send(msg.encode())
                    # self.time = 0
                elif (command == "resetTimer"):
                    thisTime = msg[2]
                    self.time = int(thisTime)    

                elif (command == "OtherPlayerFiredBullet"): # ship = self.shipGroup.sprites()[0]
                    # print("Process other players firing bullets")
                    PID = msg[1]
                    ship = self.otherSpaceships[PID].sprites()[0]
                    newBullet = Bullet(ship.x, ship.y-ship.height//2-Bullet.size//2)
                    self.otherPlayersBullets[PID].add(newBullet)
                elif (command == "OtherPlayerFiredBomb"):
                    # print("Process other players firing bombs")
                    PID = msg[1]
                    ship = self.otherSpaceships[PID].sprites()[0]
                    if self.otherPlayersBombNumbers[PID] > 0:
                        self.otherPlayersBombNumbers[PID] -= 1
                        ship = self.otherSpaceships[PID].sprites()[0]
                        newBomb = Bomb(ship.x, ship.y-ship.height//2-Bomb.size//2)
                        self.otherPlayersBombs[PID].add(newBomb)

                elif (command == "playerKeyDown"):
                    # print("Process key pressed", end = ' ')
                    PID = msg[1]
                    self.currentOtherPlayer = PID
                    thisKey = msg[2]
                    # print("this key = ", thisKey)
                    self.otherPlayersKeys[PID][thisKey] = True
                elif (command == "playerKeyUp"):
                    # print("Process key up")
                    PID = msg[1]
                    self.currentOtherPlayer = ""
                    thisKey = msg[2]
                    self.otherPlayersKeys[PID][thisKey] = False
                elif (command == "BossDamage"):
                    # print("Process HP change")
                    PID = msg[1]
                    bossDamage = int(msg[2])
                    for boss in self.bossType1Group:
                        boss.hp -= bossDamage
                        if (boss.hp < 0):
                            self.win = 1
                            # self.changeBGMusic()
                            # self.round += 1
                            self.bossType1Group.empty()
                            self.gameState = "endState"
                elif (command == "BossMoved"):
                    for boss in self.bossType1Group:
                        vx, vy = boss.velocity
                        vx = int(msg[2])
                        boss.velocity = vx, vy
                elif (command == "weWon"):
                    pass
                    # PID = msg[1]
                    # self.win = 1
                    # self.gameState = "endState"
                elif (command == "PlayerOut"):
                    PID = msg[1]
                    self.otherSpaceships[PID].empty()
            except Exception as e:               
                print("failed")
                print(e)
            serverMsg.task_done()
            
        if self.gameState == "gameState" or self.gameState == "in boss fight":
            self.gameStateTimerFired(dt)
        elif self.gameState == "startState":
            self.startStateTimerFired(dt)
        elif self.gameState == "endState":
            self.endStateTimerFired(dt)
        elif self.gameState == "instructionState":
            self.instructionStateTimerFired(dt)
        elif self.gameState == "pauseState":
            self.pauseStateTimerFired(dt)
        elif self.gameState == "finalState":
            self.finalStateTimerFired(dt)
    
    def redrawAll(self, screen):
        if self.gameState == "gameState" or self.gameState == "in boss fight":
            self.gameStateRedrawAll(screen)
        elif self.gameState == "startState":
            self.startStateRedrawAll(screen)
        elif self.gameState == "endState":
            self.endStateRedrawAll(screen)
        elif self.gameState == "instructionState":
            self.instructionStateRedrawAll(screen)
        elif self.gameState == "pauseState":
            self.pauseStateRedrawAll(screen)
        elif self.gameState == "finalState":
            self.finalStateRedrawAll(screen)

####################################
# finalState 
####################################
    def finalStateKeyPressed(self, keyCode, mod):
        if keyCode == pygame.K_c:
            pass
        if keyCode == pygame.K_r:
            self.bossType1Number = 0
            self.advancedShooting = 0
            self.time = 0
            self.init()
            self.gameState = "startState"
        if keyCode == pygame.K_ESCAPE:
            self.playing = 0
    
    def finalStateMousePressed(self, x, y, button):
        pass
    
    def finalStateTimerFired(self, dt):
        if self.time == 100:
            x = random.randint(self.width//10, self.width*5//10)
            y = random.randint(self.height//10, self.height*9//10)
            character1 = FinalSceneCharacter1(x, y)
            self.finalSceneCharacters1.add(character1)
            x = random.randint(self.width*5//10, self.width*9//10)
            y = random.randint(self.height//10, self.height*9//10)
            character2 = FinalSceneCharacter2(x, y)
            self.finalSceneCharacters1.add(character1)
            self.finalSceneCharacters2.add(character2)
        self.finalSceneCharacters1.update(self.width, self.height)
        self.finalSceneCharacters2.update(self.width, self.height)
    
    def finalStateRedrawAll(self, screen):
        self.finalSceneCharacters1.draw(screen)
        self.finalSceneCharacters2.draw(screen)
        (msg, color) = ("Press 'r' to return to start menu", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*10//12)
        screen.blit(textSurf, textRect)
        (msg, color) = ("Press 'esc' to quit the game", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*11//12)
        screen.blit(textSurf, textRect)

####################################
# pauseState 
####################################
    def pauseStateKeyPressed(self, keyCode, mod):
        if keyCode == pygame.K_p:
            self.gameState = "gameState"
        if keyCode == pygame.K_r:
            self.time = 0
            self.init()
            self.gameState = "startState"
        
    
    def pauseStateMousePressed(self, x, y, button):
        pass
    
    def pauseStateTimerFired(self, dt):
        pass
    
    def pauseStateDrawText(self, screen):
        (msg, color) = ("Paused", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*3//8)
        screen.blit(textSurf, textRect)
        (msg, color) = ("Press 'p' again to play", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*4//8)
        screen.blit(textSurf, textRect)
        (msg, color) = ("Press 'r' to return to game menu", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*5//8)
        screen.blit(textSurf, textRect)
    
    def pauseStateRedrawAll(self, screen):
        self.pauseStateDrawText(screen)

####################################
# instructionState 
####################################
    def instructionStateKeyPressed(self, keyCode, mod):
        if keyCode == pygame.K_r:
            self.gameState = "startState"
    
    def instructionStateMousePressed(self, x, y, button):
        pass
    
    def instructionStateTimerFired(self, dt):
        pass
    
    def keyInstructionDrawText(self, screen):
        # need to add more instructions
        myfont = pygame.font.SysFont('Arial Rounded MT Bold', 28)
        textPlaySurface = myfont.render("Instructions", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*1//15))
        myfont = pygame.font.SysFont('Arial Rounded MT Bold', 24)
        textPlaySurface = myfont.render("Press up, down, left, right arrow keys to move the spaceship", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*2//15))
        textPlaySurface = myfont.render("Press spacekey to fire bullets", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*3//15))
        textPlaySurface = myfont.render(
        "Press 'd' to fire nuclear bomb", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*4//15))
        textPlaySurface = myfont.render(
        "Press 's' to shoot much more powerfully if you are in advanced shooting mode", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*5//15))
        textPlaySurface = myfont.render(
        "If you hit a red-cross, your HP will increase by 50", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*6//15))
        textPlaySurface = myfont.render(
        "If you hit a circle 'B', your number of bombs will increase by 1. Five is max num.", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*7//15))
        textPlaySurface = myfont.render(
        "If you hit a circle 'W', you will get advanced shooting weapon.", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*8//15))
        textPlaySurface = myfont.render(
        "Press 'p' to pause the game and press 'p' again to resume", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*9//15))
        textPlaySurface = myfont.render(
        "Press 'esc' to return to start menu if in game state and quit game if in start menu", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*10//15))
    
    def instructionStateDrawText(self, screen):
        myfont = pygame.font.SysFont('Arial Rounded MT Bold', 24)
        textPlaySurface = myfont.render("Press 'r' to return to start menu", 
        False, (224,255,255))
        screen.blit(textPlaySurface,(self.width//15,self.height*13//15))
        self.keyInstructionDrawText(screen)
    
    def instructionStateRedrawAll(self, screen):
        self.instructionStateDrawText(screen)

####################################
# startState 
####################################
    
    def startStateKeyPressed(self, keyCode, mod):
        if keyCode == pygame.K_1:
            self.time = 0
            self.mode = "one player mode"
            self.gameState = "gameState"  
        if keyCode == pygame.K_2:
            self.time = 0
            self.mode = "double player mode" 
            self.gameState = "gameState"  
        elif keyCode == pygame.K_i:
            self.gameState = "instructionState"
        elif keyCode == pygame.K_ESCAPE:
            self.playing = False
    
    def startStateMousePressed(self, x, y, button):
        pass
    
    def startStateTimerFired(self, dt):
        pass
    
    def startStateDrawText(self, screen):
        self.startMenuGroup.draw(screen)
        myfont = pygame.font.SysFont('Brush Script MT Italic', 50)
        # text game score
        textPlaySurface = myfont.render("Enter 112 Planet", False, (240, 255, 255))
        screen.blit(textPlaySurface,(self.width//3.1,self.height*3//8))
        (msg, color) = ("Press '1' to start one player mode", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*7//12)
        screen.blit(textSurf, textRect)
        (msg, color) = ("Press '2' to start double player mode", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*8//12)
        screen.blit(textSurf, textRect)
        (msg, color) = ("Press 'i' to read game instructions", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*9//12)
        screen.blit(textSurf, textRect)
        (msg, color) = ("Press 'esc' to exit this game", (224, 255, 255))
        textSurf, textRect = self.text_objects(msg, color)
        textRect.center = (self.width//2, self.height*10//12)
        screen.blit(textSurf, textRect)
    
    def startStateRedrawAll(self, screen):
        self.startStateDrawText(screen)

####################################
# endState 
####################################        
    def endStateKeyPressed(self, keyCode, mod):
        if keyCode == pygame.K_c:
            self.time = 0
            self.bossType1Number = 0
            self.advancedShooting = 0
            self.gameState = "gameState"
        
        if keyCode == pygame.K_r:
            self.time = 0
            self.bossType1Number = 0
            self.advancedShooting = 0
            self.init()
            self.gameState = "startState"
            
        
        if keyCode == pygame.K_e:
            if self.win == 1:
                self.time = 0
                newMusic = pygame.mixer.Sound('music/videoMusic.wav')
                self.changeBGMusic(newMusic)
                self.gameState = "finalState"
        
        if keyCode == pygame.K_ESCAPE:
            self.playing = 0
    
    def endStateMousePressed(self, x, y, button):
        pass
    
    def endStateTimerFired(self, dt):
        pass
    
    def endStateDrawText(self, screen):
        pass
    
    def endStateRedrawAll(self, screen):
        if self.win == None:
            (msg, color) = ("Congradulations!", (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*3//8)
            screen.blit(textSurf, textRect)
            if self.round == 2:
                (msg, color) = ("You collected 1st element >>> '1' of '112' !", 
                (224, 255, 255))
                textSurf, textRect = self.text_objects(msg, color)
                textRect.center = (self.width//2, self.height*4//8)
            elif self.round == 3:
                (msg, color) = ("You collected 2nd element >>> '1' of '112' !", 
                (224, 255, 255))
                textSurf, textRect = self.text_objects(msg, color)
                textRect.center = (self.width//2, self.height*4//8)
            elif self.round == 4:
                (msg, color) = ("You collected last element >>> '2' of '112' !", 
                (224, 255, 255))
                textSurf, textRect = self.text_objects(msg, color)
                textRect.center = (self.width//2, self.height*4//8)
            screen.blit(textSurf, textRect)
            if self.round == 4:
                (msg, color) = ("You won! Get prepared to land in 112 planet!", (224, 255, 255))
                textSurf, textRect = self.text_objects(msg, color)
                textRect.center = (self.width//2, self.height*5//8)
                screen.blit(textSurf, textRect)
                (msg, color) = ("You Scored %d" % (self.score) , (224, 255, 255))
                textSurf, textRect = self.text_objects(msg, color)
                textRect.center = (self.width//2, self.height*6//8)
                screen.blit(textSurf, textRect)
            (msg, color) = ("Press 'c' to continue playing ", (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*7//8)
            screen.blit(textSurf, textRect)
        elif self.win == 0:
            myfont = pygame.font.SysFont('Arial Rounded MT Bold', 50)
            # text game score
            textPlaySurface = myfont.render("You lost!", False, (224,255,255))
            screen.blit(textPlaySurface,(self.width//2.6,self.height*4//8))
            (msg, color) = ("Press 'r' to return to start menu", (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*10//12)
            screen.blit(textSurf, textRect)
            (msg, color) = ("Press 'esc' to quit game", (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*11//12)
            screen.blit(textSurf, textRect)
        elif self.win == 1 and self.thisPlayerAlive == 1:
            # msg = "weWon %d\n" % (1)
            # if (msg != ""):
            #     # print ("sending: ", msg)
            #     self.server.send(msg.encode())
            (msg, color) = ("You won! Get prepared to land in 112 planet!", (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*3//8)
            screen.blit(textSurf, textRect)
            (msg, color) = ("You Scored %d" % (self.score) , (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*4//8)
            screen.blit(textSurf, textRect)
            (msg, color) = ("Press 'e' to enter final scene", (224, 255, 255))
            textSurf, textRect = self.text_objects(msg, color)
            textRect.center = (self.width//2, self.height*5//8)
            screen.blit(textSurf, textRect)

####################################
# gameState 
#################################### 

    def gameStateMousePressed(self, x, y, button):
        # user can press left mouse button to fire bomb
        msg = ""
        if button == 1:
            if self.bombNums > 0:
                self.bombNums -= 1
                ship = self.shipGroup.sprites()[0]
                bomb = Bomb(ship.x, ship.y-ship.height//2-Bomb.size//2)
                self.playerBombs.add(bomb)
                msg = "OtherPlayerFiredBomb %d\n" % (1)
        if (msg != ""):
            # print ("sending: ", msg,)
            self.server.send(msg.encode())
                
    def gameStateMouseMotion(self, x, y):
        pass
        # mx, my, detectingR = x, y, 5
        # ship = self.shipGroup.sprites()[0]
        # sx, sy = int(ship.x), int(ship.y)
        # if abs(mx - sx) > detectingR:
        #     if mx < sx:
        #         ship.thrustX(-abs(mx-sx)*ship.power, self.width, self.height)
        #     elif mx > sx:
        #         ship.thrustX(abs(mx-sx)*ship.power, self.width, self.height)
        # if abs(my - sy) > detectingR:
        #     if my < sy:
        #         ship.thrustY(-abs(my-sy)*ship.power, self.width, self.height)
        #     elif my > sy:
        #         ship.thrustY(abs(my-sy)*ship.power, self.width, self.height)
        
    def gameStateKeyPressed(self, keyCode, mod):
        msg = ""
        if keyCode == pygame.K_p:
            self.gameState = "pauseState"
        # fire missle
        if keyCode == pygame.K_SPACE:
            ship = self.shipGroup.sprites()[0]
            bullet = Bullet(ship.x, ship.y-ship.height//2-Bullet.size//2)
            self.playerBullets.add(bullet)
            msg = "OtherPlayerFiredBullet %d\n" % (1)
        # another way to fire nuclear bomb by pressing key 'D'
        if keyCode == pygame.K_d:
            if self.bombNums > 0:
                self.bombNums -= 1
                ship = self.shipGroup.sprites()[0]
                bomb = Bomb(ship.x, ship.y-ship.height//2-Bomb.size//2)
                self.playerBombs.add(bomb)
                msg = "OtherPlayerFiredBomb %d\n" % (1)
        if keyCode == pygame.K_ESCAPE:
            self.gameState = "startState"
        if (msg != ""):
            # print ("sending: ", msg,)
            self.server.send(msg.encode())
            
    def checkCollision(self):
        if (self.mode == "one player mode"):
            for enemy in pygame.sprite.groupcollide(self.enemiesType3, 
            self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 5
                self.explosions.add(Explosion(enemy.x, enemy.y))
            for enemy in pygame.sprite.groupcollide(self.enemiesType3, 
            self.playerBullets, False, True, pygame.sprite.collide_circle):
            # self.channel2.play(self.explosionSound)
                self.explosions.add(Explosion(enemy.x, enemy.y))
                enemy.hp -= 10
                if enemy.hp < 0:
                    self.score += 3 # this is two players' total score 
                    self.enemiesType3.remove(enemy)

        msg = ""
        # check collision between type 1 enemies and spaceship bullets
        for enemy in pygame.sprite.groupcollide(self.enemiesType1, 
        self.playerBullets, False, True, pygame.sprite.collide_circle):
            # self.channel2.play(self.explosionSound)
            self.explosions.add(Explosion(enemy.x, enemy.y)) # this is two players' total score 
            enemy.hp -= 10
            if enemy.hp < 0:
                self.score += 2
                self.enemiesType1.remove(enemy)
        # check collision between type 1 enemies and other spaceship's bullets
        for playerName in self.otherPlayersBullets:
            for enemy in pygame.sprite.groupcollide(self.enemiesType1,
            self.otherPlayersBullets[playerName], False, True, 
            pygame.sprite.collide_circle):
                self.explosions.add(Explosion(enemy.x, enemy.y))
                enemy.hp -= 10
                if enemy.hp < 0:
                    self.score += 2
                    self.enemiesType1.remove(enemy)
               
        # check collison between type 2 enemies and spaceship bullets
        for enemy in pygame.sprite.groupcollide(self.enemiesType2, 
        self.playerBullets, False, True, pygame.sprite.collide_circle):
            # self.channel2.play(self.explosionSound)
            self.explosions.add(Explosion(enemy.x, enemy.y))
            enemy.hp -= 10
            if enemy.hp < 0:
                self.score += 4
                self.enemiesType2.remove(enemy)
        # check collisions between type 2 enemies and other spaceship's bullets
        for playerName in self.otherPlayersBullets:
            for enemy in pygame.sprite.groupcollide(self.enemiesType2,
            self.otherPlayersBullets[playerName], False, True,
            pygame.sprite.collide_circle):
                self.explosions.add(Explosion(enemy.x, enemy.y))
                enemy.hp -= 10
                if enemy.hp < 0:
                    self.score += 4
                    self.enemiesType2.remove(enemy)
                
        # check collision between spaceship and firstaid stations
        for firstAidStation in pygame.sprite.groupcollide(self.firstAidStations, 
        self.shipGroup, True, False, pygame.sprite.collide_circle):
            self.shipGroup.sprites()[0].hp += 50
            if self.shipGroup.sprites()[0].hp > 100:
                self.shipGroup.sprites()[0].hp = 100
        # check collisions between other spaceship and firstaid stations
        for playerName in self.otherSpaceships:
            for firstAidStation in pygame.sprite.groupcollide(self.firstAidStations,
            self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                self.otherSpaceships[playerName].sprites()[0].hp += 50
                if self.otherSpaceships[playerName].sprites()[0].hp > 100:
                    self.otherSpaceships[playerName].sprites()[0].hp = 100
                
        # check collision between spaceship and bomb supply stations
        for bombSupplyStation in pygame.sprite.groupcollide(self.bombSupplyStations, 
        self.shipGroup, True, False, pygame.sprite.collide_circle):
            self.bombNums += 1
            if self.bombNums > 5: self.bombNums = 5 # set limit to 5 for now
        # check collision between other spaceship and bomb supply stations
        for playerName in self.otherSpaceships:
            for bombSupplyStation in pygame.sprite.groupcollide(self.bombSupplyStations,
            self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                self.otherPlayersBombNumbers[playerName] += 1
                if self.otherPlayersBombNumbers[playerName] > 5:
                    self.otherPlayersBombNumbersp[playerName] = 5

        for weaponSupplyStation in pygame.sprite.groupcollide(self.weaponSupplyStations, 
        self.shipGroup, True, False, pygame.sprite.collide_circle):
            self.advancedShooting = 1

        # check collision between enemies and spaceship
        # type 1 enemies
        for enemy in pygame.sprite.groupcollide(self.enemiesType1, 
        self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 10
                self.explosions.add(Explosion(enemy.x, enemy.y))
        # type 2 enemies
        for enemy in pygame.sprite.groupcollide(self.enemiesType2, 
        self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 10
                self.explosions.add(Explosion(enemy.x, enemy.y))
        # check collisions between enemies and other spaceships
        # type 1 enemies
        for playerName in self.otherSpaceships:
            for enemy in pygame.sprite.groupcollide(self.enemiesType1,
            self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                otherShip = self.otherSpaceships[playerName].sprites()[0]
                self.explosions.add(Explosion(enemy.x, enemy.y))
        # type 2 enemies
        for playerName in self.otherSpaceships:
            for enemy in pygame.sprite.groupcollide(self.enemiesType2,
            self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                otherShip = self.otherSpaceships[playerName].sprites()[0]
                self.explosions.add(Explosion(enemy.x, enemy.y))
                        
        # check collision between type 2 enemies' bullets and spaceship
        for enemy in self.enemiesType2:
            for bullet in pygame.sprite.groupcollide(enemy.bullets, 
            self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 5
                self.explosions.add(Explosion(bullet.x, bullet.y))
        for playerName in self.otherSpaceships:
            for enemy in self.enemiesType2:
                for bullet in pygame.sprite.groupcollide(enemy.bullets, 
                self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                    otherShip = self.otherSpaceships[playerName].sprites()[0]
                    self.explosions.add(Explosion(bullet.x, bullet.y))
                
        # check collision between enemy base station bullets and spacehsip
        for station in self.enemyStations:
            for bullet in pygame.sprite.groupcollide(station.bullets, 
            self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 5
                self.explosions.add(Explosion(bullet.x, bullet.y))
        # check collision between enemy base station bullets and other spacehsip
        for playerName in self.otherSpaceships:
            for station in self.enemyStations:
                for bullet in pygame.sprite.groupcollide(station.bullets, 
                self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                    otherShip = self.otherSpaceships[playerName].sprites()[0]
                    self.explosions.add(Explosion(bullet.x, bullet.y))
                
        # check collision between type 1 boss's bullets, missles and spaceship
        for boss in self.bossType1Group:
            for bullet in pygame.sprite.groupcollide(boss.pattern1Bullets, 
            self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 2
                self.explosions.add(Explosion(bullet.x, bullet.y))
            for bullet in pygame.sprite.groupcollide(boss.pattern2Bullets, 
            self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 2
                self.explosions.add(Explosion(bullet.x, bullet.y))
            for missle in pygame.sprite.groupcollide(boss.missles, 
            self.shipGroup, True, False, pygame.sprite.collide_circle):
                self.shipGroup.sprites()[0].hp -= 5
                self.explosions.add(Explosion(missle.x, missle.y))
        # check collision between type 1 boss's bullets, missles and other spaceship
        for playerName in self.otherSpaceships:
                for boss in self.bossType1Group:
                    for bullet in pygame.sprite.groupcollide(boss.pattern1Bullets, 
                    self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                        otherShip = self.otherSpaceships[playerName].sprites()[0]
                        self.explosions.add(Explosion(bullet.x, bullet.y))
                    for bullet in pygame.sprite.groupcollide(boss.pattern2Bullets, 
                    self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                        otherShip = self.otherSpaceships[playerName].sprites()[0]
                        self.explosions.add(Explosion(bullet.x, bullet.y))
                    for missle in pygame.sprite.groupcollide(boss.missles, 
                    self.otherSpaceships[playerName], True, False, pygame.sprite.collide_circle):
                        otherShip = self.otherSpaceships[playerName].sprites()[0]
                        self.explosions.add(Explosion(missle.x, missle.y))

        # check collision between spaceship bullets and boss type 1
        for bullet in pygame.sprite.groupcollide(
        self.playerBullets, 
        self.bossType1Group, True, False, pygame.sprite.collide_circle):
            self.explosions.add(Explosion(bullet.x, bullet.y))
            boss.hp -= 5
            msg = "BossDamage %d\n" % (5)
            self.server.send(msg.encode())
            if (boss.hp < 0):
                if self.mode == "double player mode":
                    self.win = 1
                    self.score += 100
                    self.bossType1Group.empty()
                    # self.changeBGMusic()
                    self.gameState = "endState"
                elif self.mode == "one player mode":
                    # print("game round = ", self.round)
                    self.round += 1
                    self.score += 100
                    self.bossType1Group.empty()
                    self.bossType1Number = 0
                    self.gameState = "endState"
                    if (self.round == 4):
                        self.win = 1 
                        # self.changeBGMusic()
                        self.gameState = "endState"
        # check collision between other spaceship bullets and boss type 1
        for playerName in self.otherPlayersBullets:
            for bullet in pygame.sprite.groupcollide(
            self.otherPlayersBullets[playerName],
            self.bossType1Group, True, False, pygame.sprite.collide_circle):
                self.explosions.add(Explosion(bullet.x, bullet.y))
                                  
    def moveMisslesAI(self, dt):
        for boss in self.bossType1Group:
            boss.loadMissles(dt, self.width, self.height, self.mode)
            if self.gameState == "in boss fight":
                if self.mode == "one player mode":
                    ship = self.shipGroup.sprites()[0]
                    targetX, targetY = ship.x, ship.y
                    missle = boss.missles.sprites()[0]
                    missleX, missleY = missle.x, missle.y
                    vx, vy = targetX - missleX, targetY - missleY
                    missle.velocity = vx//20, vy//20
                    # missle.angle = math.atan2(vy//20, vx//20)
                    missle.enemyMissleUpdate(self.width, self.height)
                elif self.mode == "double player mode":
                    ship0 = self.allPlayers.sprites()[0]
                    ship1 = self.allPlayers.sprites()[1]
                    missle0 = boss.missles.sprites()[0]
                    missle1 = boss.missles.sprites()[1]
                    targetX0, targetY0 = ship0.x, ship0.y
                    targetX1, targetY1 = ship1.x, ship1.y
                    missleX0, missleY0 = missle0.x, missle0.y
                    missleX1, missleY1 = missle1.x, missle1.y
                    vx0, vy0 = targetX0 - missleX0, targetY0 - missleY0
                    vx1, vy1 = targetX1 - missleX1, targetY1 - missleY1
                    missle0.velocity = vx0//20, vy0//20
                    missle1.velocity = vx1//20, vy1//20
                    # missle.angle = math.atan2(vy//20, vx//20)
                    missle0.enemyMissleUpdate(self.width, self.height)
                    missle1.enemyMissleUpdate(self.width, self.height)
            
    def enemyUpdate(self, dt):
        if (self.mode == "one player mode"):
            for enemy in self.enemiesType3:
                ship = self.shipGroup.sprites()[0]
                if (enemy.timeAlive > 20):
                    vx, vy = enemy.velocity
                    vx = (ship.x - enemy.x)/50
                    enemy.velocity = vx, vy
                enemy.update(self.width, self.height)
        elif (self.mode == "double player mode"):
            for enemy in self.enemiesType3:
                enemy.update(self.width, self.height)
        # update type 1 enemies
        for enemy in self.enemiesType1:
            enemy.update(self.width, self.height)
        # update type 2 enemies
        for enemy in self.enemiesType2:
            # add bullet to a type 2 enemy every 100 time units
            if self.time % 100 == 0:
                bullet = EnemyBullet(enemy.x, enemy.y+enemy.height//2+EnemyBullet.size//2)
                enemy.bullets.add(bullet)
                self.enemyBullets.add(bullet)   
            enemy.update(self.width, self.height)
        for station in self.enemyStations:
            if self.time % 50 == 0:
                station.loadBullets(dt, self.width, self.height)
            station.moveBulletsInPattern(dt, self.width, self.height)
        for boss in self.bossType1Group:
            boss.update(dt, self.width, self.height)
            # print("boss timeAlive = ", boss.timeAlive)
            if boss.timeAlive == 85:
                msg = "EneterBossState1 %d\n" % (1)
                self.server.send(msg.encode())
                boss.enterBossState1(dt, self.width, self.height)
                self.gameState = "in boss fight"
                # print("debug boss state 1 velocity = ", boss.velocity)
            if self.gameState == "in boss fight":
                # need to clear other types of enemies
                # boss has three different shootining patterns
                # pattern 1: two bullets shooting
                # pattern 2: bullets shooting in circle
                # pattern 3: AI missles tracking
                if (len(boss.pattern1Bullets) == 0):
                    boss.loadPattern1Bullets(dt, self.width, self.height)
                if (len(boss.pattern2Bullets) == 0):
                    boss.loadPattern2Bullets(dt, self.width, self.height)
                if (not bool(boss.missles)):
                    boss.loadMissles(dt, self.width, self.height, self.mode)
                
                self.enemiesType1.empty()
                self.enemiesType2.empty()
                self.enemiesType3.empty()

                if (bool(self.playerBullets)):
                    vx, vy = boss.velocity
                    closetBullet = None
                    closetDis = 100000
                    for bullet in self.playerBullets:
                        if math.sqrt((bullet.x - boss.x)*(bullet.x - boss.x) + (bullet.y - boss.y)*(bullet.y - boss.y))\
                         < closetDis:
                            # print("here")
                            closetDis = math.sqrt((bullet.x - boss.x)*(bullet.x - boss.x) + (bullet.y - boss.y)*(bullet.y - boss.y))
                            closetBullet = bullet
                    if (abs(boss.x - closetBullet.x) < 60):
                        if boss.x < closetBullet.x:
                            vx = -(60 - abs(boss.x - closetBullet.x))*1.75
                            # print("boss vx" , vx)
                            boss.velocity = (vx, vy)
                        else:
                            vx = (60 - abs(boss.x - closetBullet.x))*1.75
                            # print("boss vx" , vx)
                            boss.velocity = (vx, vy)
                        msg = "BossMoved %d\n" % (vx)
                        self.server.send(msg.encode())
                    else:
                        vx = 0
                        boss.velocity = (vx, vy)
                        msg = "BossMoved %d\n" % (int(vx))
                        self.server.send(msg.encode())
                
                boss.moveBulletsInPattern1(dt, self.width, self.height)
                boss.moveBulletsInPattern2(dt, self.width, self.height)
                self.moveMisslesAI(dt)
                if (bool(boss.missles)):
                    if (boss.missles.sprites()[0].missleTimeAlive == 500):
                        self.explosions.add(Explosion(boss.missles.sprites()[0].x, 
                        boss.missles.sprites()[0].y))
    
    
    def generateRandomGameObjects(self, dt):
        msg = ""
        if self.time % 500 == 0:
            x = random.randint(self.width*6//8, self.width*7//8)
            y = 0
            self.enemiesType3.add(EnemyType3(x, y, self.round))
            msg = "GenerateEnemyType3 %d %d %d\n" % (x, y, self.round)
            self.server.send(msg.encode())
        # add enemy type 1 to screen every 100 time units
        if self.time % 100 == 0:
            x = random.randint(self.width//8, self.width*7//8)
            y = 0 
            self.enemiesType1.add(EnemyType1(x, y, self.round))
            msg = "GenerateEnemyType1 %d %d %d\n" % (x, y, self.round)
            self.server.send(msg.encode())
        # add enemy type 2 to screen every 100 time units
        if self.time % 100 == 0:
            x = random.randint(self.width//8, self.width*7//8)
            y = 0 
            self.enemiesType2.add(EnemyType2(x, y, self.round))
            msg = "GenerateEnemyType2 %d %d %d\n" % (x, y, self.round)
            self.server.send(msg.encode())
        if self.time % 500 == 0:  # 10 for testing, 500 for real game  
            x = random.randint(self.width//8, self.width*7//8)
            y = 0 
            self.firstAidStations.add(FirstAidStation(x, y))
            msg = "GenerateFirstAidStation %d %d\n" % (x, y)
            self.server.send(msg.encode())
        if self.time % 800 == 0:  # 10 for testing, 500 for real game  
            x = random.randint(self.width//8, self.width*7//8)
            y = 0 
            self.weaponSupplyStations.add(WeaponSupplyStation(x, y))
            msg = "GenerateWeaponSupplyStation %d %d\n" % (x, y)
            self.server.send(msg.encode())
        if self.time % 600 == 0:  # 10 for testing, 500 for real game   
            x = random.randint(self.width//8, self.width*7//8)
            y = 0
            self.bombSupplyStations.add(BombSupplyStation(x, y))
            msg = "GenerateBombSupplyStation %d %d\n" % (x, y)
            self.server.send(msg.encode())
        # add enemy base station to screen every 500 time units
        if self.time % 750 == 0: # 100 for testing 1000 for real game
            x = random.randint(self.width*6//8, self.width*7//8)
            y = 0 
            self.enemyStations.add(EnemyStation(x, y))
            msg = "GenerateEnemyStation %d %d\n" % (x, y)
            self.server.send(msg.encode())
        # print("self.time = ", self.time)
        # add boss into the game
        if self.time % 1500 == 0: # 1000 for testing, 2000 for real game
            print("generate a boss", "This round is", self.round, "bossNum is", self.bossType1Number)
            x = self.width//2
            y = 0 
            msg = "GenerateBoss %d %d\n" % (x, y)
            self.server.send(msg.encode())
            if (self.bossType1Number < 1):
                boss1 = BossType1(self.round, x, y)
                self.bossType1Group.add(boss1)
                # print("add a boss", end = ' ')
                # print(self.bossType1Group)
                self.bossType1Number += 1
        # if (msg != ""):
            # print ("sending: ", msg,)
            # self.server.send(msg.encode())
                        
    def gameStateTimerFired(self, dt):
        ship = self.shipGroup.sprites()[0]
        if self.isKeyPressed(pygame.K_LEFT):
            ship.thrustX(-ship.power, self.width, self.height)
        if self.isKeyPressed(pygame.K_RIGHT):
            ship.thrustX(+ship.power, self.width, self.height)
        if self.isKeyPressed(pygame.K_UP):
            ship.thrustY(-ship.power, self.width, self.height)
        if self.isKeyPressed(pygame.K_DOWN):
            ship.thrustY(+ship.power, self.width, self.height)
        if self.isKeyPressed(pygame.K_s):
            if self.advancedShooting == 1:
                bullet = Bullet(ship.x, ship.y-ship.height//2-Bullet.size//2)
                self.playerBullets.add(bullet)
                # print("spacekey number is", pygame.K_s)
            # msg = "OtherPlayerFiredBullet %d\n" % (1)

        # print("self.currentOtherPlayer is ", self.currentOtherPlayer)
        # Handle key inputs from other players
        # When other players move spceship by keys, '276' left '275' right '273' up '274' down
        if self.currentOtherPlayer != "":
            # print("this other player keys dict is ", self.otherPlayersKeys[self.currentOtherPlayer])
            if self.otherPlayersKeys[self.currentOtherPlayer].get('276', False):
                ship = self.otherSpaceships[self.currentOtherPlayer].sprites()[0]
                # print("other ship x is", ship.x)
                ship.thrustX(-ship.power, self.width, self.height)
            if self.otherPlayersKeys[self.currentOtherPlayer].get('275', False):
                ship = self.otherSpaceships[self.currentOtherPlayer].sprites()[0]
                ship.thrustX(+ship.power, self.width, self.height)
            if self.otherPlayersKeys[self.currentOtherPlayer].get('273', False):
                ship = self.otherSpaceships[self.currentOtherPlayer].sprites()[0]
                ship.thrustY(-ship.power, self.width, self.height)
            if self.otherPlayersKeys[self.currentOtherPlayer].get('274', False):
                ship = self.otherSpaceships[self.currentOtherPlayer].sprites()[0]
                ship.thrustY(+ship.power, self.width, self.height)
            if self.otherPlayersKeys[self.currentOtherPlayer].get('115', False):
                ship = self.otherSpaceships[self.currentOtherPlayer].sprites()[0]
                bullet = Bullet(ship.x, ship.y-ship.height//2-Bullet.size//2)
                self.otherPlayersBullets[self.currentOtherPlayer].add(bullet)

        # check if other spacship's hp is less than 0
        for playerName in self.otherSpaceships:
            self.otherSpaceships[playerName].update(self.isKeyPressed, self.width, self.height)
            if bool(self.otherSpaceships[playerName]):
                if self.otherSpaceships[playerName].sprites()[0].hp < 0:
                    # print("%s is out of game!" % (playerName))
                    if playerName in self.otherSpaceships:
                        self.otherSpaceships[playerName].empty()

        self.shipGroup.update(self.isKeyPressed, self.width, self.height)
        # check if spaceship's hp is less than 0
        if self.shipGroup.sprites()[0].hp < 0: 
            if self.mode == "one player mode":
                self.win = 0
                self.gameState = "endState"
            elif self.mode == "double player mode":
                self.thisPlayerAlive = 0
                self.win = 0
                msg = "PlayerOut %d\n" % (1)
                self.server.send(msg.encode())
                self.gameState = "endState"

        self.playerBullets.update(self.width, self.height)
        for playerName in self.otherPlayersBullets:
            self.otherPlayersBullets[playerName].update(self.width, self.height)
        self.playerBombs.update(dt, self.width, self.height)
        for playerName in self.otherPlayersBombs:
            self.otherPlayersBombs[playerName].update(dt, self.width, self.height)
            if (bool(self.otherPlayersBombs[playerName])):
                for bomb in self.otherPlayersBombs[playerName]:
                    if bomb.isExploded():
                        self.explosions.add(Explosion(bomb.x, bomb.y))
                        bomb.kill()
                        for enemy in self.enemiesType1:
                            self.explosions.add(Explosion(enemy.x, enemy.y))
                        self.enemiesType1.empty()
                        for enemy in self.enemiesType2:
                            self.explosions.add(Explosion(enemy.x, enemy.y))
                        self.enemiesType2.empty()


        # check player bomb explosion
        if (bool(self.playerBombs)):
            for bomb in self.playerBombs:
                if bomb.isExploded():
                    self.explosions.add(Explosion(bomb.x, bomb.y))
                    bomb.kill()
                    for enemy in self.enemiesType1:
                        self.explosions.add(Explosion(enemy.x, enemy.y))
                    self.enemiesType1.empty()
                    for enemy in self.enemiesType2:
                        self.explosions.add(Explosion(enemy.x, enemy.y))
                    self.enemiesType2.empty()
                    for enemy in self.enemiesType3:
                        self.explosions.add(Explosion(enemy.x, enemy.y))
                    self.enemiesType3.empty()
        
        # print(self.numPlayers)
        if (self.mode == "double player mode"):
            if (self.numPlayers == 2):
                random.seed(self.time)
                self.generateRandomGameObjects(dt)
        elif (self.mode == "one player mode"):
            # if self.round == 1: random.seed(1)
            # elif self.round == 2: random.seed(2)
            # elif self.round == 3: random.seed(3)
            self.generateRandomGameObjects(dt)
        
        self.enemyUpdate(dt)

        self.enemyStations.update(dt, self.width, self.height)   
        self.firstAidStations.update(dt, self.width, self.height)
        self.bombSupplyStations.update(dt, self.width, self.height)
        self.weaponSupplyStations.update(dt, self.width, self.height)

        self.checkCollision()

        self.explosions.update(dt) 
                 
    def gameStateDrawText(self, screen):
        myfont = pygame.font.SysFont('Arial Rounded MT Bold', 28)
        # text game score
        textScoreSurface = myfont.render('Score %d'%(self.score), False, (224,255,255))
        screen.blit(textScoreSurface,(5,5))
        # text game round
        textRoundSurface = myfont.render('Round %d'%(self.round), False, (224,255,255))
        screen.blit(textRoundSurface,(self.width//2-30,5))
        # text spaceship health
        textRoundSurface = myfont.render('HP', False, (224,255,255))
        screen.blit(textRoundSurface,(self.width*4//5-30,self.height - self.height//15))
    
    def gameStateDrawHowManyBombs(self, screen):
        myfont = pygame.font.SysFont('Arial Rounded MT Bold', 28)
        # text game score
        textBombSurface = myfont.render('Bombs x %d'%(self.bombNums), 
        False, (224,255,255))
        screen.blit(textBombSurface,(5,self.height - self.height//15))
    
    def gameStateRedrawAll(self, screen):      
        if self.gameState == "gameState" or self.gameState == "in boss fight":
            # draw first aid stations and bomb supply stations
            self.enemyStations.draw(screen)
            self.firstAidStations.draw(screen)
            self.bombSupplyStations.draw(screen)
            for station in self.bombSupplyStations:
                myfont = pygame.font.SysFont('Arial Rounded MT Bold', 24)
                textBombSurface = myfont.render('B', False, (224,255,255))
                screen.blit(textBombSurface,
                (station.x-station.size//1.45,station.y-station.size//1.45))
            self.weaponSupplyStations.draw(screen)
            for station in self.weaponSupplyStations:
                myfont = pygame.font.SysFont('Arial Rounded MT Bold', 24)
                textBombSurface = myfont.render('W', False, (224,255,255))
                screen.blit(textBombSurface,
                (station.x-station.size//1.4,station.y-station.size//1.45))
                
            # draw type 1 and type 2 enemies
            self.enemiesType1.draw(screen)
            self.enemiesType2.draw(screen)
            self.enemiesType3.draw(screen)
                
            # draw enemy type 2 bullets
            for enemy in self.enemiesType2:
                enemy.bullets.draw(screen)

            # draw spaceships
            self.shipGroup.draw(screen)
            self.playerBullets.draw(screen)
            self.playerBombs.draw(screen)
            # draw other spaceships
            for playerName in self.otherSpaceships:
                self.otherSpaceships[playerName].draw(screen)
                self.otherPlayersBullets[playerName].draw(screen)
                self.otherPlayersBombs[playerName].draw(screen)
            
            # draw enemy base station bullets
            for station in self.enemyStations:
                station.bullets.draw(screen)
                    
            #  draw type 1 boss and its bullets, missles
            self.bossType1Group.draw(screen)
            for boss in self.bossType1Group:
                # print("pattern1 bullets ", boss.pattern1Bullets)
                if (len(boss.pattern1Bullets) == 10):
                    boss.pattern1Bullets.draw(screen)
                    boss.pattern2Bullets.draw(screen) 
                    boss.missles.draw(screen)

            self.explosions.draw(screen)

            # draw HP bar
            hpBarWid = self.shipGroup.sprites()[0].hp
            if hpBarWid < 0: hpBarWid = 0
            pygame.draw.rect(screen,(0,255,255),(self.width*4//5,
                                self.height - self.height//15,
                                hpBarWid, 20), 0)
            # draw text
            self.gameStateDrawText(screen)
            # draw how many bombs
            self.gameStateDrawHowManyBombs(screen)


serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()            
Game(750, 750).run(serverMsg, server)
