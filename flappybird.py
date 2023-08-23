import pygame
import neat
import os

from Class.Bird import Bird
from Class.PipeManager import PipeManager

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PATH_NEAT_CONFIG = "neat_config"


def draw_score(screen, score):
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(str(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, 50)
    screen.blit(text, text_rect)


def run(genomes, config):
    ge = []
    nets = []
    birds = []
    pipes = PipeManager(WINDOW_WIDTH, WINDOW_HEIGHT)

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2))
        genome.fitness = 0
        ge.append(genome)

    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
    )
    clock = pygame.time.Clock()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # fill cyan color
        screen.fill((0, 150, 255))

        # check collision
        for i, bird in enumerate(birds):
            if pipes.collision(bird):
                ge[i].fitness -= 1
                nets.pop(i)
                ge.pop(i)
                birds.pop(i)

        if len(birds) == 0:
            break

        # update
        pipes.update(dt, birds[0], ge)
        for bird in birds:
            bird.update(dt)

        # draw
        pipes.draw(screen)
        for bird in birds:
            bird.draw(screen)

        draw_score(screen, pipes.getScore())

        # jump
        next_pipe = pipes.getNextPipe(birds[0])
        for i, bird in enumerate(birds):
            ge[i].fitness += 0.1

            # punition if bird is too high or too low
            if bird.y < 0 or bird.y > WINDOW_HEIGHT:
                ge[i].fitness -= 0.5

            output = nets[i].activate(
                (
                    bird.y,
                    abs(bird.y - next_pipe.up),
                    abs(bird.y - next_pipe.down),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()


def init_neat(config_path):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, PATH_NEAT_CONFIG)
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(run, 50)


if __name__ == "__main__":
    init_neat(PATH_NEAT_CONFIG)

    # run()
