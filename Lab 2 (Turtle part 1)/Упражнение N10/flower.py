'''Drawing a flower with circles.'''
import turtle


def two_circles(radius):
    '''Drawing two opposite circles.'''
    step = radius * 3 / 57.3
    for i in range(int(360 / 3)):
        turtle.forward(step)
        turtle.left(3)
    for i in range(int(360 / 3)):
        turtle.forward(step)
        turtle.right(3)


for i in range(3):
    two_circles(50)
    turtle.left(60)

# hold window
turtle.mainloop()
