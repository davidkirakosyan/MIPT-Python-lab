import random
import math

import pygame
from pygame.draw import *

from colors import *


class Game:
    """
    Controls game
    """
    FPS = 30
    score = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg = WHITE

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bg)
        self.font = pygame.font.SysFont('arial', 30, True)
        self.clock = pygame.time.Clock()
        self.tries = 0

        self.cannon = Cannon(
            self.screen,
            0.1 * self.width,
            0.85 * self.height,
            0.05 * self.height,
            random.choice(GAME_COLORS),
        )
        self.target_colors = GAME_COLORS
        self.target_colors.remove(self.cannon.color)
        self.targets = []
        for i in range(2):
            self.targets.append(
                Ball(
                    self.screen,
                    random.randint(5 * self.width // 10, 9 * self.width // 10),
                    random.randint(self.height // 10, 8 * self.height // 10),
                    random.choice(self.target_colors),
                    random.randint(self.height // 30, self.height // 20),
                )
            )
        self.emoji_n = 1
        self.emojis = [
            Emoji(
                self.screen,
                random.randint(5 * self.width // 10, 9 * self.width // 10),
                random.randint(self.height // 10, 8 * self.height // 10),
                random.choice(self.target_colors),
                random.randint(self.height // 15, self.height // 10),
                0
            )
        ]

    def mainloop(self):
        finished = False
        mouse_down = False
        key_down_event = None
        while not finished:
            self.clock.tick(self.FPS)

            self.screen.fill(self.bg)
            line(self.screen, BLACK, (0, 9 * self.height // 10),
                 (self.width, 9 * self.height // 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                if event.type == pygame.MOUSEMOTION:
                    self.cannon.rotate_muzzle(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.cannon.shoot()
                    self.tries += 1
                    mouse_down = False
                if event.type == pygame.KEYDOWN:
                    key_down_event = event
                elif event.type == pygame.KEYUP:
                    key_down_event = None
            if mouse_down:
                self.cannon.increase_muzzle()
            if key_down_event is not None:
                self.move_cannon(key_down_event)

            self.show_scores()

            if self.cannon.missiles:
                self.handle_missiles()

            for target in self.targets:
                target.draw()
            for i, emoji in enumerate(self.emojis):
                if emoji.health <= 0:
                    self.emojis.remove(emoji)
                    continue
                emoji.draw()
                self.emoji_move_control(emoji, i)
                emoji.move(self.width, self.height)
            self.add_emoji()
            self.cannon.draw(self.bg)

            pygame.display.update()
        pygame.quit()

    def show_scores(self):
        text = self.font.render("Score: {}".format(self.score), True, BLACK)
        x_ = self.width // 20
        y_ = self.height // 20
        self.screen.blit(text, (x_, y_))

        text = self.font.render("Tries: {}".format(self.tries), True, BLACK)
        x_ = self.width // 20
        y_ = self.height // 10
        self.screen.blit(text, (x_, y_))

    def handle_missiles(self):
        y_max = 0.9 * self.height
        x_max = self.width
        for missile in self.cannon.missiles:
            missile.move(x_max, y_max)
            missile.draw()
            if missile.is_dead(y_max):
                self.cannon.missiles.remove(missile)
            if not self.check_target_touching(missile):
                self.check_emoji_touching(missile)

    def check_target_touching(self, missile):
        """
        Checks if missile is touching one of the targets.

        :type missile: Missile
        :return: True, if is touching, False otherwise
        """
        for target in self.targets:
            if target.is_touching(missile):
                self.cannon.missiles.remove(missile)
                self.tries = 0
                self.targets.remove(target)
                args = (
                    self.screen,
                    random.randint(5 * self.width // 10, 9 * self.width // 10),
                    random.randint(self.height // 10, 8 * self.height // 10),
                    random.choice(self.target_colors),
                )
                self.targets.append(Ball(
                    *args,
                    random.randint(self.height // 30, self.height // 20),
                ))
                self.score += target.award
                return True
        return False

    def check_emoji_touching(self, missile):
        for emoji in self.emojis:
            if emoji.is_touching(missile):
                self.cannon.missiles.remove(missile)
                break

    def emoji_move_control(self, emoji, index):
        """
        Orients emoji to catch missile.

        :type emoji: Emoji
        :param index: index of emoji in self.emojis
        :return: None
        """
        if index + 1 > len(self.targets):
            index = random.randint(0, len(self.targets) - 1)
        if self.cannon.missiles:
            tr = self.cannon.missiles[0].trajectory
            emoji.dest_x, emoji.dest_y = min_dist(tr, self.targets[emoji.t_index])
        else:
            emoji.dest_x = 0
            emoji.dest_y = 0

    def add_emoji(self):
        if self.score % 5 == 0 or len(self.emojis) == 0:
            self.emoji_n = self.score // 5 + 1
            if len(self.emojis) < self.emoji_n:
                if len(self.emojis) >= len(self.targets):
                    target_index = random.randint(0, len(self.targets) - 1)
                else:
                    target_index = len(self.emojis)
                self.emojis.append(
                    Emoji(
                        self.screen,
                        random.randint(5 * self.width // 10, 9 * self.width // 10),
                        random.randint(self.height // 10, 8 * self.height // 10),
                        random.choice(self.target_colors),
                        random.randint(self.height // 15, self.height // 10),
                        target_index,
                    )
                )

    def move_cannon(self, event):
        """
        Determines if arrow keys arrow keys are pressed.
        and moves cannon.

        :param event: pygame KEYDOWN event
        :return: None
        """
        if event.key == pygame.K_LEFT:
            self.cannon.move(left=True)
        elif event.key == pygame.K_RIGHT:
            self.cannon.move(left=False)


class Cannon:
    velocity = 5

    def __init__(self, screen, x, y, radius, color):
        """
        :param screen: pygame Surface object
        :param x: x-coord. of cannon
        :param y: y-coord. of cannon
        :param radius: radius of cannon
        """
        self.x = int(x)
        self.y = int(y)
        self.r = int(radius)
        self.screen = screen
        self.color = color
        self.angle = 0  # muzzle direction
        self.width = 2 * self.r
        self.height = self.width // 4
        self.delta_muz = self.r // 25
        self.missiles = []

    def draw(self, bg_color):
        """
        Draws cannon with its muzzle.

        :return: None
        """
        circle(self.screen, self.color, (self.x, self.y), self.r)
        circle(self.screen, BLACK, (self.x, self.y), self.r, 2)

        plot = pygame.Surface((self.width, self.height))
        plot.fill(self.color)
        plot.set_colorkey(bg_color)
        plot = pygame.transform.rotate(plot, math.degrees(self.angle))

        y_ = self.y - plot.get_height() + self.height // 2
        self.screen.blit(plot, (self.x, y_))

        tr = trajectory(
            self.angle,
            self.x + self.width * math.cos(self.angle),
            self.y - self.width * math.sin(self.angle),
            20 * (self.width / self.r - 1),
            10,
            0.1
        )[:6]
        aalines(self.screen, GREY, False, tr)

    def rotate_muzzle(self, event: pygame.event.EventType):
        """
        Aligns muzzle with mouse position.
        """
        e_x, e_y = event.pos
        if e_x <= self.x:
            e_x = self.x + 2
        if e_y >= self.y:
            e_y = self.y
        self.angle = math.atan((self.y - e_y) / (e_x - self.x))

    def increase_muzzle(self):
        if self.width > 3 * self.r:
            self.delta_muz *= -1
        if self.width < 2 * self.r:
            self.delta_muz *= -1
        self.width += self.delta_muz

    def shoot(self):
        self.missiles.append(Missile(
            self.screen,
            self.x + self.width * math.cos(self.angle),
            self.y - self.width * math.sin(self.angle),
            self.color,
            self.r // 2,
            self.angle,
            20 * (self.width / self.r - 1)
        ))
        self.width = 2 * self.r

    def move(self, left: bool):
        """
        Moves cannon.

        :param left: True if left arrow, False if right
        :return: None
        """
        screen_width = self.screen.get_size()[0]
        if left:
            if self.x > 0.1 * screen_width:
                self.x -= int(self.velocity)
        else:
            if self.x < 0.4 * screen_width:
                self.x += int(self.velocity)


class Missile:
    g = 10
    k = 0.1

    def __init__(self, screen, x, y, color, radius, angle, vel):
        self.screen = screen
        self.x = int(x)
        self.y = int(y)
        self.angle = angle
        self.v_x = vel * math.cos(self.angle)
        self.v_y = - vel * math.sin(self.angle)
        self.r = int(radius)
        self.color = color
        self.trajectory = trajectory(angle, x, y, vel, self.g, self.k)
        self.time = 0

    def move(self, x_max, y_max):
        """
        Moves missile.

        :param x_max: screen's width
        :param y_max: screen's height
        :return:
        """
        dt = 0.07
        if x_max - self.x <= self.r:
            self.v_x = -0.9 * abs(self.v_x)
        if y_max - self.y <= self.r:
            self.v_y = -0.5 * abs(self.v_y)
            self.v_x *= 0.8  # ground friction
        self.v_x += - self.k * self.v_x * dt
        self.v_y += self.g * dt - self.k * self.v_y * dt

        self.x = int(self.x + self.v_x)
        self.y = int(self.y + self.v_y)

        self.time += dt

    def draw(self):
        """
        Draws missile.

        :return: None
        """
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def is_dead(self, y_max: int):
        is_on_bottom = y_max - self.y <= 2 * self.r and abs(self.v_x) <= 2
        is_over_top = self.y <= 0
        return self.time > 100 or is_on_bottom or is_over_top


class Ball:
    def __init__(self, screen, x, y, color, size):
        self.award = 1
        self.screen = screen
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.color = color

    def draw(self):
        """
        Draws ball targets with radius = size

        :return: None
        """
        circle(self.screen, self.color, (self.x, self.y), self.size)
        circle(self.screen, BLACK, (self.x, self.y), self.size, 1)

    def is_touching(self, other: Missile):
        """
        Checks for collision with `other`

        :return: True if is touching `other`
        """
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist <= self.size + other.r


class Emoji:
    def __init__(self, screen, x, y, color, size, target_index):
        self.screen = screen
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.color = color
        self.health = 10
        self.v_x = 5
        self.v_y = 5
        # destination coordinates
        self.dest_x = 0
        self.dest_y = 0
        # which target would be protected
        self.t_index = target_index

    def draw(self):
        """
        Draws ball targets with radius = size

        :return: None
        """
        circle(self.screen, RED, (self.x, self.y), self.size)

        left_eye = (self.x - self.size // 3, self.y - self.size // 3)
        circle(self.screen, BLACK, left_eye, self.size // 4)
        circle(self.screen, RED, left_eye, self.size // 10)

        right_eye = (self.x + self.size // 3, self.y - self.size // 3)
        circle(self.screen, BLACK, right_eye, self.size // 4)
        circle(self.screen, RED, right_eye, self.size // 10)

        mouth_rect = (self.x - self.size // 3, self.y + self.size // 4, 2 * self.size // 3, 2 * self.size // 3)
        arc(self.screen, BLACK, mouth_rect, 0, math.pi, 3)

        circle(self.screen, BLACK, (self.x, self.y), self.size, 2)

    def move(self, scr_width, scr_height):
        """
        Moves Emoji depending on cannon's direction.

        :param scr_width: screen's width
        :param scr_height: screen's height
        :return: None
        """
        x_max = 9 * scr_width // 10
        x_min = 5 * scr_width // 10
        y_max = 8 * scr_height // 10
        y_min = scr_height // 10

        if self.dest_x == 0 and self.dest_y == 0:
            if abs(self.v_x) < 5 and abs(self.v_y) < 5:
                self.v_x = random.randint(-5, 5)
                self.v_y = random.randint(-5, 5)
            if self.x - x_min <= 0:
                self.v_x = abs(self.v_x)
            elif x_max - self.x <= 0:
                self.v_x = -abs(self.v_x)
            if self.y - y_min <= 0:
                self.v_y = abs(self.v_y)
            elif y_max - self.y <= 0:
                self.v_y = -abs(self.v_y)
        else:
            self.v_x = - 0.04 * (self.x - self.dest_x)
            self.v_y = - 0.04 * (self.y - self.dest_y)
            if abs(self.v_x) < 0.05:
                self.v_x = 0
            if abs(self.v_y) < 0.05:
                self.v_y = 0

        self.x = int(self.x + self.v_x)
        self.y = int(self.y + self.v_y)

    def is_touching(self, other: Missile):
        """
        Checks for collision with `other`

        :return: True if is touching `other`
        """
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        if dist <= self.size + other.r:
            self.health -= 1
            return True
        return False


def min_dist(traject, target):
    """
    Calculates the nearest to the target point, which the missile can reach.

    :param traject: missile's trajectory
    :param target: Ball object
    :return: the nearest point's (x, y)
    """
    dist = []
    for x, y in traject:
        dist.append(((x - target.x) ** 2 + (y - target.y) ** 2) ** 0.5)
    return traject[dist.index(min(dist))]


def trajectory(angle, x_0, y_0, vel, g, k):
    """
    Calculates trajectory of a missile
    
    :param angle: initial angle from horizon 
    :param x_0: initial x-coordinate
    :param y_0: initial y-coordinate
    :param vel: initial velocity
    :param g: gravity acceleration
    :param k: air resistance coefficient
    :return: [(x,y)], points of the trajectory
    """
    dt = 0.07
    x, y = int(x_0), int(y_0)
    dx = vel * math.cos(angle)
    dy = - vel * math.sin(angle)

    traject = []
    for i in range(100):
        traject.append((x, y))
        dx += - k * dx * dt
        dy += g * dt - k * dy * dt
        x = int(x + dx)
        y = int(y + dy)
        if y < 0:
            break

    return traject


if __name__ == "__main__":
    game = Game(1200, 600)
    game.mainloop()
