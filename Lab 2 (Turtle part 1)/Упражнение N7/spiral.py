import turtle

# r = phi
delta_phi = 3
phi = 0

turtle.shape('turtle')
for i in range(1200):
    # ds = r * d(phi) = phi * d(phi)   phi in radians
    s = (phi) * (delta_phi) / 650
    turtle.left(delta_phi)
    turtle.forward(s)
    phi += delta_phi

# hold window
turtle.mainloop()
