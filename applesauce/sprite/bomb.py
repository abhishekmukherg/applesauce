import weakref

import pygame

from applesauce import settings
from applesauce.sprite import util


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, center, *groups):
        self.type = 'bomb'
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = util.load_image( "bomb.png" )
        self.rect = self.image.get_rect()
        
        self.rect.center = center
        
    def update(self):
        pass
