import pygame, random
import math
from GameObject import GameObject
from EnemyBullet import EnemyBullet

class EnemyStation(GameObject):
    minSize = 10
    maxSize = 10
    minSpeed = 1
    maxSpeed = 1
    lifeTime = 1000  # last 1 second, 250*0.02 = 5s 

    @staticmethod
    def init():
        EnemyStation.image = \
        pygame.image.load('images/mainbase.png').convert_alpha()
        EnemyStation.image = pygame.transform.rotate(EnemyStation.image, 0)  
                
    def __init__(self, x, y, level=None):
        self.timeAlive = 0
                
        if level is None:
            level = random.randint(EnemyStation.minSize, EnemyStation.maxSize)
        self.level = level # different enemy levels
        factor = 1
        
        w, h = EnemyStation.image.get_size()
        EnemyStation.image = pygame.transform.rotate(
                           pygame.transform.scale
                           (EnemyStation.image, 
                           (int(w * factor), int(h * factor))
                           ), 0)
        super().__init__(x, y, EnemyStation.image, max(w, h) / 2 * factor)
        
        vx = 0 
        vy = random.randint(EnemyStation.maxSpeed, EnemyStation.maxSpeed)
        self.velocity = vx, vy        

        self.bullets = pygame.sprite.Group()

    def update(self, dt, screenWidth, screenHeight):
        self.timeAlive += 1
        super().update(screenWidth, screenHeight)
        if self.timeAlive > EnemyStation.lifeTime:
            self.kill()
            self.bullets.empty()
            
    def loadBullets(self, dt, screenWidth, screenHeight):
        numberBullets = 16
        for i in (range(numberBullets)):
            if (len(self.bullets) <= 15):
                bullet = EnemyBullet(self.x, self.y)
                bullet.initEnemyBaseBulletVelocity(360//numberBullets*i)
                self.bullets.add(bullet)
        
    def moveBulletsInPattern(self, dt, screenWidth, screenHeight):
        for bullet in self.bullets:
            bullet.update(screenWidth, screenHeight)

    