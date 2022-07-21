import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screenWidth = 432
screenHeight = 705

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Flappy Bird')

# load sprites
bg = pygame.image.load("img/bg.png")
bg = pygame.transform.scale(bg, (432, 540))

ground = pygame.image.load("img/ground.png")
ground = pygame.transform.scale(ground, (432 + 36, 175))

# define game variables
groundScroll = 0
scrollSpeed = 2
flying = False
gameOver = False
pipeGap = 200
pipeFrequency = 2500 # milliseconds
lastPipe = pygame.time.get_ticks() - pipeFrequency

class Pipe(pygame.sprite.Sprite):
    def __init__ (self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        # position 1 from the top, position -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipeGap) / 2]
        if position == -1:
            self.rect.topleft = [x, y + int(pipeGap) / 2]

    def update(self):
        self.rect.x -= scrollSpeed
        if(self.rect.right < 0):
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0

        for num in range(1,4):
            img = pygame.image.load(f"img/y_b_{num}.png")
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 540:
                self.rect.y += int(self.vel)

        if gameOver == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel -= 10

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flappyCooldown = 15
            while self.counter > flappyCooldown:
                self.counter = 0
                self.index += 1 
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], -self.vel * 2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

# groups sprites
birdGroup = pygame.sprite.Group()
pipeGroup = pygame.sprite.Group()

firstFlappy = Bird(75, int(screenHeight) / 2)
birdGroup.add(firstFlappy)

run = True
while run:

    clock.tick(fps)

    # draw the background
    screen.blit(bg, (0, 0))

    # draw the bird
    birdGroup.draw(screen)
    birdGroup.update()

    # draw the pipe
    pipeGroup.draw(screen)

    # draw the ground
    screen.blit(ground, (groundScroll, 540))

    # look for collision
    if pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False) or firstFlappy.rect.top < 0:
        gameOver = True
    # check in bird hit the ground
    if firstFlappy.rect.bottom >= 540:
        gameOver = True
        flying = False

    if gameOver == False and flying == True:
        # generate new pipes
        timeNow = pygame.time.get_ticks()
        if timeNow - lastPipe > pipeFrequency:
            pipeHeight =  random.randint(-160, 40)
            topPipe = Pipe(screenWidth, int(screenHeight) / 2 + pipeHeight, 1)
            btmPipe = Pipe(screenWidth, int(screenHeight) / 2 + pipeHeight, -1)
            pipeGroup.add(topPipe)
            pipeGroup.add(btmPipe)
            lastPipe = timeNow

        #scroll  the ground
        groundScroll -= scrollSpeed
        if abs(groundScroll) > 35:
            groundScroll = 0

        pipeGroup.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
            flying = True
    
    pygame.display.update()

pygame.quit()
