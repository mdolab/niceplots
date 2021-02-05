import random
from niceplots import horiz_bar

try:
    # use random words for the example
    word_file = "/usr/share/dict/words"
    words = open(word_file).read().splitlines()
    wl = len(words)

    def rw():
        return random.choice(words)

    header = [rw(), rw()]
    n = 15  # number of bars to create
    labels = [rw() for i in range(n)]
    times = [random.random() * random.randint(0, 1000) for i in range(n)]
    nd = 1

except:  # if user is not on a *nix system
    header = ["Method", "Time (sec)"]
    labels = ["Analytic Forward", "Analytic Adjoint", "FD Forward Diff.", "FD Central Diff.", "FD Backward Diff."]
    times = [0.00456, 0.00847, 0.0110, 0.0213, 0.011]
    nd = 4

horiz_bar(labels, times, header, nd=nd)
