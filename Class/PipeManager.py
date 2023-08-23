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
        self.score = 0

    def update(self, dt, bird, ge):
        self.spawn_timer += dt
        if self.spawn_timer >= SPAWN_DELAY or len(self.pipes) == 0:
            self.spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.height, ASSET))

        for pipe in self.pipes:
            if pipe.x < 0 - ASSET.get_width():
                self.pipes.remove(pipe)

        for pipe in self.pipes:
            pipe.update(dt)

        for pipe in self.pipes:
            if pipe.check_passed(bird.x):
                self.score += 1
                for g in ge:
                    g.fitness += 5
                break

    def draw(self, screen):
        for pipe in self.pipes:
            pipe.draw(screen)

    def collision(self, bird):
        for pipe in self.pipes:
            if pipe.collides(bird.get_rect()):
                bird.alive = False
                return True
        return False

    def getNextPipe(self, bird):
        for pipe in self.pipes:
            if pipe.x + ASSET.get_width() > bird.x:
                return pipe
        raise Exception("No next pipe found")

    def getScore(self):
        return self.score
