try:
    import pygame, random, sys
    import pygame.font
    from pygame.locals import *
    import os
  
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

class Bullet(pygame.sprite.Sprite):
    """Bullet class, will have the image, along with coords and abilities"""
    def __init__(self, image, rect, speed, surface, startx, starty, owner):
        self.image = image
        self.rect = rect
        self.speed = speed
        self.surface = surface
        self.startx = startx
        self.starty = starty
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.owner = owner

    def update(self):
       newpos = self.rect.move(self.movepos)
       if self.area.contains(newpos):
           self.rect = newpos
       pygame.event.pump()
