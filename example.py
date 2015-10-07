import matplotlib.pyplot as plt
import numpy as np
from misc import my_legend, adjust_spines

np.random.seed(314)

n = 1000
x = np.linspace(0, 1, n)

x = np.sort(x)

plt.figure()
for i in range(1,5):
    plt.plot(x, np.sort((np.random.rand(n)-x))**i, label='label_{}'.format(i), clip_on=False)

ax = plt.gca()
my_legend(ax)
adjust_spines(ax)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

