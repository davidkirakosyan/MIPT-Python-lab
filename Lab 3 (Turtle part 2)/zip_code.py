import turtle

# reading movements from DIGITS.txt
with open('DIGITS.txt') as file:
    DIGITS = []
    for line in file.readlines()[1:]:  # pass comment
        line = line[:-1]  # remove \n
        line = line.split(', ')
        DIGITS.append(tuple(tuple(map(int, step.split())) for step in line))


def write_digit(x_init=0, y_init=0, step=30):
    turtle.goto(x_init, y_init)
    for j, (x, y, angle) in enumerate(DIGITS[i]):
        if j == 1:
            turtle.down()
        turtle.goto(x_init + x * step, y_init + y * step)
        turtle.left(angle)
    turtle.up()
    turtle.setheading(0)


zip_code = '141700'
zip_code = list(map(int, list(zip_code)))

turtle.shape('turtle')
turtle.width(2)
turtle.up()
step = 40
# align zip code
x_pos = -len(zip_code) * 30
y_pos = 50
for i in zip_code:
    write_digit(x_pos, y_pos, step)
    x_pos += step * 1.5

turtle.hideturtle()
# hold window
turtle.mainloop()
