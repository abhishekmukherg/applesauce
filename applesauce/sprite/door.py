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
import weakref
import logging

import pygame

from applesauce import settings
from applesauce.sprite import util
from applesauce.sprite import effects


LOG = logging.getLogger(__name__)


class Door(effects.SpriteSheet):
    
    def __init__(self, loc, horizontal, *groups):
        self.type = 'door'
        if horizontal:
            image = util.load_image("Lvl_02_DoorH_Close_sheet.png")
            size = (93, 31)
        else:
            image = util.load_image("Lvl_02_DoorV_Close_sheet.png")
            size = (31, 93)
        effects.SpriteSheet.__init__(self, image, size)
        self.frame = 0
        self.sound = None
        self._moving = False
        self.frame_mod = 1
        
        self.rect.center = loc

    @property
    def open(self):
        return self.anim_frame == 0

    @property
    def moving(self):
        return self._moving

    @moving.setter
    def moving(self, val):
        if val != self._moving and val:
            self.anim_frame += self.frame_mod
        self._moving = val
        
    def update(self):
        if not self.moving:
            return
        self.frame += 1

        if self.frame < settings.DOOR_FRAME_TIME:
            return

        self.frame = 0
        if self.anim_frame >= settings.DOOR_FRAME_COUNT - 1:
            self.frame_mod = -1
            self.moving = False
        elif self.anim_frame <= 0:
            self.frame_mod = 1
            self.moving = False
        else:
            self.anim_frame += self.frame_mod

        assert self.anim_frame < settings.DOOR_FRAME_COUNT and \
                self.anim_frame >= 0
