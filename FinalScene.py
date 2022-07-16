import pygame, random
import math
from GameObject import GameObject

class FinalScene(GameObject):
    minSize = 2
    maxSize = 4
    maxSpeed = 5

    @staticmethod
    def init():
        image1 = pygame.image.load('images/staff/53.png').convert_alpha()
        image2 = pygame.image.load('images/staff/54.png').convert_alpha()
        FinalScene.images = []
        FinalScene.images.append(image1)
        FinalScene.images.append(image2)
                
    def __init__(self, x, y, level=None):
        if level is None:
            level = random.randint(Asteroid.minSize, Asteroid.maxSize)
        self.level = level
        factor = 1
        
        image = random.choice(FinalScene.images)
        w, h = image.get_size()
        image = pygame.transform.scale(image, (int(w * factor), int(h * factor)))
        super().__init__(x, y, image, w / 2 * factor)
        self.angleSpeed = random.randint(-10, 10)
        vx = random.randint(-FinalScene.maxSpeed, FinalScene.maxSpeed)
        vy = random.randint(-FinalScene.maxSpeed, FinalScene.maxSpeed)
        self.velocity = vx, vy
    
    def update(self, screenWidth, screenHeight):
        self.angle += self.angleSpeed
        super().update(screenWidth, screenHeight)
    
    # def breakApart(self):
    #     if self.level == Asteroid.minSize:
    #         return []
    #     else:
    #         return [FinalScene(self.x, self.y, self.level - 1),
    #                 FinalScene(self.x, self.y, self.level - 1)]