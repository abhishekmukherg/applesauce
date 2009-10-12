from __future__ import division

import pygame
import weakref
import math

from applesauce import settings


class PlayerNotFoundException(Exception):
    pass

class WallsNotFoundException(Exception):
    pass


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, player, walls, patrol=None, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.allerted = False
        self.patrol = patrol
        self.player = player
        self.walls = walls
        self.max_v = settings.ENEMY_MAX_V

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
        length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
        if length == 0:
            return (0, 0)
        vector = map(lambda x: (x * self.max_v)/length, vector)
        return vector

    def walk_towards_player(self):
        """Walk towards the player at rate self.max_v"""
        vector = self._vector_towards_player()
        self.rect.move_ip(*vector)


class BasicEnemy(Enemy):
    
    def __init__(self, player, walls, *groups):
        Enemy.__init__(self, player, walls, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((160, 160, 160))
        self.rect = self.image.get_rect()


class Officer(Enemy):

    def __init__(self, player, walls, *groups):
        Enemy.__init__(self, player, walls, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()

    def update(self):
        if self.can_see_player():
            self.allerted = True
            self.walk_towards_player()
