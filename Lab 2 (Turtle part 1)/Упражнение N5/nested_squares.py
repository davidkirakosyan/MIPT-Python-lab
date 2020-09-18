import turtle

# defining square side and difference
a = 50
delta = 50
delta = delta - (delta % 2)

turtle.shape('turtle')
for i in range(10):
	for j in range(4):
		turtle.forward(a)
		turtle.left(90)
	if i < 9:
		turtle.penup()
		x, y = turtle.pos()
		x -= delta / 2
		y -= delta / 2
		turtle.goto(x, y)
		turtle.pendown()
		a += delta

# hold window
turtle.mainloop()