import collections

import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        # TODO: defind self.image, self.rect
        self.movement = {'up':False, 'down':False, 'left':False, 'right':False}
        self.speed = 5
        
    def set_movement(self, direction):
        """Sets the movement direction

        Removes movement on all directions except "direction". If direction is
        a list, then set to those directions. If direction is None, no movement
        is done

        """
        if direction is None: # no movement
            self.__cancel_movement()
        elif isinstance(direction, collections.Iterable):
            self.__set_movement(direction)
        else:
            self.__set_movement([direction])

    def __cancel_movement(self):
        for k in self.movement:
            self.movement[k] = False

    def __set_movement(self, directions):
        self.__cancel_movement()
        for direction in directions:
            assert direction in self.movement
            self.movement[dir] = True
