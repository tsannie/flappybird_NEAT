import pygame

ASSETS_PATH = [
    pygame.image.load("assets/bird/bluebird-downflap.png"),
    pygame.image.load("assets/bird/bluebird-midflap.png"),
    pygame.image.load("assets/bird/bluebird-upflap.png"),
]
ANIMATION_SPEED = 3
LIFT = -7


class Bird:
    def __init__(self, spawn_x, spawn_y):
        self.x = spawn_x
        self.y = spawn_y
        self.gravity = 0.25
        self.velocity = 0
        self.score = 0
        self.alive = True
        self.image_index = 0
        self.image = ASSETS_PATH

    def update(self, dt):
        # update image_index
        self.image_index += ANIMATION_SPEED * dt
        if self.image_index >= len(self.image):
            self.image_index = 0

    def draw(self, screen):
        print(self.image_index)
        screen.blit(self.image[int(self.image_index)], (self.x, self.y))
