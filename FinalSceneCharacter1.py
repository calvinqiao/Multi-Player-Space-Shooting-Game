import pygame, random
import math
from GameObject import GameObject

class FinalSceneCharacter1(GameObject):
    minSize = 2
    maxSize = 4
    maxSpeed = 3

    @staticmethod
    def init():
        FinalSceneCharacter1.image = pygame.image.load('images/staff/53.png').convert_alpha()
                
    def __init__(self, x, y, level=None):
        if level is None:
            level = random.randint(FinalSceneCharacter1.minSize, FinalSceneCharacter1.maxSize)
        self.level = level
        factor = 0.5
        
        image = FinalSceneCharacter1.image
        w, h = image.get_size()
        image = pygame.transform.scale(image, (int(w * factor), int(h * factor)))
        super().__init__(x, y, image, w / 2 * factor)
        self.angleSpeed = random.randint(-10, 10)
        vx = random.randint(-FinalSceneCharacter1.maxSpeed, -1)
        vy = random.randint(1, FinalSceneCharacter1.maxSpeed)
        self.velocity = vx, vy
    
    def update(self, screenWidth, screenHeight):
        # self.angle += self.angleSpeed
        super().update(screenWidth, screenHeight)
        if self.x < self.width//2:        
            vx, vy = self.velocity
            vx *= -1
            self.velocity = vx, vy
        if self.x > screenWidth - self.width//2:
            vx, vy = self.velocity
            vx *= -1
            self.velocity = vx, vy
        if self.y > screenHeight - self.height//2:
            vx, vy = self.velocity
            vy *= -1
            self.velocity = vx, vy
        if self.y < self.height//2:
            vx, vy = self.velocity
            vy *= -1
            self.velocity = vx, vy
    
    # def breakApart(self):
    #     if self.level == FinalSceneCharacter1Character1.minSize:
    #         return []
    #     else:
    #         return [FinalSceneCharacter1(self.x, self.y, self.level - 1),
    #                 FinalSceneCharacter1(self.x, self.y, self.level - 1)]