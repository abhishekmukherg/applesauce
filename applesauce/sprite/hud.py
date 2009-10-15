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
import copy

import pygame

from applesauce import settings
from applesauce.sprite import util


class Hud(pygame.sprite.Sprite):
    
    def __init__(self, player, level, lives_fn, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.player = weakref.ref(player)
        self.level = level
        self.lives_fn = lives_fn
        if level == 0:
            self._image = util.load_image("HUD_Lvl_01.png")
            self.right_col_fn = lambda: self.player().flyers
        elif level == 1:
            self._image = util.load_image("HUD_Lvl_02.png")
            self.right_col_fn = lambda: self.player().bombs
        else:
            assert False
        self.rect = self._image.get_rect()

    @property
    def image(self):
        surface = copy.copy(self._image)
        if pygame.font.get_init() and self.player():
            font = pygame.font.Font(pygame.font.get_default_font(),
                    settings.HUD_FONT_SIZE)
            if self.level == 0 or self.level == 1:
                surface.blit(font.render(str(self.player().turkeyshakes),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((620, 35), (0, 0)))
                surface.blit(font.render(str(self.player().boomboxes),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((485, 35), (0, 0)))
                surface.blit(font.render(str(self.right_col_fn()),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((745, 35), (0, 0)))
                surface.blit(font.render(str(self.lives_fn()),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((75, 35), (0, 0)))
        return surface
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
        self._attract_nearby_enemies()
