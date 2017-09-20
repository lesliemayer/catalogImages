# python code imutils.py
#
# LR Mayer from OpenCV book (pdf)
# 08/22/2016
#
# Defining our own imutils package :


import numpy as np
import cv2
from matplotlib import pyplot as plt
import __future__  # for the print function so that it works in python 3

# function to translate an image in the x & y direction
def translate(image, x, y):

    print("in self defined imutils function translate **************************************")

    M = np.float32([[1, 0, x], [0, 1, y]])

    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return shifted

# function to rotate an image
# angle is the angle which to rotate the image
# scale is how much to scale the size of the image, the default is 1.0
def rotate(image, angle, center = None, scale = 1.0):

    # get height & width of image
    (h, w) = image.shape[:2]

    # if center is a value of None, calculate center from h, w
    if center is None:
        center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)

    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

# function for resizing an image w/ openCV
def resize(image, width = None, height = None, inter = cv2.INTER_AREA):

    # Default interpolation is cv2.INTER_AREA

    # set dim to not a value
    dim = None

    # get the height, width of current image
    (h, w) = image.shape[:2]

    # check that width or height is set, if not return original image
    if width is None and height is None:
       return image

    # calculate width from the give height
    if width is None:
        r = height / float(h)

        dim = (int(w * r), height)

    # calculate height from width
    else:

      r = width / float(w)

      dim = (width, int(h * r))

    # end if


    #resized = cv2.resize(image, dim, interpolation = inter)
    resized = cv2.resize(image, dim, interpolation=CV_INTER_AREA)  # better for shrinking
    # CV_INTER_LINEAR is better for zooming.   This is the default
    # CV_INTER_CUBIC is slow



    return resized

# Plot histogram of an image :

def plot_color_hist(image):
    # get each separate color channel (BGR)
    chans = cv2.split(image)
    colors = ("b", "g", "r")
    plt.figure()
    plt.title("Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")

    for (chan, color) in zip(chans, colors):
        # hist = cv2.calcHist([chan], [0], None, [256], [0, 256]) # sometimes this will crash python
        hist, bins = np.histogram(chan.ravel(), 256, [0, 256])
        plt.plot(hist, color = color)
        plt.xlim([0, 256])

    plt.show()

    return
