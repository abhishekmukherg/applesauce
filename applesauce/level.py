from __future__ import division

import copy
import itertools
import math
import logging

import pygame

from applesauce import settings
from applesauce.sprite import util
from applesauce.sprite import player
from applesauce.sprite import enemies
from applesauce.sprite import boombox
from applesauce.sprite import wall
from applesauce.sprite import flyer
from applesauce.sprite import turkeyshake
from applesauce.sprite import hud
from applesauce.sprite import bomb
from applesauce.sprite import bombsite
from applesauce.sprite import door


LOG = logging.getLogger(__name__)


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

    def __init__(self, image, big, respawn):
        self.big = big
        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.__image_name = image
        self.lives = 5
        self.respawn = respawn
        self.bbar = pygame.Surface((202, 22))
        self.bbar.fill((220,220,220))
        self.bar = pygame.Surface((200,20))
        self.bar.fill((100,0,0))

        self.hud = pygame.sprite.GroupSingle()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bombsites = pygame.sprite.Group()
        self.others = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        self.__groups = (self.player,
                         self.enemies,
                         self.walls,
                         self.others,
                         self.doors)
        
        self.draw_walls = False
        
    def sprites(self):
        return tuple(itertools.chain(*self.__groups))
        
    def copy(self):
        new_level = Level(self.__image_name)
        new_level.player = copy.copy(self.player)
        new_level.enemies = copy.copy(self.enemies)
        new_level.walls = copy.copy(self.walls)
        new_level.bombsites = copy.copy(self.bombsites)
        new_level.others = copy.copy(self.others)
        new_level.__groups = (new_level.player, new_level.enemies,
                new_level.walls, new_level.bombsites, new_level.others)
        return new_level
        
    def add_boombox(self):
        if self.player.sprite.boomboxes > 0:
            self.others.add(boombox.Boombox( self.big, self.player.sprite.rect.center, self.enemies))
            self.player.sprite.boomboxes -= 1
            
    def add_flyer(self):
        if self.player.sprite.flyers > 0:
            if self.player.sprite.contacting == 'up':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midtop, 'down' ) )
                self.player.sprite.flyers -= 1
            elif self.player.sprite.contacting == 'down':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midbottom, 'up', self.player.sprite.rect.height ) )
                self.player.sprite.flyers -= 1
            elif self.player.sprite.contacting == 'left':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midleft, 'right' ) )
                self.player.sprite.flyers -= 1
            elif self.player.sprite.contacting == 'right':
                self.others.add( flyer.Flyer( self.player.sprite.rect.midright, 'left' ) )
                self.player.sprite.flyers -= 1
                
    def add_bombsite(self, location = (0,0,0,0)):
        self.bombsites.add( bombsite.Bombsite( location[0], location[1], location[2], location[3] ) )
        
    def add_turkeyshake(self):
        if self.player.sprite.turkeyshakes > 0:
            self.others.add( turkeyshake.Turkeyshake( self.big, self.player.sprite.rect.center, self.player.sprite.facing ) )
            self.player.sprite.turkeyshakes -= 1
            
    def add_bomb(self, value):
        if value == True and self.player.sprite.bomb_place == True:
            self.player.sprite.placing = 1
        else:
            self.player.sprite.placing = 0
            
    def add_player(self, location = (0,0), flyers = 0, bombs = 0, boomboxes = 0, turkeyshakes = 0):
        self.player.add(player.Player(
            self.big,
            location,
            self.rect,
            flyers,
            bombs,
            boomboxes,
            turkeyshakes))

    def add_hud(self, level):
        self.hud.add(hud.Hud(self.player.sprite, level, lambda: self.lives))
        self.hud.sprite.bottom_right = settings.SCREEN_SIZE
            
    def add_wall(self, location = (0,0,0,0)):
        self.walls.add( wall.Wall( location[0], location[1], location[2], location[3] ) )

    def add_door(self, location, horizontal):
        self.doors.add(door.Door(location, horizontal))

    def add_enemy(self, level, location=(0, 0)):
        """Adds an anemy to the level

        the level parameter can either be 0 or 1, 0 indicates a BasicEnemy,
        1 indicates an Officer will be added. location is in level-coordinates

        """
        if level == 0:
            enemy = enemies.BasicEnemy(self.big, location, self.player.sprite, self.walls)
        elif level == 1:
            enemy = enemies.Officer(
                    self.big,
                    location,
                    self.player.sprite,
                    self.walls,
                    self.enemies)
        else:
            raise InvalidEnemyException(level, 1)
        self.enemies.add(enemy)

    def touch_door(self):
        LOG.debug("Touching nearest door in %s" % str(self.doors))
        for sprite in self.doors:
            if pygame.sprite.collide_rect_ratio(1.5)(sprite, 
                    self.player.sprite):
                LOG.debug("Moving %s" % str(sprite))
                sprite.moving = True
                return
    
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
        self.player.sprite.booltop = False
        #self.enemy_collisions()
        for group in self.__groups:
            group.update(*args)
        if self.player.sprite.placing == 200:
            self.player.sprite.placing = 0
            self.others.add( bomb.Bomb( self.player.sprite.rect.center ) )
            self.player.sprite.bombs -= 1
            self.player.sprite.just_placed = True
        self.player_collisions()
        self.other_collisions()
            
    def draw(self, surface):
        # Find location for player
        self.player.sprite.booltop = True
        player_rect = self.player.sprite.rect
        rect = copy.copy(player_rect)
        rect.center = map(lambda x: x // 2, settings.SCREEN_SIZE)
        # blit background
        surface.blit(self.image, rect.move(-self.player.sprite.rect.left,
            -self.player.sprite.rect.top))
        def rect_radius(rect):
            a = rect.width / 2
            b = rect.height / 2
            return math.sqrt(a * a + b * b)
        for sprite in self.enemies:
            if hasattr(sprite, 'allerted') and sprite.allerted:
                loc = (-player_rect.left + sprite.rect.left,
                        -player_rect.top + sprite.rect.top)
                pygame.draw.circle(surface,
                        (255, 0, 0),
                        rect.move(*loc).center,
                        rect_radius(sprite.rect) + 5,
                        5)

        groups = [self.bombsites, self.others, self.enemies, self.doors]
        if self.draw_walls:
            groups.append(self.walls)
        
        for group in groups:
            for sprite in group:
                loc = (-player_rect.left + sprite.rect.left,
                        -player_rect.top + sprite.rect.top)
                if hasattr(sprite, 'draw_area'):
                    surface.blit(sprite.image,
                            rect.move(*loc),
                            sprite.draw_area)
                else:
                    surface.blit(sprite.image, rect.move(*loc))
            
        # blit player
        if self.player.sprite.wait%10 < 5: 
            surface.blit(self.player.sprite.image,
                    rect,
                    self.player.sprite.draw_area)
        if self.hud.sprite is not None:
            surface.blit(self.hud.sprite.image,
                    self.hud.sprite.rect)
        if self.player.sprite.placing > 0:
            bbar_rect = self.bbar.get_rect()
            bbar_rect.center = surface.get_rect().center
            bar_rect = self.bar.get_rect()
            bar_rect.center = bbar_rect.center
            surface.blit( self.bbar, bbar_rect )
            surface.blit( self.bar, bar_rect, pygame.Rect(0,0,self.player.sprite.placing,20) )
        if pygame.font.get_init():
            score = self.score()
            if score is None:
                return
            font = pygame.font.Font(pygame.font.get_default_font(),
                    settings.HUD_FONT_SIZE)
            text = font.render(str(self.score()), False, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.bottomright = settings.SCREEN_SIZE
            surface.blit(text, text_rect)
            
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
        wall_like_sprites = itertools.chain(self.walls, (door for door in self.doors if not door.open))
        tmp_list = pygame.sprite.spritecollide( player, wall_like_sprites, False, pygame.sprite.collide_rect )
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
                    
        tmp_list = pygame.sprite.spritecollide( player, self.enemies, False, pygame.sprite.collide_rect )
        for enemy in tmp_list:
            if enemy.allerted and player.wait == 0:
                self.lives -= 1
                player.rect.center = self.respawn
                player.wait = 100
                for enemy in self.enemies:
                    enemy.allerted = False
                    
        player.bomb_place = False
        for bombsite in self.bombsites:
            if bombsite.rect.contains(player.rect):
                if player.just_placed == True:
                    bombsite.kill()
                else:
                    player.bomb_place = True
            
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
            if other.type == 'turkeyshake' and other.exploded:
                continue
            if other.type == 'turkeyshake':
                # TODO: Make this less sucky (two collisions checks)
                collisions = pygame.sprite.spritecollide(
                        other,
                        self.enemies,
                        False)
                if collisions:
                    class TempSprite:
                        rect = other.rect.inflate(settings.TURKEY_SPLASH_SIZE,
                            settings.TURKEY_SPLASH_SIZE)
                    for sprite in pygame.sprite.spritecollide(TempSprite,
                            self.enemies, False):
                        LOG.debug("Reducing speed")
                        if hasattr(sprite, 'max_v'):
                            sprite.max_v *= settings.TURKEY_SPEED_MODIFIER
                    other.explode()
                
            if other.type == 'turkeyshake' and pygame.sprite.spritecollideany( other, self.walls ):
                other.explode()

    def score(self):
        """Get the score in the level's current form"""
        class FlyerCircle:
            def __init__(self, rect):
                self.rect = pygame.Rect((0, 0),
                        [2 * settings.FLYER_RADIUS] * 2)
                self.rect.center = rect.center
                self.radius = settings.FLYER_RADIUS
        for sprite in self.others:
            if sprite.type == 'flyer':
                f = FlyerCircle(sprite.rect)
                collided = pygame.sprite.spritecollide(
                        f,
                        self.enemies,
                        False,
                        pygame.sprite.collide_circle)
                for c in collided:
                    if hasattr(c, 'score_count'):
                        c.score_count = True
        score = len([sprite for sprite in self.enemies
                       if hasattr(sprite, 'score_count') and
                          sprite.score_count])
        score = 1 << (score // 5)
        return score


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
