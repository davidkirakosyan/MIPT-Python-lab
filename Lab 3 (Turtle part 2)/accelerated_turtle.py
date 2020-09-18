import turtle

# horizon line
turtle.goto(400, 0)
turtle.goto(-400, 0)
# initial conditions
v_x0 = 7
v_y = 12
a_y = -1
dt = 0.5
y = 0
x = -400
# moving turtle to left
turtle.up()
turtle.goto(x, y)
turtle.down()

turtle.speed(1)
for i in range(200):
    turtle.goto(x, y)
    x += v_x0 * dt
    y += v_y * dt
    if abs(y) < 2:
        v_y = abs(v_y)
    else:
        v_y += a_y * dt

# hold window
turtle.mainloop()
