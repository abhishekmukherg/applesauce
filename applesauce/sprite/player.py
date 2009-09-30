import collections

import pygame


class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        # TODO: defind self.image, self.rect
        self.movement = {'up':False, 'down':False, 'left':False, 'right':False}
        self.speed = 5
