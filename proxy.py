try:
    import sys
    import pygame
    import pygame.font
    import loader as loader

except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


class Proxy(pygame.sprite.Sprite):
    """Proxy class, will have the image, along with coords and abilities"""

    def __init__(self):
        self.image, self.rect = loader.load_png("proxy.png")
        screen = pygame.display.get_surface()
        self.isExploding = False
        self.area = screen.get_rect()
        self.speed = 10
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
