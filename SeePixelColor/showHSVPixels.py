import os # for checking file existence
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

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
        return 'h:{}, s:{}, v:{}'.format(z[0], z[1], z[2])

# End of Formatter class ======================================================================

imageName = r'F:\imagews\training/Night_ISS028-E-26583.jpg'
imageName = r'F:\imagews\training/Aurora_ISS037-E-6351.jpg'
imageName = r'F:\imagews\training/Night_ISS028-E-26555.jpg'
imageName = r'F:\imagews\training/Aurora_ISS027-E-11772.jpg'
imageName = r'F:\imagews\training/Limbnight_ISS037-E-5988.jpg'
imageName = r'F:\imagews\training/Limbnight_ISS037-E-8838.jpg'
imageName = r'F:\imagews\training/Aurora_ISS009-E-28575.jpg'  # is aurora but didn't not get detected ***
imageName = r'E:\Lightning\ISS029-E-34356.jpg'
imageName = r'E:\Lightning\ISS043-E-3092.jpg'
#imageName = r'E:\Lightning\ISS029-E-34335.jpg'
#imageName = r'E:\BetterLightning\ISS045-E-1549.jpg'
#imageName = r'E:\BetterLightning\ISS045-E-1577.jpg'
#imageName = r'E:\BetterLightning\ISS045-E-3536.jpg'
#imageName = r'E:\BetterLightning\Color_Block\ISS045-E-3536_open.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-29294.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-34271.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-13429.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-11806.jpg'

#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-13413.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-34277.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-34271.jpg'
imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-11816.jpg'
imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-11816_filter.jpg'
imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-11816_open.jpg'
imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-29097.jpg'
# imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-29100.jpg'
# imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-29100_filter.jpg'
# #imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-29100_open.jpg'
# imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-29102_open.jpg'
# imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-29107_open.jpg'
#imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-34242_open.jpg'
#imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-12958_open.jpg'
#imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-37264_filter.jpg'
#imageName = r'E:\ISS050\SumInertiaBrightWhite\ISS050-E-37264_open.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-11819.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-13420.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS045\ISS045-E-5272.jpg'


# nadir lightning
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-61118.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-61120.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-66006.jpg'
#imageName = r'\\EO-Web\images\ESC\large\ISS050\ISS050-E-29110.jpg'

# clouds
imageName = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel\images\training\cloud\cloud1.jpg'
imageName = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel\images\training\cloud\cloud1.jpg'
#imageName = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel\images\training\cloud\cloud7.jpg'
imageName = r'E:\ISS050\Clouds\ISS050-E-35099.jpg'




# Check to make sure the file exists :
if not os.path.isfile(imageName):
    sys.exit("imageName " + imageName + "  does not exist")

#data = np.random.random((10,10))
data = cv2.imread(imageName)

# Convert color
#bw = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)


# the subplots (2 different plots)
fig, axes = plt.subplots()

# the image plot
#im = axes.imshow(data, interpolation='none')
im = axes.imshow(hsv, interpolation='none')
print (im)

# format the axes subplot
axes.format_coord = Formatter(im)
plt.show()