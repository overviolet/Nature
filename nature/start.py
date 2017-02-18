# -*- coding: utf-8 -*-

import pygame
import os
import time
import random


x_limit = 400
y_limit = 400
window = pygame.display.set_mode((x_limit, y_limit))
pygame.display.set_caption('Nature: Ground Boost')
screen = pygame.Surface((x_limit, y_limit))

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def intrsect(s1_x, s2_x, s1_y, s2_y, sprite_size):
    if ((s1_x > s2_x-sprite_size) and (s1_x < s2_x+sprite_size) and
       (s1_y > s2_y - sprite_size) and (s1_y < s2_y + sprite_size)):

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

    def move(self, direction):
        if 'up' in direction:
            self.y -= 1
        if 'dn' in direction:
            self.y += 1
        if 'lf' in direction:
            self.x -= 1
        if 'rt' in direction:
            self.x += 1


hero = Sprite(350, 200, 'resources/images/sprites/demo/picachu_40')
hero.up = True
zet = Sprite(10, 20, 'resources/images/sprites/demo/bluman_40')
zet.up = True
#cat = Sprite(80, 0, 'resources/images/sprites/demo/catwoman_40')

done = True
while done:
    for e in pygame.event.get():
        #print str(e)
        if e.type == pygame.QUIT:
            done = False

    screen.fill((0, 100, 100))

    if hero.up == True:
        hero.move('up')
        if hero.y == 0:
            hero.up = False
    else:
        hero.move('dn')
        if hero.y == 360:
            hero.up = True

    if zet.up == True:
        zet.move('up')
        if zet.y == 0:
            zet.up = False
    else:
        zet.move('dn')
        if zet.y == 360:
            zet.up = True

    if intrsect(hero.x, zet.x, hero.y, zet.y, 40):
        hero.up = not hero.up
        zet.up = not zet.up



    hero.render()
    zet.render()
    #cat.render()

    window.blit(screen, (0, 0))
    pygame.display.flip()
    pygame.time.delay(5)