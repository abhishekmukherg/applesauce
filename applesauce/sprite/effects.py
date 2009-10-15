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
import pygame
import logging

LOG = logging.getLogger(__name__)

class SpriteSheet(pygame.sprite.Sprite):

    def __init__(self, image, image_size, *groups):
        """Makes a simple sprite sheet holder
        
        image: A Surface class
        image_size: (WxH) of an individual sprite
        
        """
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.rect = image.get_rect()
        self.rect.size = image_size
        self.draw_area = pygame.Rect((0, 0), image_size)
        self.anim_frame = 0
        self.state = 0
        assert self.draw_area

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, val):
        self.__state = val
        self.draw_area.top = val * self.draw_area.height

    @property
    def anim_frame(self):
        """Animation frame of the sprite sheet"""
        return self.__anim_frame

    @anim_frame.setter
    def anim_frame(self, val):
        self.__anim_frame = val
        self.draw_area.left = val * self.draw_area.width

