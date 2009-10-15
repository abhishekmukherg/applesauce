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
import pkg_resources

import pygame

from applesauce import settings
from applesauce.sprite import util


class Boombox(pygame.sprite.Sprite):
    
    def __init__(self, big, center, enemies, *groups):
        self.type = 'boombox'
        pygame.sprite.Sprite.__init__( self, *groups )
        if big == True:
            self.boombox = util.load_image( "boomboxBig.png" )
            self.rect = pygame.Rect( 0, 0, 75, 56 )
        else:
            self.boombox = util.load_image( "boombox.png" )
            self.rect = pygame.Rect( 0, 0, 38, 28 )
        self.bar = pygame.Surface( ( self.rect.width, 2 ) )
        self.bar.fill( ( 255, 0, 0 ) )
        self.bar_rect = self.bar.get_rect()
        self.time = 300
        if pygame.mixer.get_init():
            self.sound = pygame.mixer.Sound(pkg_resources.resource_stream("applesauce", "sounds/Annoying Boombox Music.ogg"))
            self.sound.set_volume(0.8)
            self.sound.play()
        else:
            self.sound = None
        self.enemies = enemies
        
        self.rect.centerx = center[0]
        self.rect.centery = center[1] - 2
        
    @property
    def image(self):
        image = pygame.Surface( ( self.rect.width, self.rect.height ), pygame.SRCALPHA, 32 ).convert_alpha()
        image.blit( self.boombox, self.boombox.get_rect() )
        image.blit( self.bar, self.bar.get_rect(), pygame.Rect( 0, 0, self.rect.width*(self.time/300.0), 2 ) )
        return image

    def _attract_nearby_enemies(self):
        if self.enemies is None:
            return
        bounding_rect = pygame.Rect((0, 0),
                [settings.BOOMBOX_RADIUS * 2] * 2)
        bounding_rect.center = self.rect.center
        class BoundingRectSprite:
            rect = bounding_rect
            radius = settings.BOOMBOX_RADIUS
        x = BoundingRectSprite
        sprites = pygame.sprite.spritecollide(
                x,
                self.enemies,
                False,
                pygame.sprite.collide_circle
                )
        for sprite in sprites:
            if hasattr(sprite, 'attractor_weakref'):
                sprite.attractor_weakref = weakref.ref(self)
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            if self.sound is not None:
                self.sound.stop()
            self.kill()
        self._attract_nearby_enemies()
