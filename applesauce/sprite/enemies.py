import pygame
import weakref


class PlayerNotFoundException(Exception):
    pass


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, player, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.player = player

    @property
    def player(self):
        return self.__player()

    @player.setter
    def player(self, val):
        self.__player = weakref.ref(val)

    def can_see_player(self, obstructions):
        """Returns if the enemy can see the player

        obstructions should be a list of Rect's that would get in the way of
        seeing the player

        Raises PlayerNotFoundException if player is None

        """
        if self.player is None:
            raise PlayerNotFoundException
        for rect in obstructions:
            pass

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


class BasicEnemy(Enemy):
    
    def __init__(self, player, *groups):
        Enemy.__init__(self, player, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((160, 160, 160))
        self.rect = self.image.get_rect()


class Officer(Enemy):

    def __init__(self, player, *groups):
        Enemy.__init__(self, player, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()

import doctest
doctest.testmod()
