import pygame
from pygame.draw import *
import random
import math


class Game:
    FPS = 30
    score = 0
    COLORS = {
        'RED': 0xFF0000,
        'BLUE': 0x0000FF,
        'YELLOW': 0xFFFF00,
        'GREEN': 0x00FF00,
        'MAGENTA': 0xFF00FF,
        'CYAN': 0x00FFFF,
        'BLACK': 0x0,
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg = 0xFFFFFF

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bg)
        self.clock = pygame.time.Clock()
        self.cannon = Cannon(
            self.screen,
            0.1 * self.width,
            0.85 * self.height,
            0.05 * self.height,
            random.choice(list(self.COLORS.values())),
        )
        self.missile = None
        self.target = Ball(
            random.randint(7 * self.width // 10, self.width),
            random.randint(self.height // 10, 8 * self.height // 10),
            random.randint(1, self.height // 20),
            random.choice(list(self.COLORS.values())),
        )

    def mainloop(self):
        finished = False
        mouse_down = False
        while not finished:
            self.clock.tick(self.FPS)

            self.screen.fill(self.bg)
            line(self.screen, self.COLORS['BLACK'], (0, 9 * self.height // 10),
                 (self.width, 9 * self.height // 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                if event.type == pygame.MOUSEMOTION:
                    self.cannon.rotate_muzzle(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
                    self.cannon.shoot(self)
            if mouse_down:
                self.cannon.increase_muzzle()

            if self.missile:
                y_max = 0.9 * self.height
                x_max = self.width
                self.missile.move(x_max, y_max)
                self.missile.draw(self)
                if self.missile.is_dead(y_max):
                    self.missile = None

            self.target.draw(self)

            self.cannon.draw(self)
            pygame.display.update()
        pygame.quit()


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

    def draw(self, other: Game):
        """
        Draws cannon with its muzzle.
        :return: None
        """
        circle(self.screen, self.color, (self.x, self.y), self.r)
        circle(self.screen, other.COLORS['BLACK'], (self.x, self.y), self.r, 2)

        plot = pygame.Surface((self.width, self.height))
        plot.fill(self.color)
        plot.set_colorkey(other.bg)
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

    def shoot(self, other: Game):
        self.width = 2 * self.r
        if not other.missile:
            other.missile = Missile(
                self.screen,
                self.x + self.width * math.cos(self.angle),
                self.y - self.width * math.sin(self.angle),
                other.COLORS['BLACK'],
                self.r // 2,
                self.angle,
                35 * (self.width / self.r - 1)
            )


class Missile:
    g = 2
    k = 0.01

    def __init__(self, screen, x, y, color, radius, angle, vel):
        self.screen = screen
        self.x = int(x)
        self.y = int(y)
        self.angle = int(angle)
        self.v_x = int(vel * math.cos(self.angle))
        self.v_y = - int(vel * math.sin(self.angle))
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
        dt = 0.5
        if self.x <= self.r or x_max - self.x <= 1.5 * self.r:
            self.v_x *= -1
        if self.y <= self.r or y_max - self.y <= 1.5 * self.r:
            self.v_y *= -1
        self.v_x += - int(self.k * self.v_x) * dt
        self.v_y += self.g - int(self.k * self.v_y) * dt
        self.x += int(self.v_x * dt)
        self.y += int(self.v_y * dt)

        self.time += dt

    def draw(self, other: Game):
        """
        Draws missile.
        :param other: Game object
        :return: None
        """
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def is_dead(self, y_max: int):
        is_on_bottom = y_max - self.y <= 0.5 * self.r
        return self.time > 120 or is_on_bottom

class Target:
    def __init__(self, x, y, size, color):
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.color = color


class Ball(Target):
    def draw(self, other: Game):
        """
        Draws ball targets with radius = size
        :return: None
        """
        circle(other.screen, self.color, (self.x, self.y), self.size)
        circle(other.screen, other.COLORS['BLACK'], (self.x, self.y), self.size, 1)

    def is_touching(self, other: Missile):
        """
        Checks for collision with `other`
        :return: True if is touching `other`.
        """
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist <= self.size + other.r


if __name__ == "__main__":
    game = Game(1200, 600)
    game.mainloop()
