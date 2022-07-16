import pygame, random
import math
from GameObject import GameObject

class BombSupplyStation(GameObject):
    speed = 1
    lifeTime = 500 
    size = 10
                
    def __init__(self, x, y, level=None):
        self.timeAlive = 0
        size  = BombSupplyStation.size
        
        image = pygame.Surface((size*2, size*2), 
        pygame.SRCALPHA)
        circle = pygame.draw.circle(image, (128, 0, 128), 
                 (size, size), size)
        super().__init__(x, y, image, size)
        
        vx = 0 
        vy = 1
        self.velocity = vx, vy        
    
    def update(self, dt, screenWidth, screenHeight):
        self.timeAlive += 1
        
        super().update(screenWidth, screenHeight)
        
        if self.timeAlive > BombSupplyStation.lifeTime:
            self.kill()