import copy
import itertools

import pygame

from applesauce.sprite import util
from applesauce.sprite import player



class Level(object):

    def __init__(self, image):
        self.image = util.load_image(image)
        self.rect = self.image.get_rect()
        self.__image_name = image

        self.player = pygame.sprite.GroupSingle(player.Player(self.rect))

        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.others = pygame.sprite.Group()

        self.__groups = (self.player, self.enemies, self.walls, self.others)

    def sprites(self):
        return tuple(itertools.chain(*self.__groups))

    def copy(self):
        new_level = Level(self.__image_name)
        new_level.player = copy.copy(self.player)
        new_level.enemies = copy.copy(self.enemies)
        new_level.walls = copy.copy(self.walls)
        new_level.others = copy.copy(self.others)
        new_level.__groups = (new_level.player, new_level.enemies,
                new_level.walls, new_level.others)
        return new_level

    def add(self, *sprites):
        self.others.add(*sprites)

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
        for group in self.__groups:
            group.update(*args)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.player.draw(surface)

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
