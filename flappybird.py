import pygame
from Class.Bird import Bird
from Class.PipeManager import PipeManager

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def draw_score(screen, score):
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, 50)
    screen.blit(text, text_rect)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
    )
    bird = Bird(WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2)
    pipes = PipeManager(WINDOW_WIDTH, WINDOW_HEIGHT)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill cyan color
        screen.fill((0, 150, 255))

        # check jump
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            bird.jump()

        bird.update(dt)
        if bird.alive:
            pipes.collision(bird)
            pipes.update(dt, bird)

        pipes.draw(screen)
        bird.draw(screen)
        draw_score(screen, bird.score)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()
