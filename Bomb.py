import pygame
import math
from GameObject import GameObject

class Bomb(GameObject):
    speed = 1
    time = 50 # last 1 second, 50*0.02 = 1s
    size = 20

    @staticmethod
    def init():
        Bomb.image = pygame.transform.rotate(pygame.transform.scale(
                     pygame.image.load('images/bomb.png').convert_alpha(),
                     (20, 40)), 180) 
    
    def __init__(self, x, y):
        self.bombPrepTime = 30
        self.timeAlive = 0
        
        size = Bomb.size
        super().__init__(x, y, Bomb.image, size // 2)
        vx = Bomb.speed * math.cos(math.radians(90))
        vy = -Bomb.speed * math.sin(math.radians(90))
        self.velocity = vx, vy
        
    def update(self, dt, screenWidth, screenHeight):
        self.timeAlive += 1
        super().update(screenWidth, screenHeight)

    def isExploded(self):
        return self.timeAlive > self.bombPrepTime