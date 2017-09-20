"""
Code to automatically make training images using a sliding window

Written by L.R. Mayer  July 2017

This hasn't been tested *****
"""

# To run :

# $ python sliding_window_make_training.py --image E:\ISS051\DayLimb\ISS051-E-11689_binary.jpg
# $ python sliding_window_make_training.py --image E:\ISS051\DayLimb\ISS051-E-12281_binary.jpg  - don't use this one
# $ python sliding_window_make_training.py --image E:\ISS051\DayLimb\ISS051-E-10738_binary.jpg
# $ python sliding_window_make_training.py --image E:\ISS051\DayLimb\ISS051-E-11041_binary.jpg


# to get the local binary patterns descriptor
import sys

#sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel/')

# from pyimagesearch.helpers import pyramid
# from pyimagesearch.helpers import sliding_window
import argparse
import time
import cv2
import os

# =============================================================================
def sliding_window(image, stepSize, windowSize):
    """
    Slide a window across an image
    :param image:  Image to loop over
    :param stepSize: determined on a per-dataset basis
    and is tuned to give optimal performance based on your dataset of images.
    In practice, it's common to use a stepSize  of 4 to 8 pixels.
    :param windowSize:  width and height (in terms of pixels) of the window we are
    going to extract from our imag
    :return:
    """
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

# =============================================================================
outDir = "E:\ISS051\DayLimb\Training/"


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())


# load the image and define the window width and height
origImage = cv2.imread(args["image"])

# resize the image
image = cv2.resize(origImage,None,fx=.25, fy=.25, interpolation = cv2.INTER_AREA)

# window size for sliding window
#(winW, winH) = (128, 128)
(winW, winH) = (256, 256)
stepSize = 64

ii = 0

for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
    # if the window does not meet our desired window size, ignore it
    if window.shape[0] != winH or window.shape[1] != winW:
            continue


    # threshold the image



    # save window as image
    # write out window variable
    outname = outDir + os.path.basename(args["image"]) + "-B" + str(ii) + ".jpg"
    print("outname = {}".format(outname))
    #outname = outDir + "ISS051-E-11689-B" + str(ii) + ".jpg"
    cv2.imwrite(outname, window)
    cv2.imshow("train", window)

    ii += 1


    # since we do not have a classifier, we'll just draw the window
    clone = image.copy()
    cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)


    cv2.imshow("Window", clone)

    cv2.waitKey(1)
    time.sleep(0.25)



