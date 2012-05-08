#!c:/Python26/python.exe -u
try:
    import pygame, random, sys
    import pygame.font
    from pygame.locals import *
    import os
    import player 
    import baddie
    import bullet
    import powerup
    import proxy
    import loader as loader
    import proxyexplosion
    from gameobjects.vector2 import Vector2
    import parallax 
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

pygame.init()
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
RESOLUTION = (1024, 768) 
TEXTCOLOR = (255, 255, 255)
background 		= pygame.Surface(RESOLUTION)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
BADDIEMINSIZE = 15
BADDIEMAXSIZE = 50
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
SHOTTHROTTLE = 5
BULLETSPEED = 10
bulletSize = 10
POWERUPRATE = 100
POWERUPTYPES = ['normal', 'random', 'wave', 'ricochet']


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def pauseGame():
    while True:
        e = pygame.event.wait()
        if e.type in (pygame.QUIT, pygame.KEYDOWN):
            return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b.rect):
            return True
    return False

def bulletHasHitBaddie(bullet, baddie):
    if bullet.rect.colliderect(baddie.rect):
        return True
    return False

def proxyExplosionHitBaddie(proxyExplosion, baddie):
    if proxyExplosion.rect.colliderect(baddie.rect):
        return True
    return False

def playerHasHitPowerup(player, powerup):
    if player.rect.colliderect(powerup.rect):
        return True
    return False

def proxyHasHitPowerup(proxy, powerup):
    if proxy.rect.colliderect(powerup.rect):
        return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def teleport(player, proxy):
    player.rect.topleft = proxy.rect.topleft

def load_sliced_sprites(w, h, filename):
    '''
    Specs :
    	Master can be any width 
    	Sprites frames height must be the same height
    	Master height must be len(frames)*frame.height
    '''
    images = []
    master_image = pygame.image.load(os.path.join('data', filename)).convert_alpha()

    master_width, master_height = master_image.get_size()
    #for i in xrange(int(master_width/w)):
    for i in xrange(int(master_height/h)):
    	images.append(master_image.subsurface((0,i*h,w,h)))
    	#images.append(master_image.subsurface((i*w,0,w,h)))
    return images

def muteUnMuteMusic():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play()

# set up pygame, the window, and the mouse cursor
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
iconImage = pygame.image.load('data/pygame_icon.bmp').convert()
icon = pygame.transform.scale(iconImage, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('JShooter')
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
# set up font
pygame.font.init()
font = pygame.font.Font('data/freesansbold.ttf', 32)

# set up sounds
gameOverSound = loader.load_sound('gameover.wav')
#TODO build some sort of music handling queue / control object.
pygame.mixer.music.load('./data/theme.ogg')
#pygame.mixer.music.load('data/background.mid')

# set up images
player = player.Player()
proxy = proxy.Proxy()
baddieImage, baddieRect = loader.load_png('baddie.png')
bulletImage, bulletRect = loader.load_png('bullet.png')
powerupImage, powerupRect = loader.load_png('powerup.png')

# show the "Start" screen
drawText('JShooter', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10))
drawText('Mouse Move', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+50)
drawText('Mouse Button1 Shoots', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+100)
drawText('WASD Moves Proxy', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+150)
drawText('Spacebar Proxy BOMB', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+200)
drawText('TAB Teleport', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+250)
drawText('[ & ] Adjust Music Volume', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+300)
drawText('m mutes the Music', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+350)
drawText('Pause: p, Q or ESC Quits', font, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 10)+400)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 450)
pygame.display.update()
waitForPlayerToPressKey()

backgrounds	= []
parallax_1 = load_sliced_sprites(1024, 1900, 'parallax1-1024x1900.png')
parallax_2 = load_sliced_sprites(1024, 768, 'parallax5-1024x768.png')
parallax_3 = load_sliced_sprites(1024, 768, 'parallax2-1024x768.png')
parallax_4 = load_sliced_sprites(1024, 768, 'parallax3-1024x768.png')
parallax_5 = load_sliced_sprites(1024, 768, 'parallax4-1024x768.png')

prlx1 = parallax.Parallax(parallax_1, 60)
prlx1.speed = 10.
prlx1.location = (0, 0)
prlx1.destination = Vector2(*(0,parallax_1[0].get_rect().h))
#prlx1.destination = Vector2(*(-parallax_1[0].get_rect().w, 0))
backgrounds.append(prlx1)

prlx2 = parallax.Parallax(parallax_2, 60)
prlx2.speed = 40.
prlx2.location = (0, 0)
#prlx2.location = (0, 110)
prlx2.destination = Vector2(*(0, parallax_2[0].get_rect().h))
#prlx2.destination = Vector2(*(-parallax_2[0].get_rect().w, 110))
backgrounds.append(prlx2)

prlx3 = parallax.Parallax(parallax_3, 60)
prlx3.speed = 80.
prlx3.location = (0, 0)
#prlx3.location = (0, 60)
prlx3.destination = Vector2(*(0, parallax_3[0].get_rect().h))
#prlx3.destination = Vector2(*(-parallax_3[0].get_rect().w, 60))
backgrounds.append(prlx3)
	 	
prlx4 = parallax.Parallax(parallax_4, 60)
prlx4.speed = 120.
prlx4.location = (0, 0)
#prlx4.location = (0, 90)
prlx4.destination = Vector2(*(0, parallax_4[0].get_rect().h))
#prlx4.destination = Vector2(*(-parallax_4[0].get_rect().w, 90))
backgrounds.append(prlx4)
		
prlx5 = parallax.Parallax(parallax_5, 60)
prlx5.speed = 900.
prlx5.location = (0, 0)
prlx5.destination = Vector2(*(0, parallax_5[0].get_rect().h))
#prlx5.destination = Vector2(*(-parallax_5[0].get_rect().w, 0))
backgrounds.append(prlx5)

bombs = 1
topScore = 0
while True:
    # set up the start of the game
    baddies = []
    bullets = []
    powerups = []
    proxyExplosions = []
    proxyExplosionCounter = 0
    score = 0
    player.rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    proxy.rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 75)
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    bulletAddCounter = 0
    powerupAddCounter = 0
    pygame.mixer.music.set_volume(float('0.5'))
    pygame.mixer.music.play(-1, 0.0)
    
    while True: # the game loop runs while the game part is playing
        #score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    teleport(player, proxy)
                #moving the proxy
                if event.key == K_LEFT or event.key == ord('a'):
                    proxy.moveRight = False
                    proxy.moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    proxy.moveLeft = False
                    proxy.moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    proxy.moveDown = False
                    proxy.moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    proxy.moveUp = False
                    proxy.moveDown = True
                if event.key == K_SPACE:
                    if bombs > 0:
                        bombs -= 1
                        proxy.isExploding = True
                    #proxy.isShooting = True
                if event.key == ord('p'):
                    drawText('Game Paused', font, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))
                    pygame.mixer.music.pause()
                    pygame.display.update()
                    pauseGame()
                    pygame.mixer.music.unpause()
                if event.key == K_LEFTBRACKET:
                    vol = pygame.mixer.music.get_volume()
                    if vol > float('0.0'):
                        newVol = float(vol) - float('0.1')
                        pygame.mixer.music.set_volume(newVol)
                        #print "Volume Lowering" + str(newVol)
                if event.key == K_RIGHTBRACKET:
                    vol = pygame.mixer.music.get_volume()
                    if vol < float('1.0'):
                        newVol = float(vol) + float('0.1')
                        pygame.mixer.music.set_volume(newVol)
                        #print "Volume Upening" + str(newVol)


            #cheats
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_LEFT or event.key == ord('a'):
                    proxy.moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    proxy.moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    proxy.moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    proxy.moveDown = False
                #if event.key == K_SPACE:
                if event.key == ord('m'):
                    muteUnMuteMusic()
                    


                if event.key == K_ESCAPE or event.key == ord('q'):
                        terminate()

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                player.rect.move_ip(event.pos[0] - player.rect.centerx, event.pos[1] - player.rect.centery)

            if event.type == MOUSEBUTTONDOWN:
                player.isShooting = True
            
            if event.type == MOUSEBUTTONUP:
                player.isShooting = False
            
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)

            newBaddie = baddie.Baddie(baddieImage, (pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize)), baddieSize, random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), pygame.transform.scale(baddieImage, (baddieSize, baddieSize)))

            baddies.append(newBaddie)

        # add new powerup
        powerupAddCounter += 1
        if powerupAddCounter == POWERUPRATE:
            powerupSize = 25
            powerupAddCounter = 0
            newPowerup = powerup.Powerup(powerupImage, (pygame.Rect(random.randint(0, WINDOWWIDTH-powerupSize), 0 - powerupSize, powerupSize, powerupSize)), 
                  powerupSize, random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), pygame.transform.scale(powerupImage, 
                  (powerupSize, powerupSize)), POWERUPTYPES[random.randint(0, len(POWERUPTYPES)-1)])
            powerups.append(newPowerup)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(player.rect.centerx, player.rect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b.rect.move_ip(0, b.speed)
            elif reverseCheat:
                b.rect.move_ip(0, -5)
            elif slowCheat:
                b.rect.move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b.rect.top > WINDOWHEIGHT:
                baddies.remove(b)
        #powerups
        for p in powerups:
            if not reverseCheat and not slowCheat:
                p.rect.move_ip(0,p.speed)
            elif reverseCheat: 
                p.rect.move_ip(0, -5)
            elif slowCheat:
                p.rect.move_ip(0,1)

        for p in powerups[:]:
            if p.rect.top > WINDOWHEIGHT:
                powerups.remove(p)

        if proxy.isExploding == True:
            if proxyExplosionCounter == 0:
                proxyExplosionCounter += 1
                newProxyExplosion = proxyexplosion.ProxyExplosion()
                newProxyExplosion.rect.x = proxy.rect.x - 75
                newProxyExplosion.rect.y = proxy.rect.y - 75
                proxyExplosions.append(newProxyExplosion)

        #bullets from player
        if player.isShooting == True:
            bulletAddCounter += 1
            if bulletAddCounter == SHOTTHROTTLE:
                bulletAddCounter = 0
                newBullet = bullet.Bullet(bulletImage, (pygame.Rect(player.rect.centerx, player.rect.centery, bulletSize, bulletSize)), BULLETSPEED, pygame.transform.scale(bulletImage, (bulletSize, bulletSize)),  player.rect.centerx, player.rect.centery, 'player')
                bullets.append(newBullet)
                if player.type == "ricochet":
                    bullets.append(newBullet)

        if player.type == 'ricochet':
            temp = 0

        if player.type == "wave":
            wave = -10
            direction = 'right'
        # Move the bullets up.
        for bu in bullets:
            if not reverseCheat and not slowCheat:
                if player.type == "normal" and bu.owner == "player":
                    bu.rect.move_ip(0, -bu.speed)
                elif player.type == "random" and bu.owner == "player":
                    bu.rect.move_ip(random.randint(-10,10), -bu.speed)
                elif player.type == "wave" and bu.owner == "player":
                    if wave == 10 and direction == "right":
                        direction = 'left'
                        wave -= 1
                    elif wave == -10 and direction == "left":
                        direction = 'right'
                        wave += 1
                    elif direction == 'left':
                        bu.rect.move_ip(wave, -bu.speed)
                        wave -= 1
                    elif direction == "right":
                        bu.rect.move_ip(wave, -bu.speed)
                        wave += 1

                elif player.type == "ricochet" and bu.owner == "player":
                    if temp == 0:
                        bu.rect.move_ip(-5, -bu.speed)
                        temp += 1
                    elif temp == 1:
                        bu.rect.move_ip(0, -bu.speed)
                        temp += 1
                    else:
                        bu.rect.move_ip(5, -bu.speed)
                        temp = 0
            elif reverseCheat:
                bu.rect.move_ip(0, -5)
            elif slowCheat:
                bu.rect.move_ip(0, 1)

         # Delete bullets that have moved past the top of the screen
        for bu in bullets[:]:
            if bu.rect.top > WINDOWHEIGHT:
                bullets.remove(bu)
        
        # Move the proxy around
        if proxy.moveDown and proxy.rect.bottom < WINDOWHEIGHT:
            proxy.rect.top += proxy.speed
        if proxy.moveUp and proxy.rect.top > 0:
            proxy.rect.top -= proxy.speed
        if proxy.moveLeft and proxy.rect.left > 0:
            proxy.rect.left -= proxy.speed 
        if proxy.moveRight and proxy.rect.right < WINDOWWIDTH:
           proxy.rect.right += proxy.speed

        # Draw the game world on the window.
#        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(background, (0, 0))
        time_passed = mainClock.tick(60)
        time_passed_seconds = time_passed / 1000.0
                
        for parallax in backgrounds:	
            parallax.process(time_passed_seconds)
            parallax.render(windowSurface)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Bombs left: %s' % (bombs), font, windowSurface, 10, 80)

        # Draw the player's rectangle
        windowSurface.blit(proxy.image, proxy.rect)
        windowSurface.blit(player.image, player.rect)
        for pe in proxyExplosions:
            if pe.frame < pe.frame_limit:
                pe.frame += pe.frame_step
                #print "Frame " + str(pe.frame)
                pe.image = pygame.transform.scale(pe.image, (pe.frame, pe.frame))
                windowSurface.blit(pe.image, pe.rect)
                #pe.rect.inflate(10,10)
            else:
                proxy.isExploding = False
                proxyExplosionCounter = 0
                proxyExplosions.remove(pe)
        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b.surface, b.rect)

        #draw the bullets
        for bu in bullets:
            windowSurface.blit(bu.surface, bu.rect)
        
        #powerups
        for p in powerups:
            windowSurface.blit(p.surface, p.rect)


        pygame.display.update()

        #check if the bullets have hit the baddies
        for bu in bullets[:]:
            for b in baddies[:]:
                if bulletHasHitBaddie(bu, b):
                    score = score + 100
                    if bu in bullets:
                        bullets.remove(bu)
                    baddies.remove(b)
        
        if proxy.isExploding == True:
            for b in baddies[:]:
                if proxyExplosionHitBaddie(pe, b):
                    baddies.remove(b)


        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(player.rect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        #powerup
        for p in powerups[:]:
            if playerHasHitPowerup(player, p):
                player.type = p.type
                #print "Setting the players bullets to " + p.type
                powerups.remove(p)
            elif proxyHasHitPowerup(proxy, p):
                bombs += 1
                powerups.remove(p)

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
