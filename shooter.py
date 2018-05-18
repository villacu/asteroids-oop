import pygame, sys
from pygame import *
import numpy as np
from random import randint


PLAYER_COLOR = (255,10,10)
BG_COLOR = (25,25,25)
COLOR_1 = (255,255,255)

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900

BULLET_SPEED = 15
PLAYER_SPEED = 5
SIZE = 10
MIN_ESIZE = 15
PLAYER_LIFE = 900

#Para hacer el efecto de cambio de colores
colorList = ((255, 51, 0),(255, 51, 153),(153, 102, 255),
(0, 102, 255),(0, 255, 255),(0, 255, 0),
(204, 255, 102),(255, 102, 0))

enemycList = ((255, 234, 234),(252, 255, 224),(224, 255, 234),
(234, 255, 242),(234, 255, 242),(255, 234, 255),
(255, 234, 245),(234, 250, 255))

oldList = ((155, 171, 120),(155, 171, 155),(155, 122, 155),
(120, 122, 155),(194, 164, 155),(120, 155, 120),
(155, 155, 122),(155, 122, 120))

### CONTROLES ###
pressUP = K_w
pressDOWN = K_s
pressLEFT = K_a
pressRIGHT = K_d

enemyList = []
boostList = []

class player(pygame.sprite.Sprite):
    def __init__(self, sideSize, color, speed):
        super().__init__()
        self.image = pygame.Surface([sideSize,sideSize])
        self.color = color
        self.size = sideSize
        pygame.draw.rect(self.image, self.color, [0, 0, sideSize, sideSize])
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/2
        self.rect.y = SCREEN_HEIGHT/2
        self.direction = [0,0]
        self.bulletList = []
        self.bulletSound = pygame.mixer.Sound('music/shot.wav')
        self.bigBulletSound = pygame.mixer.Sound('music/bigshot.wav')
        #stats
        self.speed = speed
        self.life = PLAYER_LIFE
        self.score = 0
    def moving(self):
        x_direction = self.direction[0]
        y_direction = self.direction[1]
        if(x_direction != 0):
            if self.rect.left <= (SCREEN_WIDTH-2*self.size) and self.rect.left >= 0:
                self.rect.left += self.speed*x_direction
            elif(self.rect.left > (SCREEN_WIDTH-2*self.size)):
                self.rect.left = 0
            elif(self.rect.left < 0):
                self.rect.left = (SCREEN_WIDTH-2*self.size)
        if(y_direction != 0):
            if self.rect.bottom <= (SCREEN_HEIGHT) and self.rect.top >= 0:
                self.rect.top += self.speed*y_direction
            elif(self.rect.bottom > (SCREEN_HEIGHT)):
                self.rect.top = 0
            elif(self.rect.top < 0):
                self.rect.bottom = SCREEN_HEIGHT-self.size
    def shoot(self, x, y, vx, vy):
        self.bulletSound.play()
        newBullet = bullet(x, y, vx, vy)
        self.bulletList.append(newBullet)
        #print('xvel = ' + str(newBullet.x_vel))
        #print('yvel = ' + str(newBullet.y_vel))
    def shoot_bigBullet(self, x, y, vx, vy):
        self.bigBulletSound.play()
        newBullet = bigBullet(x, y, vx, vy)
        self.bulletList.append(newBullet)
    def newColor(self, nColor):
        x = self.rect.centerx
        y = self.rect.centery
        self.image = pygame.Surface([self.size,self.size])
        pygame.draw.rect(self.image, nColor, [0, 0, self.size, self.size])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    def update(self, surface):
        #print(self.life)
        self.moving()
        surface.blit(self.image, self.rect)

class enemy(pygame.sprite.Sprite):
    def __init__(self, size, color, spawnX, spawnY):
        super().__init__()
        if size < 30:
            self.speed = PLAYER_SPEED
        elif size < 75:
            self.speed = PLAYER_SPEED-1
        elif size > 75:
            self.speed = PLAYER_SPEED-2
        self.life = size-MIN_ESIZE
        self.originalLife = self.life
        self.image = pygame.Surface([size,size])
        self.color = color
        self.size = size
        #self.speed = speed
        self.originalSize = self.size
        pygame.draw.rect(self.image, self.color, [0, 0, size, size])
        self.rect = self.image.get_rect()
        self.rect.x = spawnX
        self.rect.y = spawnY
        self.direction = [0,0]
        self.bulletList = []
        #stats
    def moving(self):
        x_direction = self.direction[0]
        y_direction = self.direction[1]
        if(x_direction != 0):
            if self.rect.left <= (SCREEN_WIDTH-2*self.size) and self.rect.left >= 0:
                self.rect.left += self.speed*x_direction
            elif(self.rect.left > (SCREEN_WIDTH-2*self.size)):
                self.rect.left = 0
            elif(self.rect.left < 0):
                self.rect.left = (SCREEN_WIDTH-2*self.size)
        if(y_direction != 0):
            if self.rect.bottom <= (SCREEN_HEIGHT) and self.rect.top >= 0:
                self.rect.top += self.speed*y_direction
            elif(self.rect.bottom > (SCREEN_HEIGHT)):
                self.rect.top = 0
            elif(self.rect.top < 0):
                self.rect.bottom = SCREEN_HEIGHT-self.size
    def hit(self):
        if self.life > MIN_ESIZE:
            self.size = self.life
            if self.speed < PLAYER_SPEED+1:
                self.speed += 0.03
    def update(self, surface):
        x = self.rect.centerx
        y = self.rect.centery
        self.image = pygame.Surface([self.size,self.size])
        pygame.draw.rect(self.image, self.color, [0, 0, self.size, self.size])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.moving()
        surface.blit(self.image, self.rect)

def enemySpawn():
    quadrant = randint(1,4)
    if quadrant == 1:
        spawnPosx = 100
        spawnPosy = 100
    elif quadrant == 2:
        spawnPosx = SCREEN_WIDTH-100
        spawnPosy = 100
    elif quadrant == 3:
        spawnPosx = 100
        spawnPosy = SCREEN_HEIGHT -100
    elif quadrant == 4:
        spawnPosx = SCREEN_WIDTH -100
        spawnPosy = SCREEN_HEIGHT -100
    newEnemy = enemy(randint(80,200),enemycList[randint(0,7)],spawnPosx,spawnPosy)
    xDir = randint(0,1)
    yDir = randint(0,1)
    if(xDir == 0):
        xDir = -1
    if(yDir == 0):
        yDir = -1
    newEnemy.direction = [xDir, yDir]
    enemyList.append(newEnemy)

class boost(pygame.sprite.Sprite):
    def __init__(self, pick):
        self.image = pygame.Surface([30,20])
        self.color = color
        pygame.draw.rect(self.image, (255,255,0), [0, 0, 30, 20])
        self.rect = self.image.get_rect()
        self.rect.x = randint(0,SCREEN_WIDTH-10)
        self.rect.y = randint(0,SCREEN_HEIGHT-10)
        self.score = 0
        self.life = 0
        if pick == 1 or 2:
            self.score = randint(1,6)*100
        elif pick == 3:
            self.life = randint(5,10)*10

    def update(self,surface):
        surface.blit(self.image, self.rect)

def spawnBoost():
    newBoost = boost(randint(1,3))
    boostList.append(newBoost)

class life(pygame.sprite.Sprite):
    def __init__(self, life):
        super().__init__()
        self.life = life
        self.originalLife = life
        self.image = pygame.Surface([SCREEN_WIDTH,10])
        self.color = (255,255,255)
        pygame.draw.rect(self.image, self.color, [0, 0, SCREEN_WIDTH, 10])
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = SCREEN_HEIGHT
        self.size = SCREEN_WIDTH
    def update(self, surface, playerLife):
        newLife = playerLife
        newSize = SCREEN_WIDTH*(newLife/self.originalLife)
        self.image = pygame.Surface([newSize,10])
        pygame.draw.rect(self.image, self.color, [0, 0, newSize, 10])
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.size = SCREEN_WIDTH
        surface.blit(self.image, self.rect)

def displayText(surface,my_font,time,score):
    #time = my_font.render(str(time),0, (255,255,255))
    surface.blit(my_font.render(str(time),0, (255,255,255)),(10,10))
    surface.blit(my_font.render(str(score),0, (255,255,155)),(100,10))

class level():
    def go(self,n):
        pygame.mixer.Sound('music/spawn.wav').play()
        for i in range(0,n):
            enemySpawn()

class bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy, vx, vy):
        super().__init__()
        self.image = pygame.Surface([4,4])
        pygame.draw.rect(self.image, (255, 255, 255), [0, 0, 4, 4])
        self.rect = self.image.get_rect()
        #self.imageProjectile = pygame.image.load('imagenes_pygame/disparoa.jpg')
        #self.rect = self.imageProjectile.get_rect()
        self.bulletSpeed = BULLET_SPEED
        self.x_vel = self.bulletSpeed*vx
        self.y_vel = self.bulletSpeed*vy
        self.rect.top = posy
        self.rect.left = posx
        self.damage = 5
    def trajectory(self):
        self.rect.top = self.rect.top + self.y_vel
        self.rect.left = self.rect.left + self.x_vel
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class bigBullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy, vx, vy):
        super().__init__()
        self.image = pygame.Surface([20,20])
        pygame.draw.rect(self.image, (255, 205, 205), [0, 0, 20, 20])
        self.rect = self.image.get_rect()
        #self.imageProjectile = pygame.image.load('imagenes_pygame/disparoa.jpg')
        #self.rect = self.imageProjectile.get_rect()
        self.bulletSpeed = BULLET_SPEED+1
        self.x_vel = self.bulletSpeed*vx
        self.y_vel = self.bulletSpeed*vy
        self.rect.top = posy
        self.rect.left = posx
        self.damage = 50
    def trajectory(self):
        self.rect.top = self.rect.top + self.y_vel
        self.rect.left = self.rect.left + self.x_vel
    def draw(self, surface):
        surface.blit(self.image, self.rect)

def game():
    pygame.init()
    #PANTALLA MUSICA STATS
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("SHOOTER")
    track = randint(1,4)
    pygame.mixer.music.load('music/soundtrack_'+ str(track) + '.mp3')
    pygame.mixer.music.play(2)
    Clock = pygame.time.Clock()
    game_1 = level()
    my_font = pygame.font.Font(None,30)
    #JUGADOR
    col = 0
    mainPlayer = player(12, colorList[4], PLAYER_SPEED)
    lifeBar = life(mainPlayer.life)
    playerScore = 0
    #BOOLEANOS
    inGame = True
    gotHit = False
    spawning = True
    enemySpawn()
    while inGame:
        time = pygame.time.get_ticks()/1000
        if(mainPlayer.life < 0):
            inGame = False
        Clock.tick(120)
        time = pygame.time.get_ticks()/1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pressRIGHT:
                    mainPlayer.direction[0] = 1
                elif event.key == pressLEFT:
                    mainPlayer.direction[0] = -1
                elif event.key == pressDOWN:
                    mainPlayer.direction[1] = 1
                elif event.key == pressUP:
                    mainPlayer.direction[1] = -1
                elif event.key == K_SPACE:
                    game_1.go(enemyNumber)
            elif event.type == KEYUP:
                if event.key == pressRIGHT:
                    if mainPlayer.direction[0] == 1:
                        mainPlayer.direction[0] = 0
                elif event.key == pressLEFT:
                    if mainPlayer.direction[0] == -1:
                        mainPlayer.direction[0] = 0
                elif event.key == pressDOWN:
                    if mainPlayer.direction[1] == 1:
                        mainPlayer.direction[1] = 0
                elif event.key == pressUP:
                    if mainPlayer.direction[1] == -1:
                        mainPlayer.direction[1] = 0
            elif event.type == MOUSEBUTTONDOWN:
                print(event.button)
                if(event.button == 1):
                    x,y = mainPlayer.rect.center
                    x2,y2 = pygame.mouse.get_pos()
                    direction = [1,1]
                    dx = x2-x
                    if dx < 0:
                        direction[0] = -1
                    dy = y2-y
                    if dy < 0:
                        direction[1] = -1
                    if dx == 0:
                        yComponent = 1
                        xComponent = 0
                    elif dy == 0:
                        xComponent = 1
                        yComponent = 0
                    else:
                        angle = np.arctan(np.abs(dy/dx))
                        xComponent = np.cos(angle)*direction[0]
                        yComponent = np.sin(angle)*direction[1]
                    #print('xcomp : ' + str(xComponent))
                    #print('ycomp : ' + str(yComponent))
                    mainPlayer.shoot(x, y, xComponent, yComponent)
                elif(event.button == 3):
                    x,y = mainPlayer.rect.center
                    x2,y2 = pygame.mouse.get_pos()
                    direction = [1,1]
                    dx = x2-x
                    if dx < 0:
                        direction[0] = -1
                    dy = y2-y
                    if dy < 0:
                        direction[1] = -1
                    if dx == 0:
                        yComponent = 1
                        xComponent = 0
                    elif dy == 0:
                        xComponent = 1
                        yComponent = 0
                    else:
                        angle = np.arctan(np.abs(dy/dx))
                        xComponent = np.cos(angle)*direction[0]
                        yComponent = np.sin(angle)*direction[1]
                    #print('xcomp : ' + str(xComponent))
                    #print('ycomp : ' + str(yComponent))
                    if(mainPlayer.score > 100):
                        mainPlayer.shoot_bigBullet(x, y, xComponent, yComponent)
                        mainPlayer.score -= 100
        if(col < 8):
            mainPlayer.newColor(colorList[int(col)])
            col += 0.1
        else:
            col = 0
            mainPlayer.newColor(colorList[int(col)])

        if gotHit == False:
            screen.fill(BG_COLOR)
        else:
            screen.fill((25,0,0))
            gotHit = False
        if len(mainPlayer.bulletList)>0:
            for x in mainPlayer.bulletList:
                x.draw(screen)
                x.trajectory()
                if x.rect.top < 10 or x.rect.left < 10 or x.rect.bottom > SCREEN_HEIGHT-10 or x.rect.right > SCREEN_WIDTH-10:
                    mainPlayer.bulletList.remove(x)
                else:
                    for enemy in enemyList:
                        if(x.rect.colliderect(enemy.rect)):
                            if enemy.size > 30:
                                enemy.life -= x.damage
                            else:
                                enemy.life -= x.damage*3
                            enemy.hit()
                            mainPlayer.score += 1
                            #mainPlayer.bulletList.remove(x)
                            print(enemy.life)
        if len(enemyList) > 0:
            for enemy in enemyList:
                if(enemy.rect.colliderect(mainPlayer.rect)):
                    pygame.mixer.Sound('music/gothit.wav').play()
                    #screen.fill(255,0,0)
                    if enemy.size > 30:
                        mainPlayer.life -= 1
                    else:
                        mainPlayer.life -= 5
                    gotHit = True
                if enemy.life > 0:
                    enemy.update(screen)
                else:
                    pygame.mixer.Sound('music/enemyKill.wav').play()
                    playerScore += 100
                    enemyList.remove(enemy)
        if len(boostList) > 0:
            for boost in boostList:
                if(boost.rect.colliderect(mainPlayer.rect)):
                    pygame.mixer.Sound('music/powerup.wav').play()
                    #screen.fill(255,0,0)
                    mainPlayer.score += boost.score
                    mainPlayer.life += boost.life
                    boostList.remove(boost)
                boost.update(screen)
        mainPlayer.update(screen)
        ## ENEMY spawn
        if(int(time)%10 == 0):
            if(spawning == True):
                for i in range(0,(int(int(time)/10)*2+1)):
                    enemySpawn()
                if(int(time)%2 == 0):
                    spawnBoost()
                spawning = False

        elif(int(time)%11 == 1):
            spawning = True
        lifeBar.update(screen, mainPlayer.life)
        #timeDisplay = my_font.render(str(time),0, (255,255,255))
        #screen.blit(timeDisplay,(10,10))
        displayText(screen,my_font,time,mainPlayer.score)
        pygame.display.update()

game()
