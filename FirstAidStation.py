import pygame, random
import math
from GameObject import GameObject

class FirstAidStation(GameObject):
    minSize = 8
    maxSize = 10
    minSpeed = 1
    maxSpeed = 1
    lifeTime = 500  

    @staticmethod
    def init():
        FirstAidStation.image = \
        pygame.image.load('images/firstAid.png').convert_alpha()
                
    def __init__(self, x, y, level=None):
        self.timeAlive = 0
                
        factor = 0.04
        
        w, h = FirstAidStation.image.get_size()
        image = pygame.transform.scale(FirstAidStation.image, 
        (int(w * factor), int(h * factor)))
        super().__init__(x, y, image, max(w, h) / 2 * factor)
        
        vx = 0 
        vy = 1
        self.velocity = vx, vy        
    
    def update(self, dt, screenWidth, screenHeight):
        self.timeAlive += 1
        
        super().update(screenWidth, screenHeight)
        
        if self.timeAlive > FirstAidStation.lifeTime:
            self.kill()