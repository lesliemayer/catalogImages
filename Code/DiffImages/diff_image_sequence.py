"""Difference time sequence images"""

"""How to run :
# python diff_image_sequence.py \\EO-Web\images\ESC\large\ISS045 --log=debug --list="E:\compareHistograms\ISS045_nadir.txt"
# python diff_image_sequence.py \\EO-Web\images\ESC\large\ISS048 --log=debug --list="E:\LightningSequences\ISS048_lightning_seq.txt"
"""

# images 22095 - 22406

# import the necessary packages
from filelist import FileList  # import the filelist class
from issimage import ISSIMAGE

import logging

# from scipy.spatial import distance as dist
# import matplotlib.pyplot as plt
# import numpy as np
import argparse
# import glob
import cv2
import os


# options :
# ------------------
# Smooth the image?
# ------------------
doSmoothing = False

# ------------------------------
# Set type of color conversion :
# ------------------------------
#colorConversionType = cv2.COLOR_BGR2HSV
#colorConversionType = cv2.COLOR_BGR2RGB
colorConversionType = cv2.COLOR_BGR2GRAY


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Difference images in the time sequence")
ap.add_argument("dataset", help="Path to images")  # this is required

# Add logging file argument
ap.add_argument("-l", "--log", help="Logging Value", default="info")

# Add list file argument
ap.add_argument("-li", "--list", help="List of images to read")

# parse the arguments
args = ap.parse_args()

# ------------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)

# The logging filename (goes in current directory unless args.out exists)
name = 'diff_image_sequence.log'

# set up the logging file :
# **** if there is problem w/ logging file will quietly go on unless you catch it ********
try:
    logging.basicConfig(level=numeric_level, filename=name, filemode='w')
except Exception, e:
    print 'Error setting up log file {}'.format(name)
    sys.exit(1)


if (doSmoothing):
    logging.info("Doing smoothing")


# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)


# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.dataset,  args.list)
imagePaths = theList.getPathFilenames()


logging.info("imagePath is %s", imagePaths)

# Set the window sizes to show images
cv2.namedWindow('d10', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('d10', 4928, 3280)  # too big
cv2.resizeWindow('d10', 640, 426)  # too big


cv2.namedWindow('d12', cv2.WINDOW_NORMAL)
cv2.resizeWindow('d12', 640, 426)

cv2.namedWindow('image0', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image0', 640, 426)

cv2.namedWindow('image1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image1', 640, 426)

cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image2', 640, 426)

cv2.namedWindow('d12-d10', cv2.WINDOW_NORMAL)
cv2.resizeWindow('d12-d10', 640, 426)


# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for ii in range(1, len(imagePaths), 1):

    filename = imagePaths[ii]   # will need to change this later
    if not os.path.isfile(filename):
        sys.exit("filename " + filename + "  does not exist")

    logging.info("Filename = %s", filename)

    # set up the ISSIMAGE object
    issimg0 = ISSIMAGE(imagePaths[ii-1])
    issimg1 = ISSIMAGE(imagePaths[ii])
    issimg2 = ISSIMAGE(imagePaths[ii+1])

    logging.info("comparing %s %s %s", imagePaths[ii-1], imagePaths[ii], imagePaths[ii+1])

    # Smooth the image
    if (doSmoothing):
        filtered0 = cv2.bilateralFilter(issimg0.image, 9, 75, 75)
        filtered1 = cv2.bilateralFilter(issimg1.image, 9, 75, 75)
        filtered2 = cv2.bilateralFilter(issimg2.image, 9, 75, 75)
    else:
        filtered0 = issimg0.image.copy()
        filtered1 = issimg1.image.copy()
        filtered2 = issimg2.image.copy()

    # convert to HSV color space
    hsvImage0 = cv2.cvtColor(filtered0, colorConversionType)
    hsvImage1 = cv2.cvtColor(filtered1, colorConversionType)
    hsvImage2 = cv2.cvtColor(filtered2, colorConversionType)

    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index


    # compute the distance between the two histograms
    # using the method and update the results dictionary
    d10 = cv2.subtract(hsvImage1, hsvImage0)
    d12 = cv2.subtract(hsvImage1, hsvImage2)

    # Subtract the subtraction
    bothSub = cv2.subtract(d12, d10)

    # Show the original images
    cv2.imshow('image0', issimg0.image)
    cv2.imshow('image1', issimg1.image)
    cv2.imshow('image2', issimg2.image)

    # Show the 3 images along with the difference
    cv2.imshow("d10", d10)
    cv2.imshow("d12", d12)

    # difference of the difference
    cv2.imshow("d12-d10", bothSub)

    cv2.waitKey(0)


    # log the results
    logging.info("image = %s", filename)
    logging.info("d10 = %s", d10)
    logging.info("d12 = %s", d12)
    logging.info(" ")



