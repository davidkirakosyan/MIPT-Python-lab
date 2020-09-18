import turtle

def main():
	init()
	big = 50
	small = 10
	half_circle(big)
	for i in range(4):
		half_circle(small)
		half_circle(big)

	# hold window
	turtle.mainloop()


def init():
	turtle.shape('turtle')
	turtle.left(90)
	turtle.penup()
	turtle.setx(-200)


def half_circle(radius):
	'''Drawing half circle.'''
	turtle.pendown()
	step = radius * 3 / 57.3
	for i in range(int(180 / 3)):
		turtle.forward(step)
		turtle.right(3)
	turtle.penup()


main()