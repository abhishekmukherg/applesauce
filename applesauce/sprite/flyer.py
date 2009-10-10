import pygame


class Flyer(pygame.sprite.Sprite):
    
    def __init__(self, location, direction, *groups):
        self.type = 'flyer'
        pygame.sprite.Sprite.__init__( self, *groups )
        if direction == 'up':
            self.image = pygame.Surface( ( 10, 3 ) )
        elif direction == 'down':
            self.image = pygame.Surface( ( 10, 3 ) )
        elif direction == 'left':
            self.image = pygame.Surface( ( 3, 10 ) )
        elif direction == 'right':
            self.image = pygame.Surface( ( 3, 10 ) )
        self.image.fill( ( 0, 255, 255 ) )
        self.rect = self.image.get_rect()
        
        self.rect.center = location
        
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )