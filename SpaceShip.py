import pygame
import math
from GameObject import GameObject

class SpaceShip(GameObject):
    Round1Distance = 5000
    
    @staticmethod
    def init():
        SpaceShip.shipImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/xspr5.png').convert_alpha(),
            (40, 80)), 0)  

    def __init__(self, PID, x, y):
        super().__init__(x, y, SpaceShip.shipImage, 30)
        
        self.PID = PID
        self.hp = 100
        self.power = 1
        self.drag = 0.9
        self.maxSpeed = 15
        self.disTravelled = 0

    def update(self, keysDown, screenWidth, screenHeight):
        self.disTravelled += 1
        
        # if keysDown(pygame.K_LEFT):
        #     self.thrustX(-self.power, screenWidth, screenHeight)
        # if keysDown(pygame.K_RIGHT):
        #     self.thrustX(+self.power, screenWidth, screenHeight)
        # if keysDown(pygame.K_UP):
        #     self.thrustY(-self.power, screenWidth, screenHeight)
        # if keysDown(pygame.K_DOWN):
        #     self.thrustY(+self.power, screenWidth, screenHeight)
        # else:
        vx, vy = self.velocity
        self.velocity = self.drag * vx, self.drag * vy
            
        super().update(screenWidth, screenHeight)
        if self.x < 0:        
            self.x = screenWidth - self.width//2
        if self.x > screenWidth:
            self.x = self.width//2
        if self.y > screenHeight - self.height//1.5: 
            self.y = screenHeight - self.height//1.5
        # print("In update ", vy)
        
    def thrustX(self, power, screenWidth, screenHeight):
        vx, vy = self.velocity
        vx += power
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed > self.maxSpeed:
            factor = self.maxSpeed / speed
            vx *= factor
            vy *= factor
        self.velocity = (vx, vy)
    
    def thrustY(self, power, screenWidth, screenHeight):
        vx, vy = self.velocity
        vy += power 
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed > self.maxSpeed:
            factor = self.maxSpeed / speed
            vx *= factor
            vy *= factor
        self.velocity = (vx, vy)      

    def changePID(self, PID):
        self.PID = PID      