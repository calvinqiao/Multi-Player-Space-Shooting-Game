import pygame, random
import math
from GameObject import GameObject
from EnemyBullet import EnemyBullet

class EnemyType3(GameObject):
    minSize = 8
    maxSize = 10
    minSpeed = 5
    maxSpeed = 8
    lifeTime = 500  

    @staticmethod
    def init():
        EnemyType3.image = \
        pygame.image.load('images/enemy3.png').convert_alpha()

                
    def __init__(self, x, y, round, level=None):
        self.timeAlive = 0
        self.directionChange = -1
        if round == 1:
            self.hp = 10
        elif round == 2:
            self.hp = 20
        elif round == 3:
            self.hp = 30 # 10 for tesing
        
        if level is None:
            level = random.randint(EnemyType3.minSize, EnemyType3.maxSize)
        self.level = level # different enemy levels
        factor = 0.8
        
        image = EnemyType3.image
        w, h = image.get_size()
        image = pygame.transform.rotate(
                           pygame.transform.scale
                           (image, 
                           (int(w * factor), int(h * factor))
                           ), 180)
        super().__init__(x, y, image, max(w, h) / 2 * factor)
        
        vx = -3
        vy = random.randint(EnemyType3.minSpeed, EnemyType3.maxSpeed)
        self.velocity = vx, vy        

        self.bullets = pygame.sprite.Group()

    def update(self, screenWidth, screenHeight):
        self.timeAlive += 1
            
        super().update(screenWidth, screenHeight)
        for bullet in self.bullets:
            bullet.update(screenWidth, screenHeight)
            
        if self.timeAlive > EnemyType3.lifeTime:
            self.kill()
    