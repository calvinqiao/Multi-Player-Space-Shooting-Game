import pygame, random
import math
from GameObject import GameObject
from EnemyBullet import EnemyBullet
from BossMissle import BossMissle

class BossType1(GameObject):
    minSize = 10
    maxSize = 10
    minSpeed = 1
    maxSpeed = 1
    lifeTime = 2000  # last 1 second, 250*0.02 = 5s 

    @staticmethod
    def init():
        BossType1.image = \
        pygame.image.load('images/boss1.png').convert_alpha()
        BossType1.image = pygame.transform.rotate(BossType1.image, 180)  
                
    def __init__(self, round, x, y, level=None):
        self.timeAlive = 0
        if round == 1:
            self.hp = 300 # 10 for testing
        elif round == 2:
            self.hp = 400
        elif round == 3:
            self.hp = 500
        
        self.missleCounter = 0
                
        if level is None:
            level = random.randint(BossType1.minSize, BossType1.maxSize)
        self.level = level # different enemy levels
        factor = 1
        
        w, h = BossType1.image.get_size()
        BossType1.image = pygame.transform.rotate(
                           pygame.transform.scale
                           (BossType1.image, 
                           (int(w * factor), int(h * factor))
                           ), 0)
        super().__init__(x, y, BossType1.image, max(w, h) / 2 * factor)
        
        vx = 0 
        vy = random.randint(BossType1.maxSpeed, BossType1.maxSpeed)
        self.velocity = vx, vy        

        self.pattern1Bullets = pygame.sprite.Group()
        self.pattern2Bullets = pygame.sprite.Group()
        self.missles = pygame.sprite.Group()# test with bullets first, change to missles later

    def update(self, dt, screenWidth, screenHeight):
        self.timeAlive += 1
        super().update(screenWidth, screenHeight)
        if self.x > screenWidth:
            self.x = random.randint(screenWidth//10, screenWidth*9//10)
        if self.x < 0:
            self.x = random.randint(screenWidth//10, screenWidth*9//10)
        #if self.timeAlive > BossType1.lifeTime:
        if self.hp < 0:
            self.kill()
            self.pattern1Bullets.empty()
            self.pattern2Bullets.empty()
            self.missles.empty()
    
    def enterBossState1(self, dt, screenWidth, screenHeight):
        vx, vy = 0, 0
        self.velocity = vx, vy
    
    def loadPattern1Bullets(self, dt, screenWidth, screenHeight):
        numberBullets = 10
        for i in (range(numberBullets)):
            if (len(self.pattern1Bullets) <= 9):
                bullet = EnemyBullet(self.x, self.y)
                bullet.initEnemyBaseBulletVelocity(360//numberBullets*i)
                self.pattern1Bullets.add(bullet)
                
    def loadPattern2Bullets(self, dt, screenWidth, screenHeight):    
        numberBullets = 2        
        for i in (range(numberBullets)):
            if (len(self.pattern2Bullets) <= 1):
                bullet = EnemyBullet(self.x, self.y)
                if i==0: angle = 88
                if i==1: angle = 92
                bullet.initEnemyBaseBulletVelocity(angle)
                self.pattern2Bullets.add(bullet)
    
    def loadMissles(self, dt, screenWidth, screenHeight, mode):
        if mode == "one player mode":
            numberMissles = 1  
        elif mode == "double player mode":
            numberMissles = 2
        for i in (range(numberMissles)):
            if (len(self.missles) < numberMissles):
                # missle = EnemyBullet(self.x, self.y)
                missle = BossMissle(self.x, self.y)
                angle = 90
                missle.initEnemyBaseBulletVelocity(angle)
                self.missles.add(missle)
    
    def moveBulletsInPattern1(self, dt, screenWidth, screenHeight):
        for bullet in self.pattern1Bullets:
            bullet.update(screenWidth, screenHeight)
            
    def moveBulletsInPattern2(self, dt, screenWidth, screenHeight):
        for bullet in self.pattern2Bullets:
            bullet.enemyPattern2BulletUpdate(screenWidth, screenHeight)
            
    def moveMissles(self, dt, screenWidth, screenHeight):
        for missle in self.missles:
            missle.enemyMissleUpdate(screenWidth, screenHeight)
    