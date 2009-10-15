# This file is part of applesauce.
#
# applesauce is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# applesauce is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with applesace.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import division

import pygame
import pkg_resources
import weakref
import logging
import math
import random
import util
import effects

from applesauce import settings


LOG = logging.getLogger(__name__)
DIRECTIONS = ('up', 'left', 'right', 'down', 'none')


class PlayerNotFoundException(Exception):
    pass

class WallsNotFoundException(Exception):
    pass


def vec_length(start, end):
    vec = (end[0] - start[0], end[1] - start[1])
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])


class Enemy(effects.SpriteSheet):
    
    def __init__(self, player, walls, image, size, patrol=None, *groups):
        effects.SpriteSheet.__init__(self, util.load_image( image ), size )
        self._allerted = False
        self.allerted = False
        self.patrol = patrol
        self.player = player
        self.walls = walls
        self._random_steps = 0
        self._random_dir = None
        self.time_till_lost = 0
        self.attractor_weakref = None
        self.facing = 'right'
        self.time = 0
        self.anim_frame = 0
        self.state = 0
        self.flipped = False
        self.booltop = True
        self.score_count = False
        if pygame.mixer.get_init():
            self.sound = pygame.mixer.Sound(pkg_resources.resource_stream("applesauce", "sounds/Spotted.ogg"))
            self.sound.set_volume(1)
        else:
            self.sound = None

    @property
    def time_till_lost(self):
        return self._time_till_lost

    @time_till_lost.setter
    def time_till_lost(self, val):
        self._time_till_lost = val
        if self._time_till_lost <= 0 and self.allerted:
            self.allerted = False
        elif self._time_till_lost > 0 and not self.allerted:
            self.allerted = True
            

    @property
    def allerted(self):
        return self._allerted

    @allerted.setter
    def allerted(self, val):
        if val != self._allerted and val and self.sound is not None:
            self.sound.play()
        self._allerted = val
        if val:
            self.time_till_lost = settings.TIME_UNTIL_OFFICER_LOST
        else:
            self.time_till_lost = 0

    @property
    def player(self):
        if self.__player is not None:
            return self.__player()
        else:
            return None

    @player.setter
    def player(self, val):
        if val is not None:
            self.__player = weakref.ref(val)
        else:
            self.__player = None

    @property
    def walls(self):
        return self.__walls()

    @walls.setter
    def walls(self, val):
        self.__walls = weakref.ref(val)
        
    @property
    def booltop(self):
        return self._booltop
        
    @booltop.setter
    def booltop(self, val):
        self._booltop = val
        if val == True:
            self.rect.bottom = self.rect.top
        else:
            self.rect.top = self.rect.bottom

    def can_see_player(self):
        """Returns if the enemy can see the player

        obstructions should be a list of Rect's that would get in the way of
        seeing the player

        Raises PlayerNotFoundException if player is None

        """
        if self.player is None:
            raise PlayerNotFoundException
        if self.walls is None:
            raise WallsNotFoundException
        distance = vec_length(self.player.rect.center, self.rect.center)
        if distance > settings.OFFICER_VIEW_DISTANCE:
            return False
        return not any(
            self._obstructs_los(
                x.rect,
                self.rect.center,
                self.player.rect.center)
            for x in self.walls)

    @staticmethod
    def _obstructs_los(rect, start, end):
        start_sec = Enemy._get_section(rect, start)
        end_sec = Enemy._get_section(rect, end)
        visibles = {0: set((0, 1, 2, 3, 6)),
                    1: set((0, 1, 2)),
                    2: set((0, 1, 2, 5, 8)),
                    3: set((0, 3, 6)),
                    4: set(),
                    5: set((2, 5, 8)),
                    6: set((0, 3, 6, 7, 8)),
                    7: set((6, 7, 8)),
                    8: set((7, 8, 9, 2, 5)),
                    }
        return end_sec not in visibles[start_sec]

    @staticmethod
    def _get_section(rect, point):
        val = 0
        # column
        if point[0] < rect.left:
            val += 0
        elif point[0] < rect.right:
            val += 1
        else:
            val += 2
        # row
        if point[1] < rect.top:
            val += 0
        elif point[1] < rect.bottom:
            val += 3
        else:
            val += 6
        return val

    def _vector_towards_sprite(self, sprite):
        """Returns vector to walk to towards player

        Limits the length of vector to be self.max_v

        """
        my_loc = self.rect.center
        p_loc = sprite.rect.center
        vector = (p_loc[0] - my_loc[0], p_loc[1] - my_loc[1])
        length = vec_length(p_loc, my_loc)
        if length == 0:
            return (0, 0)
        vector = map(lambda x: (x * self.max_v)/length, vector)
        return vector

    def walk_towards_sprite(self, sprite):
        """Walk towards the player at rate self.max_v"""
        vector = self._vector_towards_sprite(sprite)
        self.update_anim(vector)
        tmp_rect = self.rect
        self.rect = self.rect.move(*vector)
        self._return_from_collide(tmp_rect)
    
    def _return_from_collide(self, old_rect):
        collided = pygame.sprite.spritecollide(self, self.walls, False)
        for sprite in collided:
            if (self.rect.top < sprite.rect.bottom and
                    old_rect.top >= sprite.rect.bottom):
                self.rect.top = sprite.rect.bottom
            if (self.rect.left < sprite.rect.right and
                    old_rect.left >= sprite.rect.right):
                self.rect.left = sprite.rect.right
            if (self.rect.bottom > sprite.rect.top and
                    old_rect.bottom <= sprite.rect.top):
                self.rect.bottom = sprite.rect.top
            if (self.rect.right > sprite.rect.left and
                    old_rect.right <= sprite.rect.left):
                self.rect.right = sprite.rect.left

    def walk_randomly(self):
        if self._random_dir is None:
            self._random_dir = random.choice(DIRECTIONS)
            self._random_steps = settings.TIME_IN_RANDOM_DIR + \
                    random.randint(0, settings.TIME_IN_RANDOM_DIR_VARIATION)
        if self._random_steps <= 0:
            if self._random_dir == 'none':
                self._random_dir = None
            else:
                self._random_dir = 'none'
            # One for good measure (this tick)
            self._random_steps = settings.TIME_IN_RANDOM_DIR - 1
            return
        self._random_steps -= 1
        veloc_dict = {'up': (0, 1),
                      'down': (0, -1),
                      'right': (1, 0),
                      'left': (-1, 0),
                      'none': (0, 0)}
        assert all(k in veloc_dict for k in DIRECTIONS)
        assert all(((bool(abs(v[0]) == 1) ^ bool(abs(v[1]) == 1)) or
                    (v[0] == 0 and v[1] == 0))
                for v in veloc_dict.itervalues())
        veloc = veloc_dict[self._random_dir]
        veloc = map(lambda x: x * self.max_v, veloc)
        self.update_anim(veloc)
        tmp_rect = self.rect
        self.rect = self.rect.move(*veloc)
        self._return_from_collide(tmp_rect)

    def update(self):
        self.time_till_lost -= 1
        
    def update_anim(self, vector = (0,0)):
        lr = False
        if vector[0] < 0 and 2*vector[1] > 4*vector[0]:
            self.facing = 'left'
            lr = True
            if self.flipped == False:
                self.image = pygame.transform.flip( self.image, True, False )
                self.flipped = True
        elif vector[0] > 0 and 2*vector[1] <  4*vector[0]:
            self.facing = 'right'
            lr = True
            if self.flipped == True:
                self.image = pygame.transform.flip( self.image, True, False )
                self.flipped = False
        if lr:
            self.state = 2
        if vector[1] < 0 and 2*vector[0] > 4*vector[1]:
            if lr:
                self.facing += 'up'
                self.state = 1
            else:
                self.facing = 'up'
                self.state = 0
        if vector[1] > 0 and 2*vector[0] < 4*vector[1]:
            if lr:
                self.facing += 'down'
                self.state = 3
            else:
                self.facing = 'down'
                self.state = 4
        if vector[0] != 0 or vector[1] != 0:
            if self.flipped == True:
                self.time -= 1
            else:
                self.time += 1
            self.anim_frame = self.time // 2
            if self.anim_frame > 10:
                self.time = 0
                self.anim_frame = 0
            elif self.anim_frame < 0:
                self.time = 2 * 10
                self.anim_frame = 10


class BasicEnemy(Enemy):
    
    def __init__(self, big, location, player, walls, *groups):
        if big == True:
            Enemy.__init__(self, player, walls, "enemyWalkingBigMove_sheet.png", (60,90), *groups)
            self.rect.height -= 45
            self.max_v = settings.ENEMY_MAX_V_2
        else:
            Enemy.__init__(self, player, walls, "enemyWalkingMove_sheet.png", (30,45), *groups)
            self.rect.height -= 22.5
            self.max_v = settings.ENEMY_MAX_V_1
        self.rect.topleft = location

    def update(self):
        self.booltop = False
        super(BasicEnemy, self).update()
        if self.attractor_weakref:
            if self.attractor_weakref():
                self.walk_towards_sprite(self.attractor_weakref())
                self.booltop = True
                return
            else:
                self.attractor_weakref = None
        if self.allerted:
            self.walk_towards_sprite(self.player)
        else:
            self.walk_randomly()
        self.booltop = True


class Officer(Enemy):

    def __init__(self, big, location, player, walls, all_enemies, *groups):
        if big == True:
            Enemy.__init__(self, player, walls, "enemyOfficerBigMove_sheet.png", (70,87), *groups)
            self.rect.height -= 43.5
            self.max_v = settings.OFFICER_MAX_V_2
        else:
            Enemy.__init__(self, player, walls, "enemyOfficerMove_sheet.png", (35,43.5), *groups)
            self.rect.height -= 21.75
            self.max_v = settings.OFFICER_MAX_V_1
        self.rect.topleft = location
        self.time_till_lost = 0
        self.all_enemies = all_enemies

    @property
    def all_enemies(self):
        return self.__all_enemies()

    @all_enemies.setter
    def all_enemies(self, val):
        self.__all_enemies = weakref.ref(val)

    def _alert_nearby_enemies(self):
        if self.all_enemies is None:
            return
        bounding_rect = pygame.Rect((0, 0),
                [settings.OFFICER_ALERT_DISTANCE * 2] * 2)
        bounding_rect.center = self.rect.center
        class BoundingRectSprite:
            rect = bounding_rect
            radius = settings.OFFICER_ALERT_DISTANCE
        x = BoundingRectSprite
        sprites = pygame.sprite.spritecollide(
                x,
                self.all_enemies,
                False,
                pygame.sprite.collide_circle
                )
        for sprite in sprites:
            if sprite is self:
                continue
            if hasattr(sprite, 'allerted'):
                sprite.allerted = True

    def update(self):
        self.booltop = False
        super(Officer, self).update()
        if self.attractor_weakref:
            if self.attractor_weakref():
                self.walk_towards_sprite(self.attractor_weakref())
                self.booltop = True
                return
            else:
                self.attractor_weakref = None
        can_see_player = self.can_see_player()

        # the officer has no idea the player exists
        if not can_see_player and not self.allerted:
            self.walk_randomly()
            self.booltop = True
            return

        if can_see_player:
            self.allerted = True

        self._alert_nearby_enemies()
        self.walk_towards_sprite(self.player)
        self.booltop = True
