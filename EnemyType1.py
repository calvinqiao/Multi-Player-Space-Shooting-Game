import pygame, random
import math
from GameObject import GameObject

class EnemyType1(GameObject):
    minSize = 8
    maxSize = 10
    minSpeed = 3
    maxSpeed = 3
    lifeTime = 500  

    @staticmethod
    def init():
        EnemyType1.image = \
        pygame.image.load('images/enemy1.png').convert_alpha()
                
    def __init__(self, x, y, round, level=None):
        self.timeAlive = 0
        if round == 1:
            self.hp = 10
        elif round == 2:
            self.hp = 20
        elif round == 3:
            self.hp = 30 # 10 for tesing
                
        if level is None:
            level = random.randint(EnemyType1.minSize, EnemyType1.maxSize)
        self.level = level # different enemy levels
        factor = 1
        
        w, h = EnemyType1.image.get_size()
        EnemyType1.image = pygame.transform.rotate(
                           pygame.transform.scale
                           (EnemyType1.image, 
                           (int(w * factor), int(h * factor))
                           ), 180)
        super().__init__(x, y, EnemyType1.image, max(w, h) / 2 * factor)
        
        vx = 0 
        vy = random.randint(EnemyType1.maxSpeed, EnemyType1.maxSpeed)
        self.velocity = vx, vy        
    
    def update(self, screenWidth, screenHeight):
        self.timeAlive += 1
        
        super().update(screenWidth, screenHeight)
        
        if self.timeAlive > EnemyType1.lifeTime:
            self.kill()