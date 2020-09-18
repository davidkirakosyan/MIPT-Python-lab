import math
import turtle


def poly(radius, side_number):
    angle = 360 / side_number
    side = 2 * radius * math.sin(math.radians(angle / 2))

    turtle.left(90 + angle / 2)
    turtle.pendown()
    for i in range(side_number):
        turtle.forward(side)
        turtle.left(angle)
    turtle.penup()
    turtle.right(90 + angle / 2)


turtle.shape('turtle')
turtle.penup()

radius = 30
for i in range(10):
    turtle.goto(radius, 0)
    poly(radius, i + 3)
    radius += 20

# hold window
turtle.mainloop()
