import pygame
import math
from GameObject import GameObject

class Bullet(GameObject):
    speed = 25
    lifeTime = 200 
    size = 10

    def __init__(self, x, y):
        self.timeAlive = 0
                
        size = Bullet.size
        
        image = pygame.Surface((Bullet.size, Bullet.size), pygame.SRCALPHA)
        circle = pygame.draw.circle(image, (0, 255, 255), 
                 (size//2, size//2), size // 2)
                 
        super().__init__(x, y, image, size // 2)
        
        vx = Bullet.speed * math.cos(math.radians(90)) 
        # could change shooting pattern by tracking spaceship vx
        vy = -Bullet.speed * math.sin(math.radians(90))
        self.velocity = vx, vy

    def update(self, screenWidth, screenHeight):
        self.timeAlive += 1
        
        super().update(screenWidth, screenHeight)

        if self.timeAlive > Bullet.lifeTime:
            self.kill()