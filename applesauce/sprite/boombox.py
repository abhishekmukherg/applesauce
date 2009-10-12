import pygame
import util


class Boombox(pygame.sprite.Sprite):
    
    def __init__(self, center, *groups):
        self.type = 'boombox'
        self.boombox = util.load_image( "boombox.png" )
        pygame.sprite.Sprite.__init__( self, *groups )
        self.rect = pygame.Rect( 0, 0, 38, 28 )
        self.bar = pygame.Surface( ( 75, 2 ) )
        self.bar.fill( ( 255, 0, 0 ) )
        self.bar_rect = self.bar.get_rect()
        self.time = 300
        self.sound = None
        
        self.rect.centerx = center[0]
        self.rect.centery = center[1] - 2
        
    @property
    def image(self):
        image = pygame.Surface( ( 38, 28 ), pygame.SRCALPHA, 32 ).convert_alpha()
        image.blit( self.boombox, self.boombox.get_rect() )
        image.blit( self.bar, self.bar.get_rect(), pygame.Rect( 0, 0, 38*(self.time/300.0), 2 ) )
        return image
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()