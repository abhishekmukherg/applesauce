import logging

import pygame

from applesauce import settings
from applesauce import level
from applesauce import level_config
from applesauce.sprite import util


LOG = logging.getLogger(__name__)


class InvalidStateException(Exception):
    
    def __init__(self, state):
        self.state = state

    def __unicode__(self):
        return unicode(self.state)

    def __str__(self):
        return str(unicode(self))


class Game( object ):
    def __init__( self ):
        pygame.init()
        self.caption = settings.CAPTION
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        self.level = None
        self.state = 'splash'
        
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

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, val):
        self.__state = val
        if val == "act1":
            self.level_config = "level_data/level0.ini"
        elif val == "splash":
            self.level_config = "level_data/splash.ini"
        elif val == "over":
            pass
        else:
            raise InvalidStateException(val)

    @property
    def level_config(self):
        return self.__level_config

    @level_config.setter
    def level_config(self, val):
        self.__level_config = level_config.LevelConfig(val)
        self.level = level.Level(self.level_config.image())
        self.populate_level()

    def populate_level(self):
        for location in self.level_config.basic_enemies():
            LOG.debug("Adding basic enemy at %s" % str(location))
            self.level.add_enemy(0, location)
        for location in self.level_config.officers():
            LOG.debug("Adding officer at %s" % str(location))
            self.level.add_enemy(1, location)
     
    @property
    def caption(self):
        return pygame.display.get_caption()
        
    @caption.setter
    def caption(self, val):
        pygame.display.set_caption(val)

        
    def update( self ):
        self.clock.tick( 50 )
        for event in pygame.event.get():
            self.handle_event( event )
        if self.state == 'act1' or self.state == 'act2':
            self.level.update()
        

    def handle_event( self, event ):
        if event.type == pygame.QUIT:
            self.state = 'over'
        player = self.level.player.sprite
        if event.type == pygame.KEYDOWN:
            if self.state == 'splash':
                self.state = 'act1'
            elif self.state == 'lose':
                self.state = 'over'
            elif event.key == pygame.K_ESCAPE:
                self.state = 'lose'
            elif event.key == pygame.K_F1:
                self.screen = pygame.display.set_mode(settings.SCREEN_SIZE,
                                                      pygame.FULLSCREEN )
            elif event.key == pygame.K_LEFT:
                self.level.add_boombox()
            elif event.key == pygame.K_w:
                player.movement['up'] = 1
            elif event.key == pygame.K_s:
                player.movement['down'] = 1
            elif event.key == pygame.K_a:
                player.movement['left'] = 1
            elif event.key == pygame.K_d:
                player.movement['right'] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.movement['up'] = 0
            elif event.key == pygame.K_s:
                player.movement['down'] = 0
            elif event.key == pygame.K_a:
                player.movement['left'] = 0
            elif event.key == pygame.K_d:
                player.movement['right'] = 0
        

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
            self.level.draw(self.screen)
            #draw player
            #draw enemies
            #for enemy in self.enemy_list:
            #    enemy.draw(self.screen)

        
        
g = Game()
while g.state != 'over':
    g.update()
    g.draw()
    pygame.display.flip()
#pygame.mixer.music.stop()
