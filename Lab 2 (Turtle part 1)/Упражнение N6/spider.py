import turtle

n = 12

turtle.shape('turtle')
for i in range(n):
	turtle.right(360 / n)
	turtle.forward(100)
	turtle.stamp()
	turtle.backward(100)

# hold window
turtle.mainloop()
