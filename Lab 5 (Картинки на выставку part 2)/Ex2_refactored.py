import pygame
import pygame.draw as draw
import math
import random as rand

COLORS = {
    'yellow': 0xFFFF00,
    'black': 0x0,
    'white': 0xffffff,
    'red': 0xff0000,
    'sky blue': 0xafdde9,
    'grass green': 0xaade87,
    'mountain grey': 0xb3b3b3,
    'flower key color': 0xf0f0aa,
    'eye purple': 0xe580ff,
    'bush green': 0x71c837
}


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
    animal_rect = (
        int(0.12 * screen_size[0]),
        int(0.42 * screen_size[1]),
        int(0.37 * screen_size[0]),
        int(0.4 * screen_size[1]),
    )
    draw_animal(screen, *animal_rect)
    bush_rect = (
        int(0.75 * screen_size[0]),
        int(0.74 * screen_size[1]),
        screen_size[0] // 5
    )
    draw_bush(screen, *bush_rect)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = True
    while finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = False
    pygame.quit()


def rand_pos(r, offset):
    ox, oy = offset
    angle = 2 * math.pi * rand.random()
    return int(r * math.sin(angle) + ox), int(r * math.cos(angle) + oy)


def draw_mountains(screen, size):
    """
    Draws mountain chain on screen.

    :param screen: pygame Surface object
    :param size: (width, height), tuple with screen's width and height
    :return: None
    """
    closing_coeff = [
        (1, 1),
        (0, 1),
    ]
    mountains_coeff = [
        (0, 0.325),
        (0.18, 0.25),
        (0.26, 0.275),
        (0.5, 1 / 8),
        (0.54, 0.225),
        (0.64, 0.275),
        (0.8, 3 / 16),
        (0.86, 0.225),
        (1, 0.175),
    ]
    mountains_vertices = [(int(x * size[0]), int(y * size[1])) for x, y in mountains_coeff]
    closing_vertices = [(int(x * size[0]), int(y * size[1])) for x, y in closing_coeff]
    draw.polygon(screen, COLORS['mountain grey'], mountains_vertices + closing_vertices)
    draw.aalines(screen, COLORS['black'], False, mountains_vertices)


def draw_land(screen, size):
    """
    Draws land on screen.

    :param screen: pygame Surface object
    :param size: (width, height), tuple with screen's width and height
    :return:
    """
    closing_coeff = [
        (1, 1),
        (0, 1),
    ]
    surface_coeff = [
        (0, 31 / 80),
        (0.04, 307 / 800),
        (0.06, 309 / 800),
        (0.09, 63 / 160),
        (0.46, 0.4),
        (0.47, 33 / 80),
        (0.48, 69 / 160),
        (0.488, 0.475),
        (0.496, 39 / 80),
        (0.504, 0.525),
        (0.52, 0.5275),
        (0.56, 419 / 800),
        (1, 0.525),
    ]
    surface_vertices = [(int(x * size[0]), int(y * size[1])) for x, y in surface_coeff]
    closing_vertices = [(int(x * size[0]), int(y * size[1])) for x, y in closing_coeff]
    draw.polygon(screen, COLORS['grass green'], surface_vertices + closing_vertices)
    draw.aalines(screen, COLORS['black'], False, surface_vertices)


def draw_animal(screen, x, y, width, height, reverse=False):
    """
    Draws animal on screen at x, y coordinates.

    :param screen: pygame Surface object
    :param x: x-coordinate of top left point
    :param y: y-coordinate of top left point
    :param width: full width of animal
    :param height: full height of animal
    :param reverse: if False, animal looks right
    :return: None
    """
    surf = pygame.Surface((width, height))
    surf.set_colorkey(COLORS['flower key color'])
    surf.fill(COLORS['flower key color'])

    head_rect = (
        int(0.7 * width),
        height // 22,
        int(0.3 * width),
        int(0.44 * height)
    )
    draw_head(surf, *head_rect)
    legs_xy = (
        (width//10, height//2),
        (int(0.25 * width), int(0.58 * height)),
        (width//2, height//2),
        (int(0.65 * width), int(0.58 * height)),
    )
    for x_, y_, in legs_xy:
        leg_width = width // 6
        leg_height = int(0.38 * height)
        draw_leg(surf, x_, y_, leg_width, leg_height)
    body_rect = (
        0,
        int(0.41 * height),
        6 * width // 7,
        int(0.22 * height),
    )
    draw.ellipse(surf, COLORS['white'], body_rect)

    if reverse:
        surf = pygame.transform.flip(surf, True, False)

    screen.blit(surf, (x, y))


def draw_head(screen, x, y, width, height):
    """
    Draws animal's head and neck on `screen`.

    :param screen: pygame Surface object
    :param x: x-coordinate of top left point of image head
    :param y: y-coordinate of top left point of image head
    :param width: width of head
    :param height: neck and head total height
    :return: None
    """
    def draw_eye(surface, x, y, width, height):
        """
        Draws an eye of animal with pupil on surface.

        :param surface: pygame Surface Object
        :param x: x-coord of center of eye
        :param y: y-coord of center of eye
        :param width: width of eye
        :param height: height of eye
        :return: None
        """
        draw.ellipse(surface, COLORS['eye purple'], (x, y, width, height))
        pupil_rect = (
            x + int(0.4 * width),
            y + height//6,
            int(0.5 * width),
            int(0.5 * height),
        )
        draw.ellipse(surface, COLORS['black'], pupil_rect)
        glare_xy = (
            (x + int(0.1 * width), y + int(0.2 * height)),
            (x + int(0.3 * width), y + int(0.1 * height)),
            (x + int(0.6 * width), y + int(0.4 * height)),
            (x + int(0.4 * width), y + int(0.3 * height)),
        )
        draw.polygon(surface, COLORS['white'], glare_xy)

    def draw_horn(surface, x, y, width, height):
        """
        Draws a horn on the head of animal.

        :param surface: pygame Surface object
        :param x: x-coordinate of bottom right point of the horn
        :param y: y-coordinate of bottom right point of the horn
        :param width: width of horn
        :param height: height of horn
        :return: None
        """
        poly_xy = (
            (x, y),
            (x - width//3, y + height // 5),
            (x - width, y - 4 * height // 5),
        )
        draw.polygon(screen, COLORS['white'], poly_xy)

    draw.ellipse(screen, COLORS['white'], (x, y, width, height//4))
    draw.ellipse(screen, COLORS['white'],
                 (
                     x - width//10,
                     y + height//6,
                     int(0.7 * width),
                     int(0.92 * height),
                 ))
    eye_xy = (
        x + int(0.25 * width),
        y + height // 30,
        int(0.38 * width),
        int(0.16 * height),
    )
    draw_eye(screen, *eye_xy)
    horn_xy = (
        (x + width//10, y + height//15, width // 3, int(0.2 * height)),
        (x + width//4, y + height//40, width // 3, int(0.2 * height)),
    )
    for param in horn_xy:
        draw_horn(screen, *param)


def draw_leg(screen, x, y, width, height):
    """
    Draws a leg consisting of 2 vertical and 1 horizontal ellipses on pygame Surface.

    :param screen: pygame Surface object
    :param x: x-coordinate of top left point
    :param y: y-coordinate of top left point
    :param width: width of foot
    :param height: full width of 3 pieces
    :return: None
    """
    height0 = int(0.4 * height)
    width0 = int(0.7 * width)
    draw.ellipse(screen, COLORS['white'], (x, y, width0, height0))
    draw.ellipse(screen, COLORS['white'], (x, y + int(0.95*height0), width0, height0))
    draw.ellipse(screen, COLORS['white'],
                 (
                    x + 2,
                    y + int(1.9 * height0),
                    int(0.9 * width),
                    int(0.15 * height),
                 ))


def draw_bush(screen, x, y, radius):
    """
    Draws a bush on `screen` and calculates parameters of flowers.

    :param screen: pygame Surface object
    :param x: x-coordinate of bush's center.
    :param y: y-coordinate of bush's center.
    :param radius: radius of the bush
    :return: None
    """
    number_of_flowers = rand.randint(3, 6)

    draw.circle(screen, COLORS['bush green'], (x, y), radius)
    flower_width = int(0.55 * radius)
    flower_height = int(0.27 * radius)
    for i in range(number_of_flowers):
        flower_x = x + rand.randint(-radius, radius) * 3 // 8
        flower_y = y + rand.randint(-radius, radius) * 3 // 8
        draw_flower(screen, flower_x, flower_y, flower_width, flower_height)


def draw_flower(screen, x, y, w, h):
    """
    Draws a flower on `screen` object.

    :param screen: pygame Surface object
    :param x: flower's center x-coordinate
    :param y: flower's center y-coordinate
    :param w: width of the flower
    :param h: height of the flower
    :param angle: angle, the flower is rotated at
    :return: None
    """
    surface = pygame.Surface((w, h))
    surface.fill(COLORS['flower key color'])
    surface.set_colorkey(COLORS['flower key color'])

    petal_width = 4 * w // 10
    petal_height = 4 * h // 10
    petal_xy = (
        (x, y - h // 4),
        (x + 3 * w // 20, y - 3 * h // 20),
        (x - 3 * w // 20, y - 3 * h // 20),
        (x - w // 4, y),
        (x + w // 4, y),
        (x, y),
        (x + 3 * w // 20, y + h // 5),
        (x - 3 * w // 20, y + h // 5),
    )
    for i, j in petal_xy:
        if i == x and j == y:
            draw.ellipse(screen, COLORS['yellow'], (i, j, petal_width, petal_height))
            continue
        draw.ellipse(screen, COLORS['white'], (i, j, petal_width, petal_height))
        draw.ellipse(screen, COLORS['black'], (i, j, petal_width, petal_height), 1)



if __name__ == '__main__':
    main()
