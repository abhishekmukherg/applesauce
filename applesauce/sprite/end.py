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


class End(pygame.sprite.Sprite):
    
    def __init__(self, x, y, x2, y2, *groups):
        self.type = "end"
        pygame.sprite.Sprite.__init__( self, *groups )
        self.image = pygame.Surface( ( x2 - x, y2 - y ) )
        self.image.fill( ( 0, 180, 0 ) )
        self.rect = pygame.Rect( x, y, x2 - x, y2 - y )
        
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )