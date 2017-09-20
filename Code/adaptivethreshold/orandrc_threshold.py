# python code orandrc_threshold.py
# LR Mayer, thresholding from OpenCV book (pdf)
# 10/26/2016
#
# Compute threshold value by Otsu's method and Riddler-Calvard method.
# USAGE
# python orandrc_threshold.py I:\ISS051/ --log=debug --list="E:\ISS051\day_earthlimb.txt"


# Otsu's method assumes there are two peaks in the grayscale
# histogram of the image. It then tries to find an optimal
# value to separate these two peaks - thus our value of T.
# While OpenCV provides support for Otsu's method, I (the openCV book author)
# prefer the implementation by Luis Pedro Coelho in the mahotas
# package since it is more Pythonic.

from __future__ import print_function
import numpy as np
import argparse
import mahotas  # for doing the otsu threshold computation
import cv2

import os
import sys
import logging
from imutils import paths
from imutils import resize

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Do 2 kinds of adaptive thresholding on an image")
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
# __file__ is the name of the script running
logging.basicConfig(level=numeric_level, filename= os.path.basename(__file__) + '.log', filemode='w')

# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

if (args.list) :

    if os.path.isfile(args.list):
        with open(args.list) as f:
            #fileList = f.read()
            fileList = []  # initialize fileList
            for line in f:
                fileList.append(line.strip())  # strip off newline, spaces, and append

        logging.debug("fileList = %s",fileList)
        imagePaths = [args.dataset + '/' + i for i in fileList]

    else :
        sys.exit("list file does not exist")

else :

    # -----------------------------------------------------
    # Grab the image paths from the dataset directory
    # -----------------------------------------------------
    imagePaths = list(paths.list_images(args.dataset))

    # does this need to be a numpy array?
    #imagePaths = np.array(sorted(imagePaths))
    imagePaths = sorted(imagePaths)


logging.info("imagePath is %s", imagePaths)


# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")




    # -------------------------------------------
    # Read the image & convert it to gray scale
    # -------------------------------------------
    image = cv2.imread(imagePath)

    # -------------------------------------------------------------------------
    # Resize the image
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    # -------------------------------------------------------------------------
    resized = resize(image, width=500)

    image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", image)

    # smooth the image
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    cv2.imshow("Smoothed Image", blurred)
    cv2.waitKey(0)

    # compute threshold using mahota's python package otsu method
    T = mahotas.thresholding.otsu(blurred)
    print("Otsu's threshold: {}".format(T))

    # copy grayscale image & set to thresh
    thresh = image.copy()

    # Set every pixel > otsu threshold to 255 (white)
    thresh[thresh > T] = 255

    # Set every thing else not white to black
    thresh[thresh < 255] = 0

    # invert thresh
    thresh = cv2.bitwise_not(thresh)
    cv2.imshow("Otsu", thresh)

    # compute the threshold using the Riddler-Calvard method :
    T = mahotas.thresholding.rc(blurred)
    print("Riddler-Calvard: {}".format(T))

    # copy the grayscale image, set everything > T to white, rest to black, then invert
    thresh = image.copy()
    thresh[thresh > T] = 255
    thresh[thresh < 255] = 0
    thresh = cv2.bitwise_not(thresh)
    cv2.imshow("Riddler-Calvard", thresh)
    cv2.waitKey(0)
