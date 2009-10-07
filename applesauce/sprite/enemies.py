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
        pass


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
