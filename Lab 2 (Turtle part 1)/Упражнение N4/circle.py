import turtle

turtle.shape('turtle')

# making (0, 0) the center of circle
turtle.penup()
turtle.goto(0, (-10/3*57.3))
turtle.pendown()

turtle.forward(10)
for i in range(int(360 / 3)):
	turtle.left(3)
	turtle.forward(10)

# hold window
turtle.mainloop()