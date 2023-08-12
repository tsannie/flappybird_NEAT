import pygame
from Class.Bird import Bird

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bird = Bird(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill cyan color
        screen.fill((0, 180, 255))

        bird.update(dt)

        bird.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()
