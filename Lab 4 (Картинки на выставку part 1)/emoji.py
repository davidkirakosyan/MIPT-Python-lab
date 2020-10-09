import pygame


def draw_eyebrow(angle, pos: tuple, image):
    brow = pygame.Surface((180, 25))
    brow.set_colorkey((255, 255, 255))  # making background transparent
    brow.fill(BLACK)
    new = pygame.transform.rotate(brow, angle)
    image.blit(new, pos)


pygame.init()

FPS = 10
w, h = 600, 600
app = pygame.display.set_mode((w, h))
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
YELLOW = (255, 243, 16)
RED = (233, 0, 0)
app.fill(GRAY)

# face
pygame.draw.circle(app, YELLOW, (w // 2, h // 2), w // 3)
pygame.draw.circle(app, BLACK, (w // 2, h // 2), w // 3, 5)
# left eye
pygame.draw.circle(app, RED, (210, 240), w // 16)
pygame.draw.circle(app, BLACK, (210, 240), w // 16, 1)
pygame.draw.circle(app, BLACK, (210, 240), w // 35)
# right eye
pygame.draw.circle(app, RED, (390, 240), w // 22)
pygame.draw.circle(app, BLACK, (390, 240), w // 22, 1)
pygame.draw.circle(app, BLACK, (390, 240), w // 38)
# mouth
pygame.draw.rect(app, BLACK, (210, 390, 180, 30))
# right eyebrow
draw_eyebrow(-35, (110, 110), app)
# left eyebrow
draw_eyebrow(35, (330, 120), app)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
