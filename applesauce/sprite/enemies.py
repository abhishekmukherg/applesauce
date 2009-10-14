from __future__ import division

import pygame
import weakref
import logging
import math
import random

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


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, player, walls, patrol=None, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.allerted = False
        self.patrol = patrol
        self.player = player
        self.walls = walls
        self.max_v = settings.ENEMY_MAX_V
        self._random_steps = 0
        self._random_dir = None

    @property
    def player(self):
        return self.__player()

    @player.setter
    def player(self, val):
        self.__player = weakref.ref(val)

    @property
    def walls(self):
        return self.__walls()

    @walls.setter
    def walls(self, val):
        self.__walls = weakref.ref(val)

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

    def _vector_towards_player(self):
        """Returns vector to walk to towards player

        Limits the length of vector to be self.max_v

        """
        if self.player is None:
            raise PlayerNotFoundException
        my_loc = self.rect.center
        p_loc = self.player.rect.center
        vector = (p_loc[0] - my_loc[0], p_loc[1] - my_loc[1])
        length = vec_length(p_loc, my_loc)
        if length == 0:
            return (0, 0)
        vector = map(lambda x: (x * self.max_v)/length, vector)
        return vector

    def walk_towards_player(self):
        """Walk towards the player at rate self.max_v"""
        vector = self._vector_towards_player()
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
            LOG.debug("New random dir: %s" % self._random_dir)
            self._random_steps = settings.TIME_IN_RANDOM_DIR
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
        tmp_rect = self.rect
        self.rect = self.rect.move(*veloc)
        self._return_from_collide(tmp_rect)


class BasicEnemy(Enemy):
    
    def __init__(self, player, walls, all_enemies, *groups):
        Enemy.__init__(self, player, walls, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((160, 160, 160))
        self.rect = self.image.get_rect()
        self.all_enemies = all_enemies

    @property
    def all_enemies(self):
        return self.__all_enemies()

    @all_enemies.setter
    def all_enemies(self, val):
        self.__all_enemies = weakref.ref(val)

    def update(self):
        if self.allerted:
            pass



class Officer(Enemy):

    def __init__(self, player, walls, *groups):
        Enemy.__init__(self, player, walls, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.time_till_lost = 0

    @property
    def time_till_lost(self):
        return self._time_till_lost

    @time_till_lost.setter
    def time_till_lost(self, val):
        self._time_till_lost = val
        if self._time_till_lost <= 0:
            self.allerted = False
        else:
            self.allerted = True

    def update(self):
        can_see_player = self.can_see_player()
        # Reduce time_till lost if can't see player
        if not can_see_player and self.allerted:
            self.time_till_lost -= 1

        # the officer has no idea the player exists
        if not can_see_player and not self.allerted:
            self.walk_randomly()
            return

        if can_see_player:
            self.time_till_lost = settings.TIME_UNTIL_OFFICER_LOST

        self.walk_towards_player()
