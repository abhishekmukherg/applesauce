
import pygame

from applesauce.sprite import player, util


class Game( object ):
    caption = "Applesauce"
    #level_data = 'level.dat'
    level1_image = 'lvl1.png'
    level2_image = 'lvl2.png'
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
        self.player = player.Player()
        self.enemy_list = []
        
        self.screen = pygame.display.set_mode( (self.screen_width, self.screen_height) )
        self.level1 = util.load_image( self.level1_image )
        self.level2 = util.load_image( self.level2_image )
        #self.splash = util.load_image( self.splash_image )
        #self.win = util.load_image( self.win_image )
        #self.lose = util.load_image( self.lose_image )
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
        if self.state == 'act1' or self.state == 'act2':
        #    for enemy in self.enemy_list:
        #        enemy.update()
            self.player.update()
        

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
                self.screen = pygame.display.set_mode( (self.screen_width, self.screen_height), pygame.FULLSCREEN )
            elif event.key == pygame.K_w:
                self.player.movement['up'] = 1
            elif event.key == pygame.K_s:
                self.player.movement['down'] = 1
            elif event.key == pygame.K_a:
                self.player.movement['left'] = 1
            elif event.key == pygame.K_d:
                self.player.movement['right'] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.player.movement['up'] = 0
            elif event.key == pygame.K_s:
                self.player.movement['down'] = 0
            elif event.key == pygame.K_a:
                self.player.movement['left'] = 0
            elif event.key == pygame.K_d:
                self.player.movement['right'] = 0
        

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
        if self.state == 'act1': #else:
            #draw background
            self.screen.blit( self.level1, self.level1.get_rect() )
            #draw player
            self.player.draw(self.screen)
            #draw enemies
            #for enemy in self.enemy_list:
            #    enemy.draw(self.screen)

        
        
g = Game()
while g.state != 'over':
    g.update()
    g.draw()
    pygame.display.flip()
#pygame.mixer.music.stop()
