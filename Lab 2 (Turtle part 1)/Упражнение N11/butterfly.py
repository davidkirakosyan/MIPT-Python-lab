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


turtle.shape('turtle')
# making circles horizontal
turtle.left(90)
for i in range(70, 140, 10):
    two_circles(i)

# hold window
turtle.mainloop()
