import random
import os

import pygame
from pygame.constants import QUIT , K_DOWN , K_UP , K_LEFT , K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana',20)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0 , 0 , 0)
COLOR_BLUE = (0 , 0 , 255)
COLOR_GREEN = (0,255,0)

main_display = pygame.display.set_mode((WIDTH , HEIGHT))

back_ground = pygame.transform.scale(pygame.image.load('background.png'),(WIDTH,HEIGHT))
back_ground_x1 = 0
back_ground_x2 = back_ground.get_width()
back_ground_move = 3

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)



player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_move_down = [0,2]
player_move_up = [0,-2]
player_move_left = [-2,0]
player_move_right = [2,0]

def creat_eneme():
    enemy_size = (20,15)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH,random.randint(100,HEIGHT-100), *enemy_size)
    enemy_move = [random.randint(-8,-4),0]
    return [enemy , enemy_rect , enemy_move]


def creat_bonus():
    bonus_size = (15,20)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(150,WIDTH-400),0, *bonus_size)
    bonus_move = [0,random.randint(4,5)]
    return [bonus , bonus_rect , bonus_move]



CREAT_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREAT_ENEMY, 1500)

CREAT_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREAT_BONUS, 4000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE,200)

bonuses = []
enemies = []
score = 0
image_index = 0

playing = True
while True: 
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREAT_ENEMY:
            enemies.append (creat_eneme())
        if event.type == CREAT_BONUS:
            bonuses.append(creat_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0


    back_ground_x1 -= back_ground_move
    back_ground_x2 -= back_ground_move

    if back_ground_x1 < -back_ground.get_width():
        back_ground_x1 = back_ground.get_width()

    if back_ground_x2 < -back_ground.get_width():
        back_ground_x2 = back_ground.get_width()

    main_display.blit(back_ground,(back_ground_x1,0))
    main_display.blit(back_ground,(back_ground_x2,0))




    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])


        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))



    main_display.blit(FONT.render(str(score),True,COLOR_BLACK), (WIDTH-50,20))
    main_display.blit(player,player_rect)



    

    pygame.display.flip()


    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT :
            bonuses.pop(bonuses.index(bonus))