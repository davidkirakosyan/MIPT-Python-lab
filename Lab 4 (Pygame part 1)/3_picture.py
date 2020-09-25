import pygame as pyg
from pygame.draw import *


def man(plot, x, y, width, height):
    ellipse(plot, COLOR['PURPLE'], (x, y, width, height))
    circle(plot, COLOR['FACE_COLOR'], (x + width // 2, y - height // 6), height//5)
    # hands
    line(plot, COLOR['BLACK'],
         (x + width//5, y + height//10),
         (x - width//2, y + int(0.65*height)), 2)
    line(plot, COLOR['BLACK'],
         (x + int(.8*width), y + height//10),
         (x + int(1.6*width), y + height//2), 2)
    # legs
    line(plot, COLOR['BLACK'],
         (x + width//3, y + int(0.95*height)),
         (x + width//20, y + int(1.5*height)), 2)
    line(plot, COLOR['BLACK'],
         (x + width//20, y + int(1.5*height)),
         (x - width//4, y + int(1.5*height) + 2), 2)
    line(plot, COLOR['BLACK'],
         (x + 2*width//3, y + int(0.95*height)),
         (x + 3*width//4, y + int(1.49*height)), 2)
    line(plot, COLOR['BLACK'],
         (x + 3*width//4, y + int(1.49*height)),
         (x + width, y + int(1.5*height)), 2)


def woman(plot, x, y, width, height):
    # woman
    polygon(plot, COLOR['PINK'],
            [(x, y), (x-width//2, y+height), (x+width//2, y+height)])
    circle(plot, COLOR['FACE_COLOR'], (x, y-height//16), 2*height//11)
    # hands
    line(plot, COLOR['BLACK'],
            (x - width//12, y + height//6),
            (x - int(0.8*width), y + int(0.55*height)), 2)
    line(plot, COLOR['BLACK'],
            (x + width//12, y + height//6),
            (x + int(0.4*width), y + int(0.4*height)), 2)
    line(plot, COLOR['BLACK'],
            (x + int(0.4*width), y + int(0.4*height)),
            (x + int(0.6*width), y + height//4), 2)
    # legs
    line(plot, COLOR['BLACK'],
            (x - width//10, y + height),
            (x - width//10, y + int(1.45*height)), 2)
    line(plot, COLOR['BLACK'],
            (x - width//10, y + int(1.45*height)),
            (x - int(0.3*width), y + int(1.45*height)), 2)
    line(plot, COLOR['BLACK'],
            (x + width//10, y + height),
            (x + width//10, y + int(1.45*height)), 2)
    line(plot, COLOR['BLACK'],
            (x + width//10, y + int(1.45*height)),
            (x + int(0.3*width), y + int(1.45*height) + 3), 2)


pyg.init()
FPS = 60
COLOR = {
    'GREEN': (55, 200, 113),
    'BLUE': (170, 238, 255),
    'FACE_COLOR': (244, 227, 215),
    'PINK': (255, 85, 221),
    'PURPLE': (167, 147, 172),
    'RED': (255, 0, 0),
    'WHITE': (255, 255, 255),
    'BROWN': (85, 0, 0),
    'YELLOW': (255, 204, 0),
    'BLACK': (0, 0, 0),
}
w, h = 1032, 768

screen = pyg.display.set_mode((w, h))
screen.fill(COLOR['GREEN'])
# sky
rect(screen, COLOR['BLUE'], (0, 0, w, h // 2))

man(screen, 260, 250, 150, 300)

# ice cream
polygon(screen, COLOR['YELLOW'],
        [(200, 450), (105, 395), (200, 340)])
circle(screen, COLOR['BROWN'], (120, 365), 29)
circle(screen, COLOR['RED'], (170, 340), 29)
circle(screen, COLOR['WHITE'], (130, 330), 29)

woman(screen, 690, 220, 240, 330)

# balloon
line(screen, COLOR['BLACK'], (830, 315), (885, 170), 2)
polygon(screen, COLOR['RED'],
        [(885, 170), (970, 100), (870, 60)])
circle(screen, COLOR['RED'], (895, 70), 28)
circle(screen, COLOR['RED'], (945, 90), 28)

# display and quit event handling
pyg.display.update()
clock = pyg.time.Clock()
finished = False

while not finished:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            finished = True
pyg.quit()
