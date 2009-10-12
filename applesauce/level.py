import copy
import itertools

import pygame

from applesauce import settings
from applesauce.sprite import util
from applesauce.sprite import player
from applesauce.sprite import enemies
from applesauce.sprite import boombox
from applesauce.sprite import wall
from applesauce.sprite import flyer
from applesauce.sprite import turkeyshake


class InvalidEnemyException(IndexError):

    """
    Raised when an invalid enemy index is given to add_enemy
    """
    
    def __init__(self, given, max):
        self.given = given
        self.max = max

    def __unicode__(self):
        return u"%d > %d" % (self.given, self.max)

    def __str__(self):
        return str(unicode(self))


class Level(object):

    def __init__(self, image):
        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.__image_name = image
        self.lives = 5

        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.others = pygame.sprite.Group()

        self.__groups = (self.player, self.enemies, self.walls, self.others)
        
        self.draw_walls = False
        
    def sprites(self):
        return tuple(itertools.chain(*self.__groups))
        
    def copy(self):
        new_level = Level(self.__image_name)
        new_level.player = copy.copy(self.player)
        new_level.enemies = copy.copy(self.enemies)
        new_level.walls = copy.copy(self.walls)
        new_level.pickups = copy.copy(self.pickups)
        new_level.others = copy.copy(self.others)
        new_level.__groups = (new_level.player, new_level.enemies,
                new_level.walls, new_level.pickups, new_level.others)
        return new_level
        
    def add_boombox(self):
        if self.player.sprite.boomboxes > 0:
            self.others.add( boombox.Boombox( self.player.sprite.rect.center ) )
            self.player.sprite.boomboxes -= 1
            
    def add_flyer(self):
        if self.player.sprite.flyers > 0:
            if self.player.sprite.contacting == 'up':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midtop, 'down' ) )
            elif self.player.sprite.contacting == 'down':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midbottom, 'up' ) )
            elif self.player.sprite.contacting == 'left':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midleft, 'right' ) )
            elif self.player.sprite.contacting == 'right':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midright, 'left' ) )
            self.player.sprite.flyers -= 1
        
    def add_turkeyshake(self):
        if self.player.sprite.turkeyshakes > 0:
            self.others.add( turkeyshake.Turkeyshake( self.player.sprite.rect.center, self.player.sprite.facing ) )
            self.player.sprite.turkeyshakes -= 1
            
    def add_player(self, location = (0,0), flyers = 0, bombs = 0, boomboxes = 0, turkeyshakes = 0):
        self.player.sprite = player.Player( location, self.rect, flyers, bombs, boomboxes, turkeyshakes )
            
    def add_wall(self, location = (0,0,0,0)):
        self.walls.add( wall.Wall( location[0], location[1], location[2], location[3] ) )

    def add_enemy(self, level, location=(0, 0)):
        """Adds an anemy to the level

        the level parameter can either be 0 or 1, 0 indicates a BasicEnemy,
        1 indicates an Officer will be added. location is in level-coordinates

        """
        if level == 0:
            enemy = enemies.BasicEnemy(self.player.sprite)
        elif level == 1:
            enemy = enemies.Officer(self.player.sprite)
        else:
            raise InvalidEnemyException(level, 1)
        enemy.rect.topleft = location
        self.enemies.add(enemy)
    
    def remove(self, *sprites):
        for sprite_iter in sprites:
            if not hasattr(sprite, '__iter__'):
                sprite_iter = [sprite_iter]
            for sprite in sprite_iter:
                for group in self.__groups:
                    group.remove(sprite)
                    
    def has(self, *sprites):
        for sprite_iter in sprites:
            if not hasattr(sprite, '__iter__'):
                sprite_iter = [sprite_iter]
            for sprite in sprite_iter:
                for group in self.__groups:
                    if sprite in group:
                        break
                else:
                    return False
        return True

    def update(self, *args):
        #self.enemy_collisions()
        for group in self.__groups:
            group.update(*args)
        self.player_collisions()
        self.other_collisions()
            
    def draw(self, surface):
        # Find location for player
        player_rect = self.player.sprite.rect
        rect = copy.copy(player_rect)
        rect.center = map(lambda x: x // 2, settings.SCREEN_SIZE)
        # blit background
        surface.blit(self.image, rect.move(-self.player.sprite.rect.left,
            -self.player.sprite.rect.top))
        if self.draw_walls == True:
            for group in (self.others, self.enemies, self.walls):
                for sprite in group:
                    loc = (-player_rect.left + sprite.rect.left,
                            -player_rect.top + sprite.rect.top)
                    surface.blit(sprite.image, rect.move(*loc))
        else:
            for group in (self.others, self.enemies):
                for sprite in group:
                    loc = (-player_rect.left + sprite.rect.left,
                            -player_rect.top + sprite.rect.top)
                    surface.blit(sprite.image, rect.move(*loc))
            
        # blit player
        surface.blit(self.player.sprite.image, rect)
            
    def player_collisions(self):
        player = self.player.sprite
        player.contacting = ''
        #constrain to screen
        tmp_rect = player.rect.move( player.speed*(player.movement['right']-player.movement['left']), player.speed*(player.movement['down']-player.movement['up']) )
        if not( player.constraint.contains( tmp_rect ) ):
            if tmp_rect.top < player.constraint.top:
                player.rect.top = player.constraint.top
            if tmp_rect.bottom > player.constraint.bottom:
                player.rect.bottom = player.constraint.bottom
            if tmp_rect.left < player.constraint.left:
                player.rect.left = player.constraint.left
            if tmp_rect.right > player.constraint.right:
                player.rect.right = player.constraint.right
                
        tmp_list = pygame.sprite.spritecollide( player, self.walls, False, pygame.sprite.collide_rect )
        for wall in tmp_list:
            if player.rect.bottom > wall.rect.bottom and (wall.rect.bottom - player.rect.top) <= player.speed:
                player.rect.top = wall.rect.bottom
                if player.facing.endswith( 'up' ) == True and player.rect.right <= wall.rect.right and player.rect.left >= wall.rect.left:
                    player.contacting = 'up'
            if player.rect.top < wall.rect.top and (player.rect.bottom - wall.rect.top) <= player.speed:
                player.rect.bottom = wall.rect.top
                if player.facing.endswith( 'down' ) == True and player.rect.right <= wall.rect.right and player.rect.left >= wall.rect.left:
                    player.contacting = 'down'
            if player.rect.right > wall.rect.right and (wall.rect.right - player.rect.left) <= player.speed:
                player.rect.left = wall.rect.right
                if player.facing.startswith( 'left' ) == True and player.rect.bottom <= wall.rect.bottom and player.rect.top >= wall.rect.top:
                    player.contacting = 'left'
            if player.rect.left < wall.rect.left and (player.rect.right - wall.rect.left) <= player.speed:
                player.rect.right = wall.rect.left
                if player.facing.startswith( 'right' ) == True and player.rect.bottom <= wall.rect.bottom and player.rect.top >= wall.rect.top:
                    player.contacting = 'right'
            
    # def enemy_collisions(self):
        # tmp = pygame.sprite.groupcollide( self.enemies, self.walls, False, False )
        # for enemy in self.enemies:
            # for wall in tmp[enemy]:
                # if enemy.rect.top < wall.rect.top:
                    # enemy.movement['up'] = 0
                # if enemy.rect.bottom > wall.rect.bottom:
                    # enemy.movement['down'] = 0
                # if enemy.rect.left < wall.rect.left:
                    # enemy.movement['left'] = 0
                # if enemy.rect.right > wall.rect.right:
                    # enemy.movement['right'] = 0
                    
    def other_collisions(self):
        for other in self.others:
            if other.type == 'turkeyshake' and pygame.sprite.spritecollideany( other, self.walls ):
                other.explode()

    def clear(self):
        for group in self.__groups:
            group.clear()
            
    def empty(self):
        return all(g.empty() for g in self.__groups)

    def __in__(self, obj):
        return self.has(obj)
        
    def __len__(self):
        return sum(len(g) for g in self.__groups)
        
    def __iter__(self):
        return itertools.chain(*self.__groups)
