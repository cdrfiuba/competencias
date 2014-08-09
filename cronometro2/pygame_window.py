import pygame

class PyGameWindow():

    def __init__(self):
        self.WIDTH = 640
        self.HEIGHT = 480

        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT),pygame.RESIZABLE|pygame.DOUBLEBUF)

        self.font = pygame.font.Font(None, 30)
        self.text1 = self.font.render("Texto de pruebas", 0, (255, 0, 0))
 
        self.screen.blit(self.text1,(100,100))


        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()

    def update(self):
        self.screen.blit(self.text1,(100,100))
        pygame.display.update()

    def setWindowName(self, name=None):
        pygame.display.set_caption(name)
