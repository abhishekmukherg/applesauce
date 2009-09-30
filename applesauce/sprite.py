import pygame

class Sprite( object ):


    def __init__( self, frames, time, texture, x = 0, y = 0 ):
        self.texture = texture
        self.rect = self.texture.get_rect()
        self.frames = frames
        self.time = time
        self.width = self.rect.width / self.frames
        self.height = self.rect.height
        self.frame = 0
        
        if not ( x == 0 and y == 0 ):
            self.rect.move_ip( x, y )
        
        
    def get_rect( self ):
        return self.rect
        
        
    def set_texture( self, texture ):
        self.texture = texture
        
        
    def move_ip( self, x, y ):
        self.rect.move_ip( x, y )
        
        
    def update( self ):
        self.frame += 1
        if self.frame > self.time:
            self.frame = 0
            
    
    def draw( self, screen ):
        screen.blit( self.texture, self.rect, pygame.Rect( self.width * (self.frame/self.frames), 0, self.width, self.height )