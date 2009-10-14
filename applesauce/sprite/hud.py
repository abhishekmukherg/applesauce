import weakref
import copy

import pygame

from applesauce import settings
from applesauce.sprite import util


class Hud(pygame.sprite.Sprite):
    
    def __init__(self, player, level, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.player = weakref.ref(player)
        self.level = level
        if level == 0:
            self._image = util.load_image("HUD_Lvl_01.png")
        self.rect = self._image.get_rect()

    @property
    def image(self):
        surface = copy.copy(self._image)
        if pygame.font.get_init() and self.player():
            font = pygame.font.Font(pygame.font.get_default_font(),
                    settings.HUD_FONT_SIZE)
            if self.level == 0:
                surface.blit(font.render(str(self.player().turkeyshakes),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((600, 35), (0, 0)))
                surface.blit(font.render(str(self.player().boomboxes),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((475, 35), (0, 0)))
                surface.blit(font.render(str(self.player().flyers),
                                False,
                                (255, 255, 255)),
                        pygame.Rect((750, 35), (0, 0)))
        return surface
        
    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
        self._attract_nearby_enemies()
