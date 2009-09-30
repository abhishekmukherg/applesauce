import pygame, sprite

class Player( object ):

    
    def __init__( self ):
        self.movement = {'up':False, 'down':False, 'left':False, 'right':False}
        #self.sprite = sprite.Sprite( 1, 10, pygame.image.load( 'images/' ).conver_alpha() )
        self.speed = 5
        
        
    def set_movement( self, direction, value ):
        self.movement[direction] = value
        
        
    #def update( self ):
        
        
    def draw( self, screen ):
        self.sprite.draw()