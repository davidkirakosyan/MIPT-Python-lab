import pygame
from pygame.draw import *
import random
from math import sin, cos, pi
import csv
from time import asctime

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
FONT_COLOR = (255, 255, 255)
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
    v_max = 15
    radius = 60
    balls.extend(coord_calc(
        ball_number,
        s_size[0],
        s_size[1],
        radius,
        v_max
    ))
    rect_number = 2
    rects.extend(coord_calc(
        rect_number,
        s_size[0],
        s_size[1],
        2 * radius // 3,
        v_max
    ))

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    # timer init conditions
    is_showing = True
    start_time = pygame.time.get_ticks()
    show_screen_t = 2  # 2 seconds
    hide_screen_t = 3
    lap = show_screen_t

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                score += count_score(event, balls + rects, v_max, s_size)

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
        move_elements(balls + rects, *s_size)
        if is_showing:
            show_balls(screen, balls)
            show_rects(screen, rects)

        pygame.display.update()
    ask_name(screen, clock, FPS, score)
    pygame.quit()


def coord_calc(n, max_x, max_y, size, v_max):
    """
    Calculates coordinates for n items and puts in `lst`
    :param n: item amount
    :param max_x: window's max width
    :param max_y: window's max height
    :param size: size of the item
    :param v_max: full velocity
    :return: list with items
    """
    elems = []
    for i in range(n):
        angle = 2 * pi * random.random()
        elems.append({
            'x': random.randint(100, max_x - 100),
            'y': random.randint(100, max_y - 100),
            'r': size,
            'vx': int(v_max * cos(angle)),
            'vy': int(v_max * sin(angle)),
            'color': random.choice(list(COLORS.values())[:-1]),  # removing BLACK color
        })
    return elems


def move_elements(elems, w, h):
    """
    Change elements' coordinates and check whether they should bounce the wall.

    :param elems: list of dictionaries with elements' parameters
    :param w: width of window
    :param h: height of window
    :return: None
    """
    for item in elems:
        if item['x'] < item['r'] or w - item['x'] < item['r']:
            item['vx'] *= -1
        if item['y'] < item['r'] or h - item['y'] < item['r']:
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
    :param rects: list of dictionaries with rectangles' data.
    :return: None
    """
    for item in rects:
        x = item['x'] - item['r'] // 2
        y = item['y'] - item['r'] // 2
        rect(surface, item['color'], (x, y, item['r'], item['r']))


def count_score(event, elems, v_max, s_size):
    """
    Checks whether click is on area of any element.
    If yes, returns 1 and changes element's parameters.

    :param event: pygame Event object
    :param elems: list of dictionaries with elements' data.
    :param v_max: full velocity module
    :param s_size: screen's (width, height)
    :return: score if click was on element, 0 otherwise
    """
    x, y = event.pos
    for item in elems:
        touching, res = is_touching(item, x, y)
        if touching:
            new = coord_calc(1, s_size[0], s_size[1], item['r'], v_max)[0]  # get new coords
            for k in new.keys():
                if k == 'r':
                    continue
                item[k] = new[k]
            break
    return res


def is_touching(item, click_x, click_y):
    """
    Determines if click was on the item in `balls` or `rects`.
    If yes returns tuple with (True, score).

    :param item: item in `balls` or `rects`
    :param click_x: click x-coordinate
    :param click_y: click y-coordinate
    :return: (True, score) or (False, 0)
    """
    touching = False
    res = 0
    if item in rects:
        dist_x = abs(item['x'] - click_x)
        dist_y = abs(item['y'] - click_y)
        if dist_x <= item['r'] and dist_y <= item['r']:
            touching = True
            res = 3
    else:
        distance = ((item['x'] - click_x) ** 2 + (item['y'] - click_y) ** 2) ** 0.5
        if distance <= item['r']:
            touching = True
            res = 1

    return touching, res


def show_score(surface, score):
    """
    Draws player's score in top left corner of `screen`.

    :param surface: pygame Surface object
    :param score: player's score
    :return: None
    """
    font = pygame.font.SysFont('arial', 25, True)
    text = font.render("Score: {}".format(score), True, FONT_COLOR)
    surface.blit(text, text.get_rect())


def timer(curr_time, str_time, lap, show_t, hide_t, is_showing):
    """
    Checks if current time is bigger than timer start time + lap time.
    If true elements showing condition changes.
    Lap time also changes in order to provide different show/hide interval.

    :param curr_time: current time in milliseconds
    :param str_time: timer start time in milliseconds
    :param lap: lap time in seconds
    :param show_t: screen showing time in seconds
    :param hide_t: screen hiding time in seconds
    :param is_showing: Bool, if True elements can be seen.
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


def ask_name(surface, clock, fps, score):
    """
    At the end of the game renders text with score,
    asks player of his name and writes achievement in a csv file.

    :param surface: pygame Surface object
    :param clock: pygame Clock
    :param fps: fps for clock
    :param score: player's score
    :return: None
    """
    if score == 0:
        return

    entered_name = False
    name = ''
    render_end_screen(surface, score, name)
    while not entered_name:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                name += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-2]  # including backspace char
                if event.unicode == '\r':
                    entered_name = True
                    break
                render_end_screen(surface, score, name)
    if name[-1] == '\r':
        name = name[:-1]
        with open('achievements.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([name, score, asctime()])


def render_end_screen(surface, score, name):
    """
    Renders text with score, asks player of his name.
    Prints player's name during typing.

    :param surface: pygame Surface object
    :param score: player's score
    :param name: player's entered name
    :return: None
    """
    w, h = surface.get_size()
    surface.fill(COLORS['BLACK'])
    font = pygame.font.SysFont('arial', 30, True)

    text1 = "Your score is: {}!!!".format(score)
    text1_obj = font.render(text1, True, FONT_COLOR)
    rect1 = text1_obj.get_rect(center=(w // 2, h // 3))
    text2 = "Please enter your name: "
    text2_obj = font.render(text2, True, FONT_COLOR)
    rect2 = text2_obj.get_rect(center=(w // 3, h // 2))
    text3 = "or press X button to quit."
    text3_obj = font.render(text3, True, FONT_COLOR)
    rect3 = text3_obj.get_rect(center=(w // 2, 2 * h // 3))

    render_table(surface, w, h)

    surface.blit(text1_obj, rect1)
    surface.blit(text2_obj, rect2)
    surface.blit(text3_obj, rect3)

    name_obj = font.render(name, True, FONT_COLOR)
    name_rect = name_obj.get_rect(center=(2 * w // 3, h // 2))
    surface.blit(name_obj, name_rect)

    pygame.display.update()


def render_table(surface, w, h):
    """
    Draws table with first 5 best results from csv file

    :param surface: pygame Surface object
    :param w: width of `surface`
    :param h: height of `surface`
    :return: None
    """
    font = pygame.font.SysFont('arial', 22, True)

    results = []
    try:
        with open('achievements.csv') as file:
            reader = csv.reader(file)
            for row in list(reader):
                results.append({'name': row[0], 'score': row[1]})
            results.sort(key=lambda item: int(item['score']), reverse=True)
            results = results[:5]
    except FileNotFoundError:
        return
    x = 7 * w // 10
    y = 0

    title_obj = font.render('Best Results', True, FONT_COLOR)
    title_rect = title_obj.get_rect(center=(x + 3 * w // 20, h // 40))
    surface.blit(title_obj, title_rect)
    rect(surface, FONT_COLOR, (x, y, 3 * w // 10, h // 20), 1)

    y += h // 20
    for player in results:
        name_obj = font.render(player['name'], True, FONT_COLOR)
        name_rect = name_obj.get_rect(
            center=(x + 3 * w // 40, y + h // 40)
        )
        score_obj = font.render(player['score'], True, FONT_COLOR)
        score_rect = score_obj.get_rect(
            center=(x + 9 * w // 40, y + h // 40)
        )
        surface.blit(name_obj, name_rect)
        surface.blit(score_obj, score_rect)

        rect(surface, FONT_COLOR,
             (x, y, 3 * w // 20, h // 20), 1)
        rect(surface, FONT_COLOR,
             (x + 3 * w // 20, y, 3 * w // 20, h // 20), 1)

        y += h // 20


if __name__ == '__main__':
    main()
