"""Code to test image segmentation using Kmeans with markers"""

import os
import sys
import logging
import numpy as np
import cv2
from issimage import ISSIMAGE
from genericimage import GENERICIMAGE

filename = r'E:\BetterLightning\ISS045-E-1637.jpg'
#filename = r'E:\BetterLightning\ISS045-E-3537.jpg'
#filename = r'E:\BetterLightning\ISS030-E-149855.jpg'
filename = r'E:\ISS050\Clouds\ISS050-E-36940.jpg'
filename = r'E:\ISS050\Clouds\ISS050-E-19440.jpg'
#filename = r'E:\ISS050\Clouds\ISS050-E-19167.jpg'  # mostly cloud - very good segmentation of clouds
filename = r'I:\ISS051\ISS051-E-30996.jpg' # clouds
filename = r'I:\ISS051\ISS051-E-31616.jpg' # clouds
filename = r'I:\ISS051\ISS051-E-31631.jpg' # clouds
filename = r'I:\ISS051\ISS051-E-31684.jpg' # coastline
filename = r'I:\ISS051\ISS051-E-36209.jpg' # clouds & land
filename = r'I:\ISS051\ISS051-E-36263.jpg' # puffy clouds, mostly land
filename = r'I:\ISS051\ISS051-E-36724.jpg' # mountains
filename = r'E:\Clouds\smallClouds\smallCloud1.jpg' # clouds & mountain
filename = r'E:\Clouds\smallClouds\smallCloud2.jpg' # clouds & mountain
#filename = r'E:\Clouds\smallClouds\smallCloud3.jpg' # clouds & mountain


if not os.path.isfile(filename):
    sys.exit("filename " + filename + "  does not exist")

logging.info("Filename = %s", filename)

# Check to see if it's an ISS image
index = filename.find('ISS')

if (index == -1):
    # set up the GENERICIMAGE object
    issimg = GENERICIMAGE(filename)
else:
    # set up the ISSIMAGE object
    issimg = ISSIMAGE(filename)

# resize the image
# -------------------
# Resize the image
# -------------------
issimg.resize(800)

gray = cv2.cvtColor(issimg.image,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray scale",gray)

ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

cv2.imshow("threshold", thresh)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
cv2.imshow("opening", opening)


# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)
cv2.imshow("sure background", sure_bg)


# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)


ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
cv2.imshow("sure foreground",sure_fg)

unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(issimg.image,markers)
issimg.image[markers == -1] = [255,0,0]

cv2.imshow("segmented", issimg.image)

cv2.imwrite("segmentedImage.jpg", issimg.image)


cv2.waitKey(0)