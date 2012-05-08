try:
    import pygame, random, sys
    import pygame.font
    from pygame.locals import *
    import os
    import loader as loader
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)
    
class ProxyExplosion(pygame.sprite.Sprite):
    """ProxyExplosion class, will have the image, along with coords and abilities"""
    def __init__(self):
        self.image, self.rect = loader.load_png('proxyexplosion.png')
        screen = pygame.display.get_surface()
        self.frame = 0
        self.frame_step = 10
        self.frame_limit = 250
        self.area = screen.get_rect()
    
    def update(self):
       newpos = self.rect.move(self.movepos)
       if self.area.contains(newpos):
           self.rect = newpos
       pygame.event.pump()

