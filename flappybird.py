import pygame
import neat
import os

from Class.Bird import Bird
from Class.PipeManager import PipeManager

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PATH_NEAT_CONFIG = "neat_config"
generation = 0
best_score = 0


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

    global generation
    generation += 1

    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    font = pygame.font.SysFont("Arial", 20)

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
                ge[i].fitness -= 10
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

        # update population
        population = len(birds)

        # draw generation
        text_pop = font.render(f"Population: {population}", True, (255, 255, 255))
        text_gen = font.render(f"Generation: {generation}", True, (255, 255, 255))

        # print on top left
        screen.blit(text_pop, (10, 10))
        screen.blit(text_gen, (10, 40))

        # best score
        global best_score
        best_score = max(best_score, pipes.getScore())
        text_best = font.render(f"Best score: {best_score}", True, (255, 255, 255))

        # print on top right
        screen.blit(text_best, (WINDOW_WIDTH - text_best.get_width() - 10, 10))

        # jump
        next_pipe = pipes.getNextPipe(birds[0])
        for i, bird in enumerate(birds):
            ge[i].fitness += 0.1

            # bonus zone
            if bird.y < next_pipe.up + 5 and bird.y > next_pipe.down - 5:
                ge[i].fitness += 0.2

            output = nets[i].activate(
                (bird.y, abs(bird.y - next_pipe.up), abs(bird.y - next_pipe.down))
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

    winner = population.run(run)


if __name__ == "__main__":
    init_neat(PATH_NEAT_CONFIG)

    # run()
