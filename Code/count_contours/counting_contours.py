# python code counting_contours.py
# LR Mayer from OpenCV book (pdf)
# 09/07/2016
#
# using edges to count countours :
# adapted from the OpenCV counting_coins.py example code
#
# arguments : -i  "E:\janice_code_and_data\Copied D Drive\Python_Scripts\OpenCV2\datas\training\SmallISS037-E-2413.jpg"
# arguments : -i  "E:\janice_code_and_data\Copied D Drive\Python_Scripts\OpenCV2\datas\training\SmallISS037-E-5930.jpg"
# arguments : -i  "Smallcoins.jpg"

# we are going to use these edges to help us find the
# actual coins in the image and count them.
# OpenCV provides methods to find 'curves' in an image,
# called contours. A contour is a curve of points, with no
# gaps in the curve. Contours are extremely useful for such
# things as shape approximation and analysis.
# In order to find contours in an image, you need to first obtain
# a binarization of the image, using either edge detection
# methods or thresholding. In the examples below, we'll use
# the Canny edge detector to find the outlines of the coins,
# and then find the actual contours of the coins.

from __future__ import print_function
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
    help = "Path to the image")
args = vars(ap.parse_args())

# read image & convert to gray scale
image = cv2.imread(args["image"])
cv2.imshow("Image", image)
#image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
gray =  cv2.cvtColor(image,   cv2.COLOR_BGR2GRAY)

# smooth the image
# nn = the neighborhood size
nn = 11
#nn = 5
blurred = cv2.GaussianBlur(gray, (nn, nn), 0)
cv2.imshow("Image", image)

# compute edges on the smoothed image
# any gradient values below 30 are considered
# non-edges whereas any values above 150 are considered
# sure edges.
#edged = cv2.Canny(blurred, 30, 150)  good for city lights
edged = cv2.Canny(blurred, 30, 50)


cv2.imshow("Edges", edged)

# find the contours of the edges. cnts is the returned contours
# This method returns
# a 3-tuple of: (1) our image after applying contour detection
# (which is modified and essentially destroyed), (2) the
# contours themselves, cnts, and (3) the hierarchy of the contours
# (OpenCV 3.0 is different from OpenCV 2.4, which returns a tuple of 2)
# This function is destructive
# to the image you pass in. If you intend using that image
# later on in your code, it's best to make a copy of it, using
# the NumPy copy method.
# The second argument is the type of contours we want.
# We use cv2.RETR_EXTERNAL to retrieve only the outermost
# contours (i.e., the contours that follow the outline of the
# coin). We can also pass in cv2.RETR_LIST to grab all contours.
# Other methods include hierarchical contours using
# cv2.RETR_COMP and cv2.RETR_TREE, but hierarchical contours
# are outside the scope of this book.
# of resources.
# Our contours cnts is simply a Python list. We can use
# the len function on it to count the number of contours that
# were returned.
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

print("I count {} coins in this image".format(len(cnts)))

# copy the original image
# Now, we are able to draw our contours. In order not to
# draw on our original image, we make a copy of the original
# image
coins = image.copy()

# draw the contours in green on the coins image
# contour index of -1 means draw all contours.  If just
# wanted to draw ith contour, just enter i
# The last argument is the thickness of the line we
# are drawing. We'll draw the contour with a thickness of
# two pixels.
cv2.drawContours(coins, cnts, -1, (0, 255, 0), 2)
cv2.imshow("Coins", coins)
cv2.waitKey(0)

# here is some code to draw the first, second,
# and third contours, respectively:
# cv2.drawContours(coins, cnts, 0, (0, 255, 0), 2)
# cv2.drawContours(coins, cnts, 1, (0, 255, 0), 2)
# cv2.drawContours(coins, cnts, 2, (0, 255, 0), 2)

# crop each individual coin from the image:
# i is the # of the contour, c is the contour
for (i, c) in enumerate(cnts):
    # cv2.boundingRect finds the 'enclosing box' that our contour will fit into, allowing us
    # to crop it from the image.The function takes a single parameter, a contour, and then
    # returns a tuple of the x and y position that the rectangle starts at, followed by
    # the width and height of the rectangle. We then crop the coin from the image
    # using our bounding
    (x, y, w, h) = cv2.boundingRect(c)
    print("Coin #{}".format(i + 1))

    # crop the coin from the image using our bounding
    # box coordinates and NumPy array slicing & show it
    coin = image[y:y + h, x:x + w]
    cv2.imshow("Coin", coin)  # show the bounding box

    # initialize our mask as a NumPy array of zeros,
    # with the same width and height of our original image.
    print ("image.shape = {}".format(image.shape))
    print ("image.shape[:2] = {}".format(image.shape[:2]))  # the 1st two values in the tuple, y,x
    mask = np.zeros(image.shape[:2], dtype = "uint8")

    # get the minimum enclosing circle of the countour c, fits a circle to the contour
    # get back the center of the circle, and radius
    ((centerX, centerY), radius) = cv2.minEnclosingCircle(c)
    print ("centerX {}, centerY {}, radius {}".format(centerX,centerY,radius))

    # make a circle, same size as coin, of all white to use as a mask
    cv2.circle(mask, (int(centerX), int(centerY)), int(radius), 255, -1)

    # crop the mask to the bounding rectangle
    mask = mask[y:y + h, x:x + w]
    # and the coin w/ the mask, then show the masked coin
    cv2.imshow("Masked Coin", cv2.bitwise_and(coin, coin, mask = mask))
    cv2.waitKey(0)