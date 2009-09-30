
import pygame

import applesauce.sprite.player


class Game( object ):
    caption = "Applesauce"
    #level_data = 'level.dat'
    #background_image = 'images/FinalCity.png'
    #splash_image = 'images/MainScreen.png'
    #win_image = 'images/WinScreen.png'
    #lose_image = 'images/LoseScreen.png'
    #music = 'audio/CT_factory Ruins.ogg'
    screen_width = 800
    screen_height = 600
    
    
    def __init__( self ):
        pygame.init()
        pygame.display.set_caption( self.caption )
        
        self.state = 'splash'
        self.clock = pygame.time.Clock()
        #self.player = player.Player()
        self.enemy_list = []
        
        self.screen = pygame.display.set_mode( (self.screen_width, self.screen_height) )
        #self.background = pygame.image.load( self.bg_image ).convert()
        #self.splash = pygame.image.load( self.splash_image ).convert()
        #self.win = pygame.image.load( self.win_image ).convert()
        #self.lose = pygame.image.load( self.lose_image ).convert()
        #self.read_level( self.level_data )


    #def add_enemy( self, line_arr ):
        
        
    #def read_level( self, file_loc ):
    #    f = open( file_loc )
    #    for line in f:
    #        if line != "\n":
    #            string.replace( line, ' ', '' )
    #            line_arr = line.split( ',' )
                    

    def update( self ):
        self.clock.tick( 50 )
        for event in pygame.event.get():
            self.handle_event( event )
        #if self.state == 'act1' or self.state == 'act2':
        #    for enemy in self.enemy_list:
        #        enemy.update()
        #    self.player.update()
        

    def handle_event( self, event ):
        if event.type == pygame.QUIT:
            self.state = 'over'
        if event.type == pygame.KEYDOWN:
            if self.state == 'splash':
                self.state = 'act1'
            elif self.state == 'lose':
                self.state = 'over'
            elif event.key == pygame.K_ESCAPE:
                self.state = 'lose'
            elif event.key == pygame.K_F1:
                self.screen = pygame.display.set_mode( (self.screen_width, self.screen_height), pygame.FULLSCREEN ) 'right', True )
            #elif event.key == pygame.K_w:
            #    self.player.setMovement( 'up', True )
            #elif event.key == pygame.K_s:
            #    self.player.setMovement( 'down', True )
            #elif event.key == pygame.K_a:
            #    self.player.setMovement( 'left', True )
            #elif event.key == pygame.K_d:
            #    self.player.setMovement( 'right', True )
        #elif event.type == pygame.KEYUP:
        #    if event.key == pygame.K_w:
        #        self.player.setMovement( 'up', False )
        #    elif event.key == pygame.K_s:
        #        self.player.setMovement( 'down', False )
        #    elif event.key == pygame.K_a:
        #        self.player.setMovement( 'left', False )
        #    elif event.key == pygame.K_d:
        #        self.player.setMovement( 'right', False )
        

    def draw(self):
        self.screen.fill( (50, 50, 50) )
        
        #draw splash screen
        #if self.state == 'splash':
        #    
        #draw win screen
        #elif self.state == 'win':
        #
        #draw lose screen
        #elif self.state == 'lose':
        #
        #draw main game
        #else:
            #draw background
            #draw player
            #self.player.draw(self.screen)
            #draw enemies
            #for enemy in self.enemy_list:
            #    enemy.draw(self.screen)

        
        
def main(argv):
    g = Game()
    while g.state != 'over':
        g.update()
        g.draw()
        pygame.display.flip()
    #pygame.mixer.music.stop()
