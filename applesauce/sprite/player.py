import collections

import pygame


class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        # TODO: defind self.image, self.rect
        self.image = pygame.Surface((50,50))
        self.rect = self.image.get_rect()
        self.movement = {'up':0, 'down':0, 'left':0, 'right':0}
        self.speed = 5
        
    def update(self):
        self.rect.move_ip( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
        
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
        