try:
    import sys
    import pygame
    import pygame.font

except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


class Powerup(pygame.sprite.Sprite):
    """Powerup class, will have the image, along with coords and abilities"""

    def __init__(self, image, rect, size, speed, surface, type):
        self.image = image
        self.rect = rect
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.size = size
        self.speed = speed
        self.surface = surface
        self.type = type

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
