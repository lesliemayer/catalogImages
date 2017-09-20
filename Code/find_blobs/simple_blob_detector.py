# Standard imports
import sys
import os
import cv2
import numpy as np
import argparse
import logging
from imutils import resize

#filename = "E:\Lightning\ISS043-E-10712.jpg"
# filename = r"E:\Lightning\ISS006-E-21385.jpg"
# filename = r"E:\Lightning\SmallISS043-E-3093.jpg"
# filename = r"E:\Lightning\SmallISS031-E-10712.jpg"
# filename = r"E:\Lightning\SmallISS031-E-10713.jpg"
#filename = r"C:\Users\lrmayer\Documents\Mayer\CatalogImages\Code\find_blobs\BlobTest.jpg"

# usage :
# python simple_blob_detector.py F:\imagews\training --log=debug --list="F:\imagews\training\small_lightning_test.txt"
# python simple_blob_detector.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt"
# python simple_blob_detector.py F:\imagews\training\ --log=debug --list="F:\imagews\training\no_lightning.txt"

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Find blobs in images")
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
logging.basicConfig(level=numeric_level, filename='simple_blob_detector.log', filemode='w')

# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

# Get rid of stars by eroding the dilating (opening)
doOpening = True

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
for filename in imagePaths:

    if args.list :
        if not os.path.isfile(filename) :
               sys.exit("filename " + filename + "  does not exist")

        # Read image
        #im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        im = cv2.imread(filename)

        # resize the image
        # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
        resized = resize(im, width=500)

        # show the  image
        cv2.imshow("the image", resized)

        if (doOpening):
            kernel = np.ones((3, 3), np.uint8)
            opened = cv2.morphologyEx(resized, cv2.MORPH_OPEN, kernel)
        else:
            opened = resized

        cv2.imshow("morphed",opened)

        # Need to mask out by color, then get blobs

        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        #params.minThreshold = 10 too small
        params.minThreshold = 100
        params.maxThreshold = 200

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 10  # too big?
        params.minArea = 5
        params.maxArea = 1000

        # Filter by Circularity
        # params.filterByCircularity = True
        # params.minCircularity = 0.1

        # Filter by Convexity  : this is need for lightning shape
        params.filterByConvexity = True
        params.minConvexity = 0.5

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        # Filter by color?
        params.filterByColor = True

        # By default the detector looks for dark blobs. You can tell it instead to
        # look for light blobs by setting params.blobColor = 255
        params.blobColor = 255

        #Later I'd like to detect areas of a set colour, which I think means I need to pre-process
        # the image to find the areas of the colour I want. Using cv2.inRange() to do this will
        # give a monochrome image (each pixel either black or white), so there's no point in the blob
        # detector running at several threshold values (by default I think it creates 16 different
        # thresholded images for analysis). So I guess I can do something like params.minThreshold=128;
        # params.maxThreshold=128 to tell it to only do one thresholding run.

        # ONLY NEED THIS IF WILL BE RUNNING ON OTHER SYSTEMS
        # # Create a detector with the parameters
        # ver = (cv2.__version__).split('.')
        # if int(ver[0]) < 3 :
        #     detector = cv2.SimpleBlobDetector(params)
        # else :
        #     detector = cv2.SimpleBlobDetector_create(params)


        # Set up the detector with default parameters.
        #detector = cv2.SimpleBlobDetector()  # this doesn't work
        detector = cv2.SimpleBlobDetector_create(params)
        #detector = cv2.SimpleBlobDetector_create()

        # blur the image ***** MAYBE SHOULDN'T BLUR TOO MUCH - WILL MAKE A BLOB WHERE THERE'S NOT ONE
        # blurred = cv2.GaussianBlur(resized, (11, 11), 0)
        # bilateral smoothing (keep the edges)
        blurred = cv2.bilateralFilter(resized, 9, 75, 75)

        # Detect blobs.
        keypoints = detector.detect(blurred)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(blurred, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # draw contours around keypoints
        #cv2.drawContours(im, keypoints, -1, (0, 255, 0), 3)

        # set size of display window
        # cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Keypoints", 500, 300)

        # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(0)