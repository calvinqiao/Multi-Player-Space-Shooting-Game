import pygame, random
import math
from GameObject import GameObject
from EnemyBullet import EnemyBullet

class EnemyType2(GameObject):
    minSize = 8
    maxSize = 10
    minSpeed = 2
    maxSpeed = 2
    lifeTime = 500  

    @staticmethod
    def init():
        EnemyType2.images = []
        EnemyType2.imageType1 = \
        pygame.image.load('images/enemy2.png').convert_alpha()
        EnemyType2.images.append(EnemyType2.imageType1)
        EnemyType2.imageType2 = \
        pygame.image.load('images/enemy2.png').convert_alpha()
        EnemyType2.images.append(EnemyType2.imageType2)

                
    def __init__(self, x, y, round, level=None):
        self.timeAlive = 0
        self.directionChange = -1
        if round == 1:
            self.hp = 20
        elif round == 2:
            self.hp = 30
        elif round == 3:
            self.hp = 40 # 10 for tesing
        
        if level is None:
            level = random.randint(EnemyType2.minSize, EnemyType2.maxSize)
        self.level = level # different enemy levels
        factor = 1
        
        image = random.choice(EnemyType2.images)
        w, h = image.get_size()
        EnemyType2.image = pygame.transform.rotate(
                           pygame.transform.scale
                           (image, 
                           (int(w * factor), int(h * factor))
                           ), 180)
        super().__init__(x, y, image, max(w, h) / 2 * factor)
        
        vx = 1 
        vy = random.randint(EnemyType2.maxSpeed, EnemyType2.maxSpeed)
        self.velocity = vx, vy        

        self.bullets = pygame.sprite.Group()

    def update(self, screenWidth, screenHeight):
        self.timeAlive += 1
        if (self.timeAlive % 50 == 0):
            # print("drift")
            vx, vy = self.velocity 
            vx = vx *  self.directionChange
            self.velocity = vx, vy 
            
        super().update(screenWidth, screenHeight)
        for bullet in self.bullets:
            bullet.update(screenWidth, screenHeight)
            
        if self.timeAlive > EnemyType2.lifeTime:
            self.kill()
    