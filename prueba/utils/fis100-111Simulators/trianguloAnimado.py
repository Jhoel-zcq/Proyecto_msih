import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

tf = 3
grav = 10
vi = 10
angv = 15
viy = vi * np.sin(np.deg2rad(angv))
vix = vi * np.cos(np.deg2rad(angv))
dy = -10

fig, ax = plt.subplots()
ax.set(xlim=(0, 30), ylim=(-20, 20))

line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

xdata, ydata = [], []

def animate(i):
    t = 0.01 * i

    x = t * vix
    y = -grav/2 *t**2 + t*viy - dy

    xdata.append(x)
    ydata.append(y)

    line.set_data(xdata, ydata) 

    return line,

anim = animation.FuncAnimation(fig,
                               animate,
                               init_func=init,
                               frames=120,
                               interval=50,
                               repeat=True)

plt.show()