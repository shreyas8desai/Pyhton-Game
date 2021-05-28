import pygame
from pygame.locals import *
import sys
import random

# Global Variables & Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_IMAGES = {}
GAME_SOUNDS = {}
baseX = 0
baseY = SCREEN_HEIGHT * 0.85
playerX = SCREEN_WIDTH/5
playerY = SCREEN_HEIGHT/2
# functions start from here
def welcomeScreen():
    while True:
        messageX = SCREEN_WIDTH/2 - GAME_IMAGES["message"].get_width()/2
        messageY = SCREEN_HEIGHT * 0.15
        SCREEN.blit(GAME_IMAGES["background"], (0, 0))
        SCREEN.blit(GAME_IMAGES["base"], (baseX, baseY))
        SCREEN.blit(GAME_IMAGES["player"], (playerX, playerY))
        SCREEN.blit(GAME_IMAGES["message"], (messageX, messageY))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return
                
def gameLoop():
    score = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    playerX = SCREEN_WIDTH/5
    playerY = SCREEN_HEIGHT/2
    # upper pipes
    upperPipes = [
        {"x" : SCREEN_WIDTH, "y" : newPipe1[0]["y"]},
        {"x" : SCREEN_WIDTH + SCREEN_WIDTH/2, "y" : newPipe2[0]["y"]}
    ]

    # lower pipes
    lowerPipes = [
        {"x" : SCREEN_WIDTH, "y" : newPipe1[1]["y"]},
        {"x" : SCREEN_WIDTH + SCREEN_WIDTH/2, "y" : newPipe2[1]["y"]}
    ]

    pipeSpeedX = -4
    playerSpeedY = -5
    playerMaxSpeed = 10
    playerAccY = 1
    playerFlyingSpeedY = -5
    playerFlying = False

    playerHeight = GAME_IMAGES["player"].get_height()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_UP:
                if playerY > 0:
                    playerSpeedY = playerFlyingSpeedY
                    playerFlying = True
                    GAME_SOUNDS["fly"].play()
        
        # Moving Player up
        if playerFlying == True:
            playerFlying = False
        playerY = playerY + playerSpeedY

        # Pulling player down
        if playerSpeedY < playerMaxSpeed and not playerFlying:
            playerSpeedY = playerSpeedY + playerAccY

        # Die
        hit = isHit(playerX, playerY, upperPipes, lowerPipes)
        if hit:
            GAME_SOUNDS["die"].play()
            return

        # Changing the score
        playerCenter = playerX + GAME_IMAGES["player"].get_width()/5
        for pipe in upperPipes:
            pipeCenter = pipe["x"] + GAME_IMAGES["pipe"][0].get_width()/5
            if pipeCenter <= playerCenter < pipeCenter + 4:
                score = score + 1
                GAME_SOUNDS["point"].play()
                print("Score:", score)

        # Moving the pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] = upperPipe["x"] + pipeSpeedX
            lowerPipe["x"] = lowerPipe["x"] + pipeSpeedX

        # Adding new pipes
        if 0 < upperPipes[0]["x"] < 5 :
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # Removing old pipes
        if upperPipes[0]["x"] < 0:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Blitting our stuff
        SCREEN.blit(GAME_IMAGES["background"], (0, 0))
        SCREEN.blit(GAME_IMAGES["player"], (playerX, playerY))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMAGES["pipe"][0], (upperPipe["x"], upperPipe["y"]))
            SCREEN.blit(GAME_IMAGES["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))
        SCREEN.blit(GAME_IMAGES["base"], (baseX, baseY))
        # blitting the score
        scoreDigits = [int(x) for x in list(str(score))]
        scoreX = SCREEN_WIDTH/1.1
        for digit in scoreDigits:
            SCREEN.blit(GAME_IMAGES["numbers"][digit], (scoreX, SCREEN_HEIGHT*0.80))
            scoreX =+ scoreX + GAME_IMAGES["numbers"][digit].get_width()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)

def isHit(playerX, playerY, upperPipes, lowerPipes):
    # hitting the ceiling or base
    if playerY < 0 or playerY > baseY:
        return True
    
    # hitting upper pipes
    for pipe in upperPipes:
        pipeHeight = GAME_IMAGES["pipe"][0].get_height()
        if (playerY < pipeHeight + pipe["y"] and abs(playerX-pipe["x"]) < GAME_IMAGES["pipe"][0].get_width()):
            return True

    # hitting lower pipes
    for pipe in lowerPipes:
        if (playerY + GAME_IMAGES["player"].get_height() > pipe["y"]) and abs(playerX - pipe["x"]) < GAME_IMAGES["pipe"][0].get_width():
            return True

    return False

def getRandomPipe():
    pipeHeight = GAME_IMAGES["pipe"][0].get_height()
    gap = GAME_IMAGES["player"].get_height() * 3
    y2 = random.randint(gap, SCREEN_HEIGHT - GAME_IMAGES["base"].get_height())
    y1 = y2 - gap - pipeHeight
    pipeX = SCREEN_WIDTH
    pipe = [
        { "x" : pipeX, "y" : y1 },
        { "x" : pipeX, "y" : y2 }
    ]
    return pipe

# main program starts from here
pygame.init()
pygame.display.set_caption("Royal Bird")
GAME_IMAGES["background"] = pygame.image.load("images/background.png").convert_alpha()
GAME_IMAGES["base"] = pygame.image.load("images/base.png").convert_alpha()
GAME_IMAGES["player"] = pygame.image.load("images/bird.png").convert_alpha()
GAME_IMAGES["message"] = pygame.image.load("images/message.png").convert_alpha()
GAME_IMAGES["numbers"] = (
    pygame.image.load("images/0.png").convert_alpha(),
    pygame.image.load("images/1.png").convert_alpha(),
    pygame.image.load("images/2.png").convert_alpha(),
    pygame.image.load("images/3.png").convert_alpha(),
    pygame.image.load("images/4.png").convert_alpha(),
    pygame.image.load("images/5.png").convert_alpha(),
    pygame.image.load("images/6.png").convert_alpha(),
    pygame.image.load("images/7.png").convert_alpha(),
    pygame.image.load("images/8.png").convert_alpha(),
    pygame.image.load("images/9.png").convert_alpha()
)
GAME_IMAGES["pipe"] = (
    pygame.transform.rotate(pygame.image.load("images/pipe.png").convert_alpha(), 180),
    pygame.image.load("images/pipe.png").convert_alpha()
)
GAME_SOUNDS["die"] = pygame.mixer.Sound("audio/die.wav")
GAME_SOUNDS["fly"] = pygame.mixer.Sound("audio/fly.wav")
GAME_SOUNDS["point"] = pygame.mixer.Sound("audio/point.wav")
while True:
    welcomeScreen()
    gameLoop()