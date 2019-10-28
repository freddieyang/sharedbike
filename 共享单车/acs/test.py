import numpy as np


a = [2, -2, 2, 2, 2]
a = np.abs(a)
a = a / sum(a)
b = set([1, 2, 3, 4, 5])
print(a)
c = np.random.choice(list(b), p=a)
print(c)
