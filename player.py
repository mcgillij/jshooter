try:
    import pygame, random, sys
    import pygame.font
    from pygame.locals import *
    import os
    import loader as loader
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


class Player(pygame.sprite.Sprite):
    """Player class, will have the image, along with coords and abilities"""

    def __init__(self):
        self.image, self.rect = loader.load_png("player.png")
        screen = pygame.display.get_surface()
        self.isShooting = False
        self.area = screen.get_rect()
        self.speed = 10
        self.type = "normal"  # bullet type

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
