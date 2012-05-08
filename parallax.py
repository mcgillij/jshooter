try:
    import pygame, random, sys
    import pygame.font
    from pygame.locals import *
    import os
    from gameobjects.vector2 import Vector2
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

class AnimatedSprite(pygame.sprite.Sprite):
		def __init__(self, images, fps = 10):
			pygame.sprite.Sprite.__init__(self)
			
			# Animation 
			self._start 			= pygame.time.get_ticks()
			self._delay 			= 1000 / fps
			self._last_update = 0
			self._frame 			= 0
			self._images 			= images
			
			self.image 				= self._images[self._frame]
			
			# Movement
			self.location 		= (0,0)
			self.destination 	= (0,0)
			self.heading			= None
			self.speed				= 0.
			
			
			
		def process(self, t):
			if self.speed > 0. and self.location != self.destination:
					destination 						= self.destination - self.location				
					distance 								= destination.get_length()
					self.heading 						= destination.get_normalized()
					most_accurate_distance 	= min(distance, t * self.speed)
					self.location 					+= most_accurate_distance * self.heading
					
		def update(self, t):
			
			# Note that this doesn't work if it's been more that self._delay
			# time between calls to update(); we only update the image once
			# then, but it really should be updated twice.
			if t - self._last_update > self._delay:
				self._frame += 1
				if self._frame >= len(self._images):
					self._frame = 0
					
				self.image = self._images[self._frame]
				self._last_update = t
            
		def render(self, screen):
			screen.blit(self.image, self.location)

class Parallax(AnimatedSprite):
		def __init__(self, images, fps = 30):
			AnimatedSprite.__init__(self, images, fps)
		
		def render(self, screen):
			# Overridding the default render method
			w,h = self.image.get_size()
			x,y = self.location
			W,H = (1024, 768)
			#W,H = RESOLUTION
			if abs(y) == h:
			#if abs(x) == w:
				self.location = Vector2(0, 0)
				#self.location = Vector2(x, 0)
				#self.location = Vector2(0, y)
				y = 0
#				x = 0
					
			# Blitting the image loop 
			if y - h < H:
			#if x - w < W:
				location = Vector2(x, y-h)
				#location = Vector2(x+w, y)
				screen.blit(self.image, location)
			
			screen.blit(self.image, self.location)
