import pygame


class Boombox(pygame.sprite.Sprite):
    
    def __init__(self, center, *groups):
        self.type = 'boombox'
        pygame.sprite.Sprite.__init__( self, *groups )
        self.rect = pygame.Rect( 0, 0, 10, 14 )
        self.bar = pygame.Surface( ( 10, 2 ) )
        self.bar.fill( ( 255, 0, 0 ) )
        self.bar_rect = self.bar.get_rect()
        self.time = 200
        self.sound = None
        
        self.rect.centerx = center[0]
        self.rect.centery = center[1] - 2
        self.bar_rect.top = self.rect.top
        self.bar_rect.centerx = center[0]
        
    @property
    def image(self):
        image = pygame.Surface( ( 10, 14 ), pygame.SRCALPHA, 32 ).convert_alpha()
        image.blit( self.bar, self.bar.get_rect(), pygame.Rect( 0, 0, self.time/20, 2 ) )
        boombox = pygame.Surface( ( 10, 10 ) )
        boombox.fill( ( 255, 255, 255 ) )
        boombox_rect = boombox.get_rect()
        boombox_rect.top += 4
        image.blit( boombox, boombox_rect )
        return image
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
        screen.blit( self.bar, self.bar_rect, pygame.Rect( 0, 0, self.time/20, 2 ) )