import pygame
from pygame.draw import *
import random
from math import sin, cos, pi

COLORS = {
    'WHITE': 0xFFFFFF,
    'RED': 0xFF0000,
    'BLUE': 0x0000FF,
    'YELLOW': 0xFFFF00,
    'GREEN': 0x00FF00,
    'MAGENTA': 0xFF00FF,
    'CYAN': 0x00FFFF,
    'BLACK': 0x0,
}
balls = []
rects = []

def main():
    """
    Initializes pygame Surface, defines event handling loop.
    """
    pygame.init()

    FPS = 50
    s_size = (1200, 900)
    screen = pygame.display.set_mode(s_size)
    screen.fill(COLORS['BLACK'])

    score = 0

    ball_number = 3
    v_max = 20
    radius = 60
    for i in range(ball_number):
        angle = 2 * pi * random.random()
        balls.append({
            'x': random.randint(100, s_size[0] - 100),
            'y': random.randint(100, s_size[1] - 100),
            'r': radius,
            'vx': int(v_max * cos(angle)),
            'vy': int(v_max * sin(angle)),
            'color': random.choice(list(COLORS.values())[:-1]),  # removing BLACK color
        })
    rect_number = 2
    for i in range(rect_number):
        angle = 2 * pi * random.random()
        rects.append({
            'x': random.randint(100, s_size[0] - 100),
            'y': random.randint(100, s_size[1] - 100),
            'r': radius * 2 // 3,
            'vx': int(v_max * cos(angle)),
            'vy': int(v_max * sin(angle)),
            'color': random.choice(list(COLORS.values())[:-1]),  # removing BLACK color
        })

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    # timer init conditions
    is_showing = True
    start_time = pygame.time.get_ticks()
    show_screen_t = 2  # 2 seconds
    hide_screen_t = 5
    lap = show_screen_t

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                score += count_score(event, balls, v_max, s_size)

        start_time, lap, is_showing = timer(
            pygame.time.get_ticks(),
            start_time,
            lap,
            show_screen_t,
            hide_screen_t,
            is_showing,
        )

        screen.fill(COLORS['BLACK'])
        show_score(screen, score)
        move_elements(balls + rects, *s_size, radius)
        if is_showing:
            show_balls(screen, balls)
            show_rects(screen, rects)

        pygame.display.update()
    pygame.quit()


def move_elements(elems, w, h, bounce_lim):
    """
    Change elements' coordinates and check whether they should bounce the wall.

    :param elems: list of dictionaries with elements' parameters
    :param w: width of window
    :param h: height of window
    :return: None
    """
    for item in elems:
        if item['x'] < bounce_lim or w - item['x'] < bounce_lim:
            item['vx'] *= -1
        if item['y'] < bounce_lim or h - item['y'] < bounce_lim:
            item['vy'] *= -1
        item['x'] += item['vx']
        item['y'] += item['vy']


def show_balls(surface, balls):
    """
    Draws balls on `surface` object.

    :param surface: pygame Surface object
    :param balls: list of dictionaries with balls' data.
    :return: None
    """
    for item in balls:
        circle(surface, item['color'], (item['x'], item['y']), item['r'])


def show_rects(surface, rects):
    """
    Draws balls on `surface` object.

    :param surface: pygame Surface object
    :param rects: list of dictionaries with balls' data.
    :return: None
    """
    for item in rects:
        x = item['x'] - item['r'] // 2
        y = item['y'] - item['r'] // 2
        rect(surface, item['color'], (x, y, item['r'], item['r']))


def count_score(event, balls, v_max, screen_size):
    """
    Checks whether click is on area of any ball.
    If yes, returns 1 and changes ball's parameters.

    :param event: pygame Event object
    :param balls: list of dictionaries with balls' data.
    :return: 1 if click is on ball, 0 otherwise.
    """
    x, y = event.pos
    res = 0
    for item in balls:
        distance = ((item['x'] - x) ** 2 +(item['y'] - y) ** 2) ** 0.5
        if distance <= item['r']:
            res = 1
            angle = 2 * pi * random.random()
            item['x'] = random.randint(100, screen_size[0] - 100)
            item['y'] = random.randint(100, screen_size[1] - 100)
            item['vx'] = int(v_max * cos(angle))
            item['vy'] = int(v_max * sin(angle))
            item['color'] = random.choice(list(COLORS.values())[:-1])  # removing BLACK color
    return res


def show_score(surface, score):
    """
    Draws player's score in top left corner of `screen`.

    :param surface: pygame Surface object
    :param score: player's score
    :return: None
    """
    font = pygame.font.SysFont('arial', 25, True)
    text = font.render("Score: {}".format(score), True, (255, 255, 255))
    surface.blit(text, text.get_rect())


def timer(curr_time, str_time, lap, show_t, hide_t, is_showing):
    """
    Checks if current time is bigger than timer start time + lap time.
    If true balls showing condition changes.
    Lap time also changes in order to provide different show/hide interval.

    :param curr_time: current time in milliseconds
    :param str_time: timer start time in milliseconds
    :param lap: lap time in seconds
    :param show_t: screen showing time in seconds
    :param hide_t: screen hiding time in seconds
    :param is_showing: Bool, if True balls can be seen.
    :return: new (start time, lap time, is_showing)
    """
    if (curr_time - str_time) / 1000 >= lap:
        is_showing = not is_showing
        str_time = curr_time
        if lap == show_t:
            lap = hide_t
        else:
            lap = show_t
    return str_time, lap, is_showing


if __name__ == '__main__':
    main()
