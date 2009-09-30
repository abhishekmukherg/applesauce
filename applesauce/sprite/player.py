import collections

import pygame


class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups, constraint):
        pygame.sprite.Sprite.__init__(self, *groups)
        # TODO: defind self.image, self.rect
        self.image = pygame.Surface((50,50))
        self.rect = self.image.get_rect()
        self.constraint = constraint
        self.movement = {'up':0, 'down':0, 'left':0, 'right':0}
        self.facing = 'right'
        self.speed = 5
        self.lives = 3
        self.fliers = 10
        self.boombox = None
        self.turkyshake = None
        
        
    def update(self):
        tmprect = self.rect.move( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
        if not(self.constraint.contains(tmprect)):
            if tmprect.top < self.constraint.top:
                self.movement['up'] = 0
            if tmprect.bottom > self.constraint.bottom:
                self.movement['down'] = 0
            if tmprect.left < self.constraint.left:
                self.movement['left'] = 0
            if tmprect.right > self.constraint.right:
                self.movement['right'] = 0
        self.rect.move_ip( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
        
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
        