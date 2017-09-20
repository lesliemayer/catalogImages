
"""
 python code simple_threshold.py
# LR Mayer, thresholding from OpenCV book (pdf)
# 05/25/2017
#
# Compute threshold value by Otsu's method and Riddler-Calvard method.
# USAGE

# python simple_threshold.py I:\ISS051/ --log=debug --list="E:\ISS051\day_earthlimb.txt" --out="E:\ISS051\DayLimb/"
# python simple_threshold.py I:\ISS051/ --log=debug --list="E:\ISS051\TrainLimb/DayLimb/dayLimb.txt" --out="E:\ISS051\TrainLimb/DayLimb/Binary/"
# python simple_threshold.py I:\ISS051/ --log=debug --list="E:\ISS051\TrainLimb/NoDayLimb/nodayLimb.txt" --out="E:\ISS051\TrainLimb/NoDayLimb/Binary/"
# python simple_threshold.py I:\ISS051/ --log=debug --list="E:\ISS051\TrainLimb/obscuredDayLimb/obscuredlimb.txt" --out="E:\ISS051\TrainLimb/NoDayLimb/Binary/"
"""

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

from filelist import get_filename

# ------------------------------------------
# Do we want to save the images to a file?
# ------------------------------------------
writeImage = True


# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Do simple thresholding on an image")
ap.add_argument("dataset", help="Path to images")  # this is required

# Add logging file argument
ap.add_argument("-l", "--log", help="Logging Value", default="info")

# Add list file argument
ap.add_argument("-li", "--list", help="List of images to read")

# Add out argument
ap.add_argument("-ou", "--out", help="Output File Directory")

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
    imagePaths = sorted(imagePaths)  # sort the images


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
    resized = resize(image, width=300)
    cv2.imshow("Resize", resized)

    # ------------------------------------------------------
    # Smooth the image
    # nn = the neighborhood size
    # For finding the limb, want the image to be very smooth
    # -------------------------------------------------------
    nn = 11  # Get less edges w/ higher n

    # -----------------------------------------------
    # Bilateral filtering preserves the edges
    # 2nd parameter is the window size for smoothing
    # -----------------------------------------------
    #filtered = cv2.bilateralFilter(image, nn, 75, 75)
    filtered = cv2.bilateralFilter(resized, nn, 15, 15)

    cv2.imshow("bilateral filter", filtered)

    image = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)


    # smooth the image
    # blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # cv2.imshow("Smoothed Image", blurred)
    # cv2.waitKey(0)



    # compute threshold using mahota's python package otsu method
    # T = mahotas.thresholding.otsu(blurred)
    # print("Otsu's threshold: {}".format(T))

    # threshold on the value array
    # 25, 100 is too high for black threshold
    #ret, thresh = cv2.threshold(image[:,:,2], 25, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(image[:, :, 2], 20, 255, cv2.THRESH_BINARY_INV)
    ret, thresh = cv2.threshold(image[:, :, 2], 10, 255, cv2.THRESH_BINARY_INV)
    #print("shape of thresh: {}".format(thresh.shape))


    cv2.imshow("Threshold 10", thresh)


    # OTSU threshold ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # compute threshold using mahota's python package otsu method
    T = mahotas.thresholding.otsu(image)
    print("Otsu's threshold: {}".format(T))

    # copy value image & set to thresh
    thresh2 = image[:, :, 2].copy()

    # Set every pixel > otsu threshold to 255 (white)
    thresh2[thresh2 > T] = 255

    # Set every thing else not white to black
    thresh2[thresh2 < 255] = 0

    # invert thresh
    thresh2 = cv2.bitwise_not(thresh2)
    cv2.imshow("Otsu", thresh2)
    cv2.waitKey(0)

    if (writeImage and args.out):

        outname = args.out + '/' + get_filename(imagePath) + '_binary.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, thresh2)