import numpy as np
import matplotlib.pyplot as plt
import cv2
from imutils import resize

class Formatter(object):
    def __init__(self, im):
        self.im = im

    # def __call__(self, x, y):
        # z is getting the value at y, x
    #     #z = self.im.get_array()[int(y), int(x)]
    #     #return 'x={:.01f}, y={:.01f}, z={:.01f}'.format(x, y, z)


    def __call__(self, x, y):
        # the x,y axes values, changes w/ movement of mouse
        #print (x,y)
        # Get the rgb values at position y, x
        z = self.im.get_array()[int(y), int(x)]
        print z
        #return 'x={:.01f}, y={:.01f}, z={:.01f}'.format(x, y, z)
        return 'r:{}, g:{}, b:{}'.format(z[0], z[1], z[2])


imageName = r'F:\imagews\training/Night_ISS028-E-26583.jpg'
imageName = r'F:\imagews\training/Aurora_ISS037-E-6351.jpg'
imageName = r'F:\imagews\training/Night_ISS028-E-26555.jpg'
imageName = r'E:\Lightning\ISS043-E-3092.jpg'
imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-29294.jpg'
imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-37264.jpg'
imageName = r'E:\ISS050\ISS050-E-37264_open.jpg'
imageName = r'E:\ISS050\ISS050-E-37264_filter.jpg'



#data = np.random.random((10,10))
data = cv2.imread(imageName)
#bw = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
#hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)

#data = resize(data, width=500)

# the subplots (2 different plots)
fig, axes = plt.subplots()

# the image plot
im = axes.imshow(data, interpolation='none')
print (im)

# format the axes subplot
axes.format_coord = Formatter(im)
plt.show()