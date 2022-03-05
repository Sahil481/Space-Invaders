import pygame
import random
import math
from pygame import mixer

pygame.init()

s = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
score_shown = 0
over_font = pygame.font.Font('freesansbold.ttf', 64)
title = pygame.font.Font('freesansbold.ttf', 64)
start = pygame.font.Font('freesansbold.ttf', 32)
restart_text_text = pygame.font.Font('freesansbold.ttf', 32)
restarted = 'no'
def show_score(x, y):
    score = font.render('score :' + str(score_value), True, (255, 255, 255))
    s.blit(score, (x, y))

def game_over_text(x, y):
    over_text = over_font.render('Game Over!', True, (255, 255, 255))
    s.blit(over_text, (200, 250))

def title_font(x, y):
    title_text = title.render('Space Invaders', True, (255, 255, 255))
    s.blit(title_text, (175, 175))

def start_font(x, y):
    start_text = start.render('Press F to start', True, (255, 255, 255))
    s.blit(start_text, (290, 250))

def restart_font_font(x, y):
    restart_text = restart_text_text.render('Press R to restart', True, (255, 255, 255))
    s.blit(restart_text, (260, 320))

def player(x, y):
    s.blit(playerImg, (x, y))


def enemy(x, y, i):
    s.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    s.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
def game():
    global score_value, running,bulletX, bulletY, playerX, bullet_state, playerX_change, restarted, running3, score_shown
    while running:
        s.fill((0, 0, 0))
        s.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    playerX_change = -5
                if event.key == pygame.K_d:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        for i in range(num_of_enemy):
            if enemyY[i] > 440:
                for j in range(num_of_enemy):
                    enemyY[j] = 2000
                game_over_text(250, 250)
                restart_font_font(250, 250)
                if score_shown == 0:
                    print(score_value)
                    score_shown += 1
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 1
                enemyX[i] = random.randint(0, 730)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'

        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()

running2 = True
while running2:
    s.blit(background, (0, 0))
    title_font(250, 250)
    start_font(250, 250)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                game()
                running2 = False

    pygame.display.update()

print('your score:', score_value)