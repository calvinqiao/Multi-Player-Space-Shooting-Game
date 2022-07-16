import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super().__init__()
        
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        # non-rotated version of image
        self.baseImage = image.copy() 
         
        w, h = image.get_size()
        self.width, self.height = w, h
        
        self.updateRect()
        
        self.velocity = (0, 0)
        
        self.angle = 0

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        self.rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, 
                    self.width, self.height)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        
        vx, vy = self.velocity
        self.x += vx
        self.y += vy
        
        self.updateRect()
