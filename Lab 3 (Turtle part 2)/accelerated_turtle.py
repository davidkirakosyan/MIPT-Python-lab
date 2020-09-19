import turtle
import math

turtle.speed(0)
turtle.shape('turtle')
# horizon line
turtle.goto(400, 0)
turtle.goto(-400, 0)
# initial conditions
v_x = 15
v_y = 15
a_y = -1
dt = 0.2
y = 0
x = -350
k = 0.02  # air resistance coef
# moving turtle to left
turtle.up()
turtle.goto(x, y)
turtle.down()

while not (v_y < 3 and y < 1):
    turtle.setheading(math.atan(v_y / v_x) * 57.3)
    x += v_x * dt
    y += v_y * dt
    turtle.goto(x, y)
    if y < 1:
        v_y = 0.9 * abs(v_y)
        print(y, v_y)
    else:
        v_y += (a_y - k * v_y) * dt  #
    v_x -= k * v_x * dt

turtle.setheading(0)
# hold window
turtle.mainloop()
