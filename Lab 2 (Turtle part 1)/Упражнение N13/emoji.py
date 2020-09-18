import turtle

def main():
	init()
	# face
	turtle.fillcolor('yellow')
	turtle.begin_fill()
	arc(100, 360)
	turtle.end_fill()

	turtle.fillcolor('blue')
	# left eye
	turtle.goto(-38, 75)
	turtle.begin_fill()
	arc(15, 360)
	turtle.end_fill()
	# right eye
	turtle.goto(38, 75)
	turtle.begin_fill()
	arc(15, 360)
	turtle.end_fill()
	# nose
	turtle.fillcolor('black')
	turtle.width(10)
	turtle.goto(0, 60)
	turtle.pendown()
	turtle.sety(30)
	turtle.penup()
	# mouth
	turtle.pencolor('red')
	turtle.goto(-50, 0)
	turtle.right(38)
	arc(82, 80)

	turtle.hideturtle()
	# hold window
	turtle.mainloop()


def init():
	turtle.shape('turtle')
	turtle.speed(0)
	turtle.penup()
	turtle.sety(-50)


def arc(radius, angle):
	'''Drawing two opposite circles.'''
	turtle.pendown()
	step = radius * 3 / 57.3
	for i in range(int(angle / 3)):
		turtle.forward(step)
		turtle.left(3)
	turtle.penup()


main()