"""Uses histogram comparison tests to compare histograms of images"""

"""How to run :
# python compare_histog_sequence.py \\EO-Web\images\ESC\large\ISS045 --log=debug --list="E:\compareHistograms\ISS045_nadir.txt"
"""

# images 22095 - 22406

# import the necessary packages
from filelist import FileList  # import the filelist class
from issimage import ISSIMAGE

import logging

from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
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
colorConversionType = cv2.COLOR_BGR2RGB


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Find lightning in time sequences")
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
name = 'compare_histog_sequence.log'
# if (args.out) :
#     name = args.out + '/' + name
# print "log filename = {}".format(name)

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

# METHOD #1: UTILIZING OPENCV
# initialize OpenCV methods for histogram comparison
OPENCV_METHODS = (  # 4 IS TOO MANY ******* RUNS OUT OF MEMORY ***************
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
#for filename in imagePaths:
# for a number range
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

    hist0 = cv2.calcHist([hsvImage0], [0, 1, 2], None, [8, 8, 8],
                         [0, 256, 0, 256, 0, 256])
    hist1 = cv2.calcHist([hsvImage1], [0, 1, 2], None, [8, 8, 8],
                         [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([hsvImage2], [0, 1, 2], None, [8, 8, 8],
                         [0, 256, 0, 256, 0, 256])

    hist0 = cv2.normalize(hist0, hist0).flatten()
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()

    d10 = []  # comparison b/t image 1 and image 0
    d12 = []  # comparison b/t image 1 and image 2

    # loop over the comparison methods
    for (methodName, method) in OPENCV_METHODS:

        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d10.append(cv2.compareHist(hist1, hist0, method))
        d12.append(cv2.compareHist(hist1, hist2, method))

    # log the results
    logging.info("image = %s", filename)
    logging.info("d10 = %s", d10)
    logging.info("d12 = %s", d12)
    logging.info(" ")



