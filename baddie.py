try:
    import os
    import random
    import sys
    import pygame
    import pygame.font
    from pygame.locals import *

except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


class Baddie(pygame.sprite.Sprite):
    """Baddie class, will have the image, along with coords and abilities"""

    def __init__(self, image, rect, size, speed, surface):
        self.image = image
        self.rect = rect
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.size = size
        self.speed = speed
        self.surface = surface

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
