import pygame
import math


class Player(pygame.sprite.Sprite):
    
    def __init__(self, location, constraint, flyers, bombs, boomboxes, turkeyshakes, *groups):
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = pygame.Surface( ( 50, 50 ) )
        self.rect = self.image.get_rect()
        self.constraint = constraint
        self.movement = { 'up':0, 'down':0, 'left':0, 'right':0 }
        self.facing = 'right'
        self.speed = 5
        self.flyers = flyers
        self.bombs = bombs
        self.boomboxes = boomboxes
        self.turkeyshakes = turkeyshakes
        self.contacting = ''
        
        self.rect.center = location
        
        
    def update(self):
        lr = False
        if self.movement['left'] == 1 and self.movement['right'] == 0:
            self.facing = 'left'
            lr = True
        elif self.movement['right'] == 1 and self.movement['left'] == 0:
            self.facing = 'right'
            lr = True
        if self.movement['up'] == 1 and self.movement['down'] == 0:
            if lr:
                self.facing += 'up'
            else:
                self.facing = 'up'
        if self.movement['down'] == 1 and self.movement['up'] == 0:
            if lr:
                self.facing += 'down'
            else:
                self.facing = 'down'
                
        self.speed = 5
        if self.movement['up'] ^ self.movement['down'] == 1 and self.movement['left'] ^ self.movement['right'] == 1:
            self.speed = math.sqrt( 12.5 )
        
        self.rect.move_ip( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
        
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
        
