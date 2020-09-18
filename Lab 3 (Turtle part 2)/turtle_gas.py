from random import random, randint
import math
import turtle


def draw_walls(x_max, y_max):
    turtle.up()
    turtle.goto(-x_max, -y_max)
    turtle.down()
    for i in range(2):
        turtle.forward(x_max * 2)
        turtle.left(90)
        turtle.forward(y_max * 2)
        turtle.left(90)
    turtle.hideturtle()


def init(number_of_molecs):
    velocity = []
    molecs = [turtle.Turtle(shape='circle') for i in range(number_of_molecs)]
    for unit in molecs:
        unit.penup()
        unit.speed(0)
        color = (random(), random(), random()) # generating color for molecules
        unit.color(color)
        unit.shapesize(0.7)
        unit.goto(randint(-x_max, x_max), randint(-y_max, y_max)) # generating position and velocity
        velocity.append({'vx': randint(-v_max, v_max),
                         'vy': randint(-v_max, v_max)
                         })
        unit.pendown()
    return molecs, velocity


def move(steps_of_time_number, pool, velocity):
    for i in range(steps_of_time_number):
        for j, unit in enumerate(pool):
            x, y = unit.xcor(), unit.ycor()
            # bounce from walls
            if x + x_max < 5 or x_max - x < 5:
                velocity[j]['vx'] *= -1
            if y + y_max < 5 or y_max - y < 5:
                velocity[j]['vy'] *= -1
            # check for collisions
            for k, other in enumerate(pool):
                if k == j:
                    continue
                is_touching = abs(x - other.xcor()) < 2 * v_max and abs(y - other.ycor()) < 2 * v_max
                if is_touching:
                    # changing with velocities
                    velocity[j]['vx'], velocity[k]['vx'] = velocity[k]['vx'], velocity[j]['vx']
                    velocity[j]['vy'], velocity[k]['vy'] = velocity[k]['vy'], velocity[j]['vy']
                    break
            vx, vy = velocity[j]['vx'], velocity[j]['vy']
            unit.goto(x + vx, y + vy)


number_of_molecs = 6
steps_of_time_number = 500
v_max = 5
x_max, y_max = 200, 200

draw_walls(x_max, y_max)
molecules, velocities = init(number_of_molecs)
move(steps_of_time_number, molecules, velocities)

# hold window
turtle.mainloop()
