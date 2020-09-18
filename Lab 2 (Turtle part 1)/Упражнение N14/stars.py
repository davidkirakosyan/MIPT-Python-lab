import math
import turtle


def main():
    init()

    turtle.setx(-160)
    star(150, 5)
    turtle.setx(160)
    star(150, 11)

    turtle.hideturtle()
    # hold window
    turtle.mainloop()


def init():
    turtle.shape('turtle')
    turtle.up()


def star(radius, n):
    angle = 360 / n
    side = 2 * radius * math.sin(math.radians(angle * (n - 1)/4))
    # moving top
    turtle.left(90)
    turtle.forward(radius)
    turtle.left(180 - angle/4)

    turtle.pendown()
    for i in range(n):
        turtle.forward(side)
        turtle.left(180 - angle/2)
    turtle.up()

    # moving center
    turtle.right(180 - angle / 4)
    turtle.backward(radius)
    turtle.right(90)


if __name__ == "__main__":
    main()
