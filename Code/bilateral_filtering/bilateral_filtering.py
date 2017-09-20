# USAGE
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora_nightlimb.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\limbnight.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\iss.txt"
# python find_color_hsv.py E:\Lightning\ --log=debug --list="E:\Lightning\lightning.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\no_lightning.txt"

# import the necessary packages
import argparse
import os # to check list file existence
import sys
import logging #  To write messages to a logfile

import cv2
import numpy as np
from imutils import paths
from imutils import resize

# -----------------------
# For checking the path
# -----------------------
#print '\n'.join(sys.path)
#sys.exit(0)

numFilters = 5


# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Use color blocking to find things in images")
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
logging.basicConfig(level=numeric_level, filename='bilateral_filtering.log', filemode='w')



# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

# ---------------------------------------------------------------------
# Define the upper and lower boundaries for a color
# to be considered "green"
# This defines
# the lower and upper limits of the shades of green in the HSV
# color space.
# ----------------------------------------------------------------------

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

    imagePaths = sorted(imagePaths)


logging.info("imagePath is %s", imagePaths)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")

    logging.debug("Reading %s", imagePath)

    # load the image, describe the image, update the list of data
    image = cv2.imread(imagePath)

    # resize the image
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    resized = resize(image, width=500)
    #
    cv2.imshow("resized", resized)
    #cv2.waitKey(0)


    for i in range(0, numFilters):
        #resized = cv2.GaussianBlur(resized, (5,5), 0)
        filtered = cv2.bilateralFilter(resized, 9, 75, 75)

    cv2.imshow("bilateral filter", filtered)

    # Convert the image color space to HSV
    #hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    cv2.waitKey(0)


# destroy pointer & all windows
cv2.destroyAllWindows()