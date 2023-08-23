import pygame

ASSETS = [
    pygame.image.load("assets/bird/bluebird-downflap.png"),
    pygame.image.load("assets/bird/bluebird-midflap.png"),
    pygame.image.load("assets/bird/bluebird-upflap.png"),
]
ANIMATION_SPEED = 3
LIFT = -6
GRAVITY = 0.35


class Bird:
    def __init__(self, spawn_x, spawn_y):
        self.x = spawn_x
        self.y = spawn_y
        self.gravity = GRAVITY
        self.velocity = 0
        self.alive = True
        self.image_index = 0
        self.image = ASSETS

    def update(self, dt):
        # update image_index
        self.image_index += ANIMATION_SPEED * dt
        if self.image_index >= len(self.image):
            self.image_index = 0

        # update velocity
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        if self.alive:
            self.velocity = LIFT

    def draw(self, screen):
        screen.blit(self.image[int(self.image_index)], (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(
            self.x, self.y, self.image[0].get_width(), self.image[0].get_height()
        )
