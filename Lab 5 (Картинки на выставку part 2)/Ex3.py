from Ex2 import colors, main, draw_background, draw_animal, draw_bush
import random as rand

def draw_advanced_scene(screen, colors):
    draw_background(screen, colors)

    draw_bush(screen, colors, 40, 340, 0.3)
    draw_bush(screen, colors, 180, 410, 0.25)
    draw_bush(screen, colors, 300, 450, 0.4)
    draw_bush(screen, colors, 220, 430, 0.15)

    draw_animal(screen, colors, 0, 300, 0.7)
    draw_animal(screen, colors, 0, 120, 0.4)
    draw_animal(screen, colors, 200, 400, 0.5, True)


if __name__ == '__main__':
    main(draw_advanced_scene, colors)