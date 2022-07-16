import pygame
import math
from GameObject import GameObject

class EnemyBullet(GameObject):
    speed = 25
    lifeTime = 100 # last 1 second 100*0.02 = 2s
    bossPattern2LifeTime = 20
    missleLifeTime = 500
    size = 10
    timeAlive = 0

    def __init__(self, x, y):
        self.timeAlive, self.missleTimeAlive = 0, 0
        self.bulletPattern2TimeAlive = 0

        size = EnemyBullet.size
        
        image = pygame.Surface((EnemyBullet.size, EnemyBullet.size), 
                pygame.SRCALPHA)
        circle = pygame.draw.circle(image, 
                 (255, 255, 255), (size//2, size//2), size // 2)
        super().__init__(x, y, image, size // 2)
        
        vx = EnemyBullet.speed * math.cos(math.radians(90))
        vy = EnemyBullet.speed * math.sin(math.radians(90))
        self.velocity = vx, vy
        
    def initEnemyBaseBulletVelocity(self, angle):
        vx = EnemyBullet.speed * math.cos(math.radians(angle))
        vy = EnemyBullet.speed * math.sin(math.radians(angle))
        self.velocity = (vx, vy)
        
    def initBossPattern2BulletBelocity(self, angle):
        vx = EnemyBullet.speed//3 * math.cos(math.radians(angle))
        vy = EnemyBullet.speed//3 * math.sin(math.radians(angle))
        self.velocity = (vx, vy)

    def update(self, screenWidth, screenHeight):
        self.timeAlive += 1
        
        super().update(screenWidth, screenHeight)

        if self.timeAlive > EnemyBullet.lifeTime:
            self.kill()
    
    def enemyMissleUpdate(self, screenWidth, screenHeight):
        self.missleTimeAlive += 1
        super().update(screenWidth, screenHeight)

        if self.missleTimeAlive > EnemyBullet.missleLifeTime:
            print("kill missle here")
            self.kill()
    
    def enemyPattern2BulletUpdate(self, screenWidth, screenHeight):
        self.bulletPattern2TimeAlive += 1
        
        super().update(screenWidth, screenHeight)

        if self.bulletPattern2TimeAlive > EnemyBullet.bossPattern2LifeTime:
            self.kill()
            # add explosions
    
    def baseShootingUpdate(screenWidth, screenHeight):
        pass
            