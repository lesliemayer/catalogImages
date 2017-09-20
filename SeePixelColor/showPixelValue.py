import numpy as np
import matplotlib.pyplot as plt

class Formatter(object):
    def __init__(self, im):
        self.im = im
    def __call__(self, x, y):
        z = self.im.get_array()[int(y), int(x)]
        return 'x={:.01f}, y={:.01f}, z={:.01f}'.format(x, y, z)

data = np.random.random((10,10))

fig, ax = plt.subplots()
im = ax.imshow(data, interpolation='none')
ax.format_coord = Formatter(im)
plt.show()