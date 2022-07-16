import pygame
import math
from GameObject import GameObject

class BossMissle(GameObject):
    speed = 25
    time = 50 # last 1 second, 50*0.02 = 1s
    size = 20
    missleLifeTime = 500

    @staticmethod
    def init():
        BossMissle.image = pygame.image.load('images/bossmisslerot.png').convert_alpha()
        
        # pygame.transform.rotate(pygame.transform.scale(
        #              pygame.image.load('images/bossmissle.png').convert_alpha(),
        #              (15, 100)), -90) 
    
    def __init__(self, x, y):
        self.bombPrepTime = 30
        self.missleTimeAlive = 0
        self.angleSpeed = 30
        factor = 0.05
        
        w, h = BossMissle.image.get_size()
        image = pygame.transform.scale(BossMissle.image, 
        (int(w * factor), int(h * factor)))
        image = pygame.transform.rotate(image, -90)
        super().__init__(x, y, image, max(w, h) / 2 * factor)
        vx = 0
        vy = 0
        self.velocity = vx, vy
        
    def update(self, dt, screenWidth, screenHeight):
        self.timeAlive += 1
        super().update(screenWidth, screenHeight)
        
    def initEnemyBaseBulletVelocity(self, angle):
        vx = BossMissle.speed * math.cos(math.radians(angle))
        vy = BossMissle.speed * math.sin(math.radians(angle))
        self.velocity = (vx, vy)    
        
    def enemyMissleUpdate(self, screenWidth, screenHeight):
        self.missleTimeAlive += 1
        self.angle += self.angleSpeed
        super().update(screenWidth, screenHeight)

        if self.missleTimeAlive > BossMissle.missleLifeTime:
            print("kill missle here")
            self.kill()

    def isExploded(self):
        return self.timeAlive > self.bombPrepTime