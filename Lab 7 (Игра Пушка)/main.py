from abc import ABC, abstractmethod
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
        target_args = (
            self.screen,
            random.randint(7 * self.width // 10, 9 * self.width // 10),
            random.randint(self.height // 10, 8 * self.height // 10),
            random.choice(self.target_colors),
        )  # without size
        self.targets = [
            Ball(*target_args, random.randint(self.height // 30, self.height // 20)),
            Emoji(*target_args, random.randint(self.height // 20, self.height // 10))
        ]

    def mainloop(self):
        finished = False
        mouse_down = False
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
            if mouse_down:
                self.cannon.increase_muzzle()

            self.show_scores()

            if self.cannon.missiles:
                self.handle_missiles()

            for target in self.targets:
                target.draw()
                target.move(self.width, self.height)
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
            for target in self.targets:
                if target.is_touching(missile):
                    self.cannon.missiles.remove(missile)
                    self.tries = 0

                    self.targets.remove(target)

                    args = (
                        self.screen,
                        random.randint(7 * self.width // 10, 9 * self.width // 10),
                        random.randint(self.height // 10, 8 * self.height // 10),
                        random.choice(self.target_colors),
                    )
                    if type(target) == Ball:
                        self.targets.append(Ball(
                            *args,
                            random.randint(self.height // 30, self.height // 20),
                        ))
                    elif type(target) == Emoji:
                        self.targets.append(Emoji(
                            *args,
                            random.randint(self.height // 20, self.height // 10),
                        ))
                    self.score += target.award
                    break  # don't check for removed missile


class Cannon:
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


class Target(ABC):
    def __init__(self, screen, x, y, color, size):
        self.screen = screen
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.color = color

    def is_touching(self, other: Missile):
        """
        Checks for collision with `other`

        :return: True if is touching `other`
        """
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist <= self.size + other.r

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self, scr_width, scr_height):
        pass


class Ball(Target):
    def __init__(self, screen, x, y, color, size):
        super().__init__(screen, x, y, color, size)
        self.award = 1

    def draw(self):
        """
        Draws ball targets with radius = size

        :return: None
        """
        circle(self.screen, self.color, (self.x, self.y), self.size)
        circle(self.screen, BLACK, (self.x, self.y), self.size, 1)

    def move(self, scr_width, scr_height):
        """
        This target doesn't move.
        """
        pass


class Emoji(Target):
    def __init__(self, screen, x, y, color, size):
        super().__init__(screen, x, y, color, size)
        self.award = 3
        self.v_x = random.randint(-10, 10)
        self.v_y = random.randint(-3, 3)

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
        Moves Emoji.

        :param scr_width: screen's width.
        :param scr_height: screen's height.
        :return: None
        """
        x_max = 9 * scr_width / 10
        x_min = x_max - 5 * self.size
        y_max = 8 * scr_height // 10
        y_min = y_max - 5 * self.size
        if self.x - x_min <= 0:
            self.v_x = abs(self.v_x)
        elif x_max - self.x <= 0:
            self.v_x = -abs(self.v_x)
        if self.y - y_min <= 0:
            self.v_y = abs(self.v_y)
        elif y_max - self.y <= 0:
            self.v_y = -abs(self.v_y)

        self.x = int(self.x + self.v_x)
        self.y = int(self.y + self.v_y)


if __name__ == "__main__":
    game = Game(1200, 600)
    game.mainloop()
