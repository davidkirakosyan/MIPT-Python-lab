import pygame
from Ex2 import COLORS
from Ex2 import draw_mountains, draw_land
from Ex2 import draw_animal
from Ex2 import draw_bush


def main():
    """
    Initializes pygame, draws background, animal and bush.

    :return: None
    """
    pygame.init()
    FPS = 60

    screen_size = (794, 1123)
    screen = pygame.display.set_mode(screen_size)
    screen.fill(COLORS['sky blue'])

    draw_mountains(screen, screen_size)
    draw_land(screen, screen_size)

    bush_rect = (
        (0.55, 0.8, 0.15),
        (0.9, 0.62, 0.12),
    )
    for x, y, scale in bush_rect:
        x_ = int(screen_size[0] * x)
        y_ = int(screen_size[1] * y)
        radius = int(screen_size[0] * scale)
        draw_bush(screen, x_, y_, radius)

    animal_rect = (
        (0.1, 0.6, 0.3, False),
        (0.15, 0.3, 0.2, False),
        (0.7, 0.6, 0.25, True),
    )
    for x, y, scale, rev in animal_rect:
        x_ = int(screen_size[0] * x)
        y_ = int(screen_size[1] * y)
        w = int(screen_size[0] * scale)
        h = int(screen_size[1] * scale)
        draw_animal(screen, x_, y_, w, h, rev)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = True
    while finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = False
    pygame.quit()


if __name__ == '__main__':
    main()
