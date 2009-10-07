import pygame


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)


class BasicEnemy(Enemy):
    
    def __init__(self, *groups):
        Enemy.__init__(self, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((160, 160, 160))
        self.rect = self.image.get_rect()


class Officer(Enemy):

    def __init__(self, *groups):
        Enemy.__init__(self, *groups)
        self.image = pygame.Surface((25, 25))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
