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

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, val):
        self.__state = val
        if val == "act1":
            self.level_config = "level_data/level0.ini"
        elif val == "act2":
            self.level_config = "level_data/level1.ini"
        elif val == "splash":
            self.level_config = "level_data/splash.ini"
        elif val == "info1":
            self.level_config = "level_data/info1.ini"
        elif val == "info2":
            self.level_config = "level_data/info2.ini"
        elif val == "info3":
            self.level_config = "level_data/info3.ini"
        elif val == "lose":
            self.level_config = "level_data/gameover.ini"
        elif val == "win":
            self.levl_config = "level_data/victory.ini"
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
        for location in self.level_config.player():
            LOG.debug("Adding player at %s" %str(location))
            self.level.add_player(
                    self.level_config.big(),
                    location[0],
                    location[1],
                    location[2],
                    location[3],
                    location[4])
        for location in self.level_config.basic_enemies():
            LOG.debug("Adding basic enemy at %s" % str(location))
            self.level.add_enemy(0, location)
        for location in self.level_config.officers():
            LOG.debug("Adding officer at %s" % str(location))
            self.level.add_enemy(1, location)
        for location in self.level_config.walls():
            self.level.add_wall(location)
        if self.level_config.hud_level() is not None:
            self.level.add_hud(self.level_config.hud_level())
     
    @property
    def caption(self):
        return pygame.display.get_caption()
        
    @caption.setter
    def caption(self, val):
        pygame.display.set_caption(val)
        
    def update( self ):
        self.clock.tick( 50 )
        if self.level.lives <= 0:
            self.state = 'lose'
        elif self.state == 'act1' and self.level.player.sprite.flyers == 0:
            self.state = 'act2'
        for event in pygame.event.get():
            self.handle_event( event )
        if self.state == 'act1' or self.state == 'act2':
            self.level.update()

    def handle_event( self, event ):
        if event.type == pygame.QUIT:
            self.state = 'over'
        player = self.level.player.sprite
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, pygame.FULLSCREEN )
            elif event.key == pygame.K_ESCAPE and self.state != 'lose':
                self.state = 'lose'
            elif self.state == 'splash':
                self.state = 'info1'
            elif self.state == 'info1':
                self.state = 'info2'
            elif self.state == 'info2':
                self.state = 'info3'
            elif self.state == 'info3':
                self.state = 'act1'
            elif self.state == 'lose':
                self.state = 'over'
            elif self.state == 'win':
                self.state = 'over'
            elif event.key == pygame.K_LEFT:
                self.level.add_boombox()
            elif event.key == pygame.K_UP:
                if self.state == 'act1':
                    self.level.add_flyer()
                #elif self.state == 'act2':
                #    self.level.add_bomb()
            elif event.key == pygame.K_RIGHT:
                self.level.add_turkeyshake()
            elif event.key == pygame.K_o:
                if self.level.draw_walls:
                    self.level.draw_walls = False
                else:
                    self.level.draw_walls = True
            elif event.key == pygame.K_w:
                player.movement['up'] = 1
            elif event.key == pygame.K_s:
                player.movement['down'] = 1
            elif event.key == pygame.K_a:
                player.movement['left'] = 1
            elif event.key == pygame.K_d:
                player.movement['right'] = 1
        elif event.type == pygame.KEYUP and (self.state == 'act1' or self.state == 'act2'):
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
        if self.level_config.magic_scroll():
            self.level.draw(self.screen)
        else:
            self.screen.blit(self.level.image, (0, 0))
        
        
g = Game()
while g.state != 'over':
    g.update()
    g.draw()
    pygame.display.flip()
#pygame.mixer.music.stop()
