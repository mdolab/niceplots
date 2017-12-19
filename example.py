import matplotlib.pyplot as plt
import numpy as np
import niceplots
import matplotlib.mlab as mlab

# Simple line plot
n = 1000
x = np.linspace(0, 1, n)

plt.figure()
for i in range(1,5):
    plt.plot(x, x**i, label='label_{}'.format(i), clip_on=False)

niceplots.all()
plt.xlabel('x')
plt.ylabel('y')

# Contour plot
delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
# difference of Gaussians
Z = 10.0 * (Z2 - Z1)

plt.figure()

niceplots.all()

im = plt.imshow(Z, interpolation='bilinear', origin='lower',
                extent=(-3,3,-2,2))
levels = np.arange(-1.2, 1.6, 0.2)
CS = plt.contour(Z, levels,
                 origin='lower',
                 linewidths=2,
                 extent=(-3,3,-2,2))
plt.xlabel('example x-axis')
plt.ylabel('example y-axis')
plt.show()
