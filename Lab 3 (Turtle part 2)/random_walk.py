import turtle
import random

turtle.shape('turtle')
turtle.speed(0)
turtle.color('red')
turtle.width(2)
for i in range(100):
    turtle.forward(30)
    turtle.left(360 * random.random())

# hold window
turtle.mainloop()
