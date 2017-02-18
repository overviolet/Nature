# -*- coding: utf-8 -*-

import pygame
import os
import time
import random

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def intrsect(s1_x, s2_x, s1_y, s2_y, s1_x_size, s2_x_size, s1_y_size, s2_y_size):
    if ((s1_x > s2_x - s1_x_size) and (s1_x < s2_x + s2_x_size) and
       (s1_y > s2_y - s1_y_size) and (s1_y < s2_y + s2_y_size)):

        return True
    else:
        return False

class Sprite:
    def __init__(self, xpos, ypos, images_path):
        self.x = xpos
        self.y = ypos
        self.sprite_set = [(os.path.join(images_path, f)) for f in os.listdir(images_path)
                           if os.path.isfile(os.path.join(images_path, f)) and '.png' in f]
        self.sprite_set.sort()
        self.bitmap_counter_max = len(self.sprite_set) - 1
        self.bitmap_counter = random.randrange(0, self.bitmap_counter_max + 1)
        self.bitmap = pygame.image.load(self.sprite_set[self.bitmap_counter])
        self.bitmap_change_period = 0.2
        self.bitmap_last_change_timestamp = 0
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        if self.bitmap_last_change_timestamp + self.bitmap_change_period < time.time():
            self.bitmap_counter = self.bitmap_counter + 1 if self.bitmap_counter < self.bitmap_counter_max else 0
            self.bitmap_last_change_timestamp = time.time()
        screen.blit(pygame.image.load(self.sprite_set[self.bitmap_counter]), (self.x, self.y))

    def move(self, direction, step=1):
        if 'up' in direction:
            self.y -= step
        if 'dn' in direction:
            self.y += step
        if 'lf' in direction:
            self.x -= step
        if 'rt' in direction:
            self.x += step

    def set_invisible(self):
        self.x = -40
        self.y = 350

x_limit = 400
y_limit = 430
window = pygame.display.set_mode((x_limit, y_limit))
pygame.display.set_caption('Nature: Ground Boost')
screen = pygame.Surface((400, 400))


hero = Sprite(200, 350, 'resources/images/sprites/demo/picachu_40')
hero.score = 0
zet = Sprite(10, 10, 'resources/images/sprites/demo/bluman_40')
zet.left = True
zet.hardness = 1
arrow = Sprite(-40, 350, 'resources/images/sprites/demo/arrow_13_40')
arrow.push = False
arrow.bet = 0
arrow.goal = '-'
info_string = pygame.Surface((400, 30))
pygame.font.init()
speed_font = pygame.font.Font(None, 16)


done = True
pygame.key.set_repeat(1, 1)
while done:
    for e in pygame.event.get():
        #print str(e)
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                if hero.x > 10:
                    hero.move('lf', 1)
            if e.key == pygame.K_RIGHT:
                if hero.x < 350:
                    hero.move('rt', 1)
            if e.key == pygame.K_UP:
                if hero.y > 150:
                    hero.move('up', 1)
            if e.key == pygame.K_DOWN:
                if hero.y < 350:
                    hero.move('dn', 1)
            if e.key == pygame.K_SPACE:
                if not arrow.push:
                    arrow.x = hero.x + 13
                    arrow.y = hero.y
                    arrow.push = True
                    arrow.bet = arrow.y - zet.y
        if e.type == pygame.MOUSEMOTION:
            pygame.mouse.set_visible(False)
            m = pygame.mouse.get_pos()
            if m[0] > 10 and m[0] < 350:
                hero.x = m[0]
            if m[1] > 150 and m[1] < 350:
                hero.y = m[1]
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if not arrow.push:
                    arrow.x = hero.x + 13
                    arrow.y = hero.y
                    arrow.push = True
                    arrow.bet = arrow.y - zet.y





    screen.fill((0, 100, 100))
    info_string.fill((0, 50, 30))

    if zet.left == True:
        zet.move('lf', zet.hardness)
        if zet.x <= 0:
            zet.left = False
    else:
        zet.move('rt', zet.hardness)
        if zet.x >= 360:
            zet.left = True

    if arrow.y < 0:
        arrow.push = False
        hero.score -= int(arrow.bet/(2*zet.hardness))
        arrow.bet = 0
        arrow.goal = 'v'

    if intrsect(arrow.x, zet.x, arrow.y, zet.y, 13, 40, 40, 40):
        arrow.push = False
        zet.hardness += 0.1
        hero.score += int(arrow.bet*zet.hardness)
        arrow.bet = 0
        arrow.goal = '˄'



    if not arrow.push:
        arrow.set_invisible()
    else:
        arrow.move('up')

    hero.render()
    zet.render()
    arrow.render()
    info_string.blit(speed_font.render('Speed: {} '.format(zet.hardness), 1, (210, 120, 200)), (250, 5))
    info_string.blit(speed_font.render('Score: {} {} shot: +{} -{}'.format(hero.score,
                                                                       arrow.goal,
                                                                       int(arrow.bet*zet.hardness),
                                                                       int(arrow.bet/(2*zet.hardness))),
                                       1, (210, 120, 200)), (10, 5))


    window.blit(info_string, (0, 0))
    window.blit(screen, (0, 30))
    pygame.display.flip()
    pygame.time.delay(5)