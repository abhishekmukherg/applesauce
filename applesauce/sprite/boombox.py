import pygame


class Boombox(pygame.sprite.Sprite):
    
    
    def __init__(self, *groups, center):
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = pygame.Surface( ( 10, 10 ) )
        self.image.fill( ( 255, 255, 255 ) ) #Temp till image
        self.rect = self.image.get_rect()
        self.bar = pygame.Surface( ( 10, 2 ) )
        self.bar.fill( ( 200, 0, 0 ) )
        self.bar_rect = self.bar.get_rect()
        self.time = 50
        self.sound = None
        
        self.rect.center = center
        self.bar_rect.bottom = self.rect.top - 2
        
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
        
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
        screen.blit( self.bar, self.bar_rect, pygame.Rect( 0, 0, self.time/5, 2 ) )