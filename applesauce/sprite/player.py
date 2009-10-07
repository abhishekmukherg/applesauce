import pygame


class Player(pygame.sprite.Sprite):
    
    
    def __init__(self, constraint, *groups):
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = pygame.Surface( ( 50, 50 ) )
        self.rect = self.image.get_rect()
        self.constraint = constraint
        self.movement = { 'up':0, 'down':0, 'left':0, 'right':0 }
        self.facing = 'right'
        self.speed = 5
        self.lives = 3
        self.fliers = 10
        self.boomboxes = 0
        self.turkyshakes = 0
        
        
    def update(self):
        self.rect.move_ip( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
        
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
        
