import pygame
import random
import sys

SIZE_BETWEEN_PIPES = 100
MINIMUM_HEIGHT = 50
SPEED = 140


class Pipe:
    def __init__(self, spawn_x, screen_height, asset):
        self.x = spawn_x
        self.speed = SPEED
        self.up = random.randint(
            MINIMUM_HEIGHT, screen_height - SIZE_BETWEEN_PIPES - MINIMUM_HEIGHT
        )
        self.down = self.up + SIZE_BETWEEN_PIPES
        self.asset = asset
        self.screen_height = screen_height
        self.passed = False

    def draw(self, screen):
        screen.blit(
            pygame.transform.rotate(self.asset, 180),
            (self.x, self.up - self.asset.get_height()),
        )
        screen.blit(self.asset, (self.x, self.down))

    def update(self, dt):
        self.x -= self.speed * dt

    def check_passed(self, bird_x):
        if not self.passed and self.x + self.asset.get_width() < bird_x:
            self.passed = True
            return True

        return False

    def collides(self, bird_rect):
        if bird_rect.colliderect(self.get_rect_up()):
            return True
        if bird_rect.colliderect(self.get_rect_down()):
            return True

        return False

    def get_rect_up(self):
        return pygame.Rect(
            self.x,
            self.up - 100000,
            self.asset.get_width(),
            100000,
        )

    def get_rect_down(self):
        return pygame.Rect(
            self.x,
            self.down,
            self.asset.get_width(),
            100000,
        )
