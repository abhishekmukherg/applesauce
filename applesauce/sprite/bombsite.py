import pygame


class Bombsite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, x2, y2, *groups):
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = pygame.Surface( ( x2 - x, y2 - y ) )
        self.image.fill( ( 180, 0, 0 ) )
        self.rect = pygame.Rect( x, y, x2 - x, y2 - y )
        
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )