import pygame, random
import math
from GameObject import GameObject

class StartMenu(GameObject):

    @staticmethod
    def init():
        StartMenu.image = \
        pygame.image.load('images/planet.png').convert_alpha()
                
    def __init__(self, x, y, level=None):
        self.timeAlive = 0
                
        factor = 1
        
        w, h = StartMenu.image.get_size()
        image = pygame.transform.scale(StartMenu.image, 
        (int(w * factor), int(h * factor)))
        super().__init__(x, y, image, max(w, h) / 2 * factor)
        
     
    
    