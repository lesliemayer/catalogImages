""""""


# USAGE
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora_nightlimb.txt"
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\limbnight.txt"
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\iss.txt"
# python test_morph.py E:\Lightning\ --log=debug --list="E:\Lightning\lightning.txt"
# python test_morph.py F:\imagews\training --log=debug --list="F:\imagews\training\no_lightning.txt"

# import the necessary packages
import argparse
import os # to check list file existence
import sys
import logging #  To write messages to a logfile
import numpy as np

import cv2
from imutils import resize
from filelist import FileList  # import the filelist class

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Test different morphology effects on images")
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
showImages = True

blurImage = True

# ------------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='test_morph.log', filemode='w')



# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

# Get the list of image names to read
theList = FileList(args.dataset,  args.list)
imagePaths = theList.getPathFilenames()


logging.info("imagePaths is %s", imagePaths)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")


    # load the image, describe the image, update the list of data
    image = cv2.imread(imagePath)

    # resize the image
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    resized = resize(image, width=500)

    if (blurImage) :
        #resized = cv2.GaussianBlur(resized, (5,5), 0)
        filtered = cv2.bilateralFilter(resized, 9, 75, 75)  # preserves the edges better
    else :
        filtered = resized.copy()

    #kernel = np.ones((5, 5), np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(filtered, kernel, iterations=1)
    dilation = cv2.dilate(filtered, kernel, iterations=1)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel)
    gradient = cv2.morphologyEx(filtered, cv2.MORPH_GRADIENT, kernel)
    tophat = cv2.morphologyEx(filtered, cv2.MORPH_TOPHAT, kernel)
    blackhat = cv2.morphologyEx(filtered, cv2.MORPH_BLACKHAT, kernel)

    # Show images if desires
    if (showImages) :

        cv2.imshow(imagePath, resized)

        cv2.imshow("Smoothed", filtered)

        # show the morphed image
        cv2.imshow("Eroded", erosion)

        cv2.imshow("Dilated", dilation)

        cv2.imshow("opening", opening)

        cv2.imshow("closing", closing)

        cv2.imshow("gradient", gradient)

        cv2.imshow("tophat", tophat)

        cv2.imshow("blackhat", blackhat)

        cv2.waitKey(0)

        cv2.destroyAllWindows()

