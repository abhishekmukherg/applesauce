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

import pygame

from applesauce import settings
from applesauce.sprite import util


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, center, *groups):
        self.type = 'bomb'
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = util.load_image( "bomb.png" )
        self.rect = self.image.get_rect()
        
        self.rect.center = center
        
    def update(self):
        pass
