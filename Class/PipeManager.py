import pygame

from Class.Pipe import Pipe

ASSET = pygame.image.load("assets/pipe.png")
SPAWN_DELAY = 2


class PipeManager:
    def __init__(self, width, height):
        self.pipes = []
        self.width = width
        self.height = height
        self.spawn_timer = 0

    def update(self, dt, bird):
        self.spawn_timer += dt
        if self.spawn_timer >= SPAWN_DELAY:
            self.spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.height, ASSET))

        for pipe in self.pipes:
            if pipe.x < 0 - ASSET.get_width():
                self.pipes.remove(pipe)

        for pipe in self.pipes:
            pipe.update(dt)

        for pipe in self.pipes:
            if pipe.check_passed(bird.x):
                bird.score += 1
                break

    def draw(self, screen):
        for pipe in self.pipes:
            pipe.draw(screen)

    def collision(self, bird):
        for pipe in self.pipes:
            if pipe.collides(bird.get_rect()):
                bird.alive = False
