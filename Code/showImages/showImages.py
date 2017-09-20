"""Given a list of images, resize them, and display.
   Written by L.R. Mayer
"""
# USAGE
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\earthlimb.txt"
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\circle.txt"
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\ISS.txt"
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python showImages.py F:\imagews\training --log=debug --list="F:\imagews\training\limbnight.txt"

# python showImages.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt"

# import the necessary packages
import logging
import argparse
import os # to check list file existence
import sys
import logging #  To write messages to a logfile

import cv2
import numpy as np
from imutils import paths

# # for getting focal length from the photos database
# from photosdb import PHOTOSDB
from issimage import ISSIMAGE

showHist = False

# -----------------------
# For checking the path
# -----------------------
# print '\n'.join(sys.path)
# sys.exit(0)

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Find the earth limb in images")
ap.add_argument("dataset", help="Path to images")  # this is required

# Add logging file argument
ap.add_argument("-l", "--log", help="Logging Value", default="info")

# Add list file argument
ap.add_argument("-li", "--list", help="List of images to read")

# parse the arguments
args = ap.parse_args()

# -----------------------------------------------
# Display the images while looping through them?
# -----------------------------------------------
showContours = False


# ------------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='showImages.log', filemode='w')

# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

# --------------------------------
# Read the file names into a list
# --------------------------------
if (args.list) :

    if os.path.isfile(args.list):
        with open(args.list) as f:
            fileList = []  # initialize fileList
            for line in f:
                fileList.append(line.strip())  # strip off newline, spaces, and append filename to list

        logging.debug("fileList = %s",fileList)
        imagePaths = [args.dataset + '/' + i for i in fileList]

    else :
        sys.exit("list file does not exist")

else :

    # -----------------------------------------------------
    # Grab the image paths from the dataset directory
    # -----------------------------------------------------
    imagePaths = list(paths.list_images(args.dataset))

    # sort the filenames
    imagePaths = sorted(imagePaths)


logging.debug("imagePaths is %s", imagePaths)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")

    # initialize ISSIMAGE class for setting up the image
    xx = ISSIMAGE(imagePath)

    xx.resize()

    xx.show()

    # plot histogram for this image
    if showHist :
        xx.plot_color_hist()

    cv2.waitKey(0)

    cv2.destroyAllWindows()