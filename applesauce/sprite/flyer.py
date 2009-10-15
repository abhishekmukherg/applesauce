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
import util


class Flyer(pygame.sprite.Sprite):
    
    def __init__(self, location, direction, diff = 0, *groups):
        self.type = 'flyer'
        pygame.sprite.Sprite.__init__( self, *groups )
        if direction == 'up':
            self.image = pygame.Surface( ( 20, 3 ) )
            self.image.fill( ( 255, 255, 255 ) )    
        elif direction == 'down':
            self.image = util.load_image( "flyer.png" )
        elif direction == 'left':
            self.image = pygame.Surface( ( 3, 20 ) )
            self.image.fill( ( 255, 255, 255 ) )    
        elif direction == 'right':
            self.image = pygame.Surface( ( 3, 20 ) )
            self.image.fill( ( 255, 255, 255 ) )    
        self.rect = self.image.get_rect()
        if direction == 'down':
            self.rect.midbottom = location
        else:
            self.rect.center = location
        if direction == 'up':
            self.rect.centery += diff
        
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )