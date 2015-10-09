import matplotlib.pyplot as plt
import numpy as np
import misc

np.random.seed(3141)

n = 1000
x = np.linspace(0, 1, n)

x = np.sort(x)

plt.figure()
for i in range(1,4):
    plt.plot(x, x**i, label='label_{}'.format(i), clip_on=False)


misc.all()
plt.xlabel('x')
plt.ylabel('y')
plt.show()