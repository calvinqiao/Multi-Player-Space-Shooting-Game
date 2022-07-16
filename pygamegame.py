'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame

class PygameGame(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass
    
    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=600, fps=50, title="Get to the 112 Planet"):
        self.playing = True
        self.playMusic = 1
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
        self.channel2 = pygame.mixer.Channel(1)
        # self.explosionSound = pygame.mixer.Sound('music/explosionSound.wav')

    def processEvents(self):
        pass

    def playBGMusic(self, music, channel):
        pass

    def run(self, serverMsg, server):
        # bgMusic = pygame.mixer.Sound('music/bgMusic.wav')
        # channel1 = pygame.mixer.Channel(0) # argument must be int
        # self.playBGMusic(bgMusic, channel1)
        
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        # self._otherPlayerKeys = dict()

        self.server = server
        self.serverMsg = serverMsg
        
        # call game-specific initialization
        self.init()
        
        bkgd = pygame.image.load('images/background.png').convert()
        y = 0
        
        while self.playing:            
            screen.blit(bkgd, (0, -bkgd.get_rect().height+ self.height + y))
            if y >= bkgd.get_rect().height - self.height:
                y = 0            
            y += 1
            time = clock.tick(self.fps)
            self.timerFired(time)
            self.processEvents()
            self.redrawAll(screen)
            # pygame.display.flip()
            pygame.display.update()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    