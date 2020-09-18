import turtle

a = 20
delta_a = 10

turtle.shape('turtle')
for i in range(36):
	turtle.forward(a)
	turtle.left(90)
	a += delta_a

# hold window
turtle.mainloop()
