import math
import util

import pygame

from applesauce.sprite import effects


class Player(effects.SpriteSheet):
    
    def __init__(self, big, location, constraint, flyers, bombs, boomboxes, turkeyshakes, *groups):
        if big == True:
            effects.SpriteSheet.__init__(self, util.load_image( "playerBigMove_sheet.png" ), (60,90) )
            self.max_speed = 5
        else:
            effects.SpriteSheet.__init__(self, util.load_image( "playerMove_sheet.png" ), (30,45) )
            self.max_speed = 4
        self.constraint = constraint
        self.movement = { 'up':0, 'down':0, 'left':0, 'right':0 }
        self.facing = 'right'
        self.flyers = flyers
        self.bombs = bombs
        self.boomboxes = boomboxes
        self.turkeyshakes = turkeyshakes
        self.contacting = ''
        self.time = 0
        self.anim_frame = 0
        self.state = 0
        self.flipped = False
        self.booltop = True
        self.wait = 0
        self.bomb_place = False
        self.placing = 0
        self.end = False
        
        self.rect.center = location
        if big:
            self.rect.height -= 45
        else:
            self.rect.height -= 22.5
        
    @property
    def booltop(self):
        return self._booltop
        
    @booltop.setter
    def booltop(self, val):
        self._booltop = val
        if val == True:
            self.rect.bottom = self.rect.top
        else:
            self.rect.top = self.rect.bottom
        
    def update(self):
        self.just_placed = False
        if self.bomb_place == False:
            self.placing = 0
        if self.wait > 0:
            self.wait -= 1
            return
        if self.placing > 0:
            self.placing += 1
            return
        lr = False
        if self.movement['left'] == 1 and self.movement['right'] == 0:
            self.facing = 'left'
            lr = True
            if self.flipped == False:
                self.image = pygame.transform.flip( self.image, True, False )
                self.flipped = True
        elif self.movement['right'] == 1 and self.movement['left'] == 0:
            self.facing = 'right'
            lr = True
            if self.flipped == True:
                self.image = pygame.transform.flip( self.image, True, False )
                self.flipped = False
        if lr:
            self.state = 2
        if self.movement['up'] == 1 and self.movement['down'] == 0:
            if lr:
                self.facing += 'up'
                self.state = 1
            else:
                self.facing = 'up'
                self.state = 0
        if self.movement['down'] == 1 and self.movement['up'] == 0:
            if lr:
                self.facing += 'down'
                self.state = 3
            else:
                self.facing = 'down'
                self.state = 4
        if self.movement['up']==1 or self.movement['down']==1 or self.movement['left']==1 or self.movement['right']==1:
            if self.flipped == True:
                self.time -= 1
            else:
                self.time += 1
            self.anim_frame = self.time / 2
            if self.anim_frame > 11:
                self.time = 0
                self.anim_frame = 0
            elif self.anim_frame < 0:
                self.time = 2 * 11
                self.anim_frame = 11
                
        vector = (self.movement['right'] - self.movement['left'],
                  self.movement['down'] - self.movement['up'])
        def length(a, b):
            return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
        vec_length = length(*vector)
        if vec_length != 0:
            vector = map(lambda x: x * self.max_speed / vec_length, vector)
        self.speed = length(*vector)
        self.rect.move_ip(*vector)
        
    
    def draw(self, screen):
        screen.blit( pygame.surface((800,600)), self.rect, self.rect )
        
