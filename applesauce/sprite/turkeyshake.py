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
import math
import util
import pkg_resources


class Turkeyshake(pygame.sprite.Sprite):
    
    def __init__(self, big, location, direction, *groups):
        self.type = 'turkeyshake'
        pygame.sprite.Sprite.__init__( self, *groups )
        self.movement = { 'up':0, 'down':0, 'left':0, 'right':0 }
        if big == True:
            self.image = util.load_image( "smoothie_TurkeyBig.png" )
        else:
            self.image = util.load_image( "smoothie_Turkey.png" )
        self.rect = self.image.get_rect()
        self.time = 30
        self.exploded = False
        self.big = big
        if pygame.mixer.get_init():
            self.sound = pygame.mixer.Sound(pkg_resources.resource_stream("applesauce", "sounds/Slurping Smoothie.ogg"))
            self.sound.set_volume(0.8)
            self.sound.play()
        else:
            self.sound = None
        
        if direction.endswith( 'up' ):
            self.movement['up'] = 1
        elif direction.endswith( 'down' ):
            self.movement['down'] = 1
        if direction.startswith( 'left' ):
            self.movement['left'] = 1
        elif direction.startswith( 'right' ):
            self.movement['right'] = 1
            
        if self.movement['up'] ^ self.movement['down'] == 1 and self.movement['left'] ^ self.movement['right'] == 1:
            self.speed = math.sqrt( 50 )
        else:
            self.speed = 10
        self.rect.center = location
        
    def explode(self):
        if self.exploded == False:
            self.time = 200
            self.exploded = True
            if self.big == True:
                self.image = util.load_image( "hit_smoothie_TurkeyBig.png" )
            else:
                self.image = util.load_image( "hit_smoothie_Turkey.png" )
            tmp = self.image.get_rect()
            tmp.center = self.rect.center
            self.rect = tmp
            for value in self.movement.keys():
                self.movement[value] = 0
        
    def update(self):
        if self.time > 0:
            self.time -= 1
        elif self.exploded == False:
            self.explode()
        else:
            self.kill()
        self.rect.move_ip( self.speed*(self.movement['right']-self.movement['left']), self.speed*(self.movement['down']-self.movement['up']) )
    
    def draw(self, screen):
        screen.blit( self.image, self.rect )
