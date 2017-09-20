# Standard imports
import sys
import os
import cv2
import numpy as np
import argparse
import logging
from imutils import resize
from filelist import FileList  # import the filelist class
from filelist import get_filename
from issimage import ISSIMAGE

# usage :
# python blob_detect_V2.py F:\imagews\training --log=debug --list="F:\imagews\training\small_lightning_test.txt"
# python blob_detect_V2.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\BetterLightning\Blobs"
# python blob_detect_V2.py F:\imagews\training\ --log=debug --list="F:\imagews\training\no_lightning.txt"
# python blob_detect_V2.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt"
# python blob_detect_V2.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"
# python blob_detect_V2.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt" --out="E:\BetterLightning\Blobs"

# ------------------------------------------
# Do we want to save the images to a file?
# ------------------------------------------
writeImage = True

# -----------------------------------------------
# Display the images while looping through them?
# -----------------------------------------------
showImages = True

# ----------------------------------------------------
# Get rid of stars by eroding the dilating (opening)
# ----------------------------------------------------
doOpening = True

# ------------------
# Smooth the image?
# ------------------
doSmoothing = True

# -----------------------
# convert to HSV color?
# -----------------------
doHSV = True


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

# The logging filename (goes in current directory unless args.out exists)
name = 'blob_detect_V2.log'
if (args.out) :
    name = args.out + '/' + name
print "log filename = {}".format(name)

# set up the logging file :
# **** if there is problem w/ logging file will quietly go on unless you catch it ********
try:
    logging.basicConfig(level=numeric_level, filename=name, filemode='w')
except Exception, e:
    print 'Error setting up log file {}'.format(name)
    sys.exit(1)

# -----------------------------------------------------------
# Write out the kernel size for the opening to the log file
# -----------------------------------------------------------
if doOpening :
    # openKernelSize = 3
    # openKernelSize = 11 # smeared out too much, but shows as purple
    openKernelSize = 5  # gets rid of stars much better than 3,3
    logging.info("Opening of %s, %s", openKernelSize, openKernelSize)

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

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for filename in imagePaths:

    #if args.list :
    if not os.path.isfile(filename) :
            sys.exit("filename " + filename + "  does not exist")

    # Read image
    #im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    #im = cv2.imread(filename)
    issimg = ISSIMAGE(filename)

    # -------------------
    # Resize the image
    # -------------------
    #resized = resize(im, width=500)
    issimg.resize(800)


    # Smooth the image
    if (doSmoothing):
        #filtered = cv2.bilateralFilter(resized, 9, 75, 75)
        filtered = cv2.bilateralFilter(issimg.image, 9, 75, 75)

    else:
        filtered = resized.copy()


    if (doOpening):
        kernel = np.ones((openKernelSize, openKernelSize), np.uint8)
        opened = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)

        # do a couple more times
        opened2 = cv2.morphologyEx(opened, cv2.MORPH_OPEN, kernel)
        opened3 = cv2.morphologyEx(opened2, cv2.MORPH_OPEN, kernel)
        opened4 = cv2.morphologyEx(opened3, cv2.MORPH_OPEN, kernel)

        opened = opened4.copy()  # to make sure I'm using the right one


    else:
        opened = filtered.copy()


    # Need to mask out by color, then get blobs
    # Convert to HSV color
    if (doHSV) :
        hsv = cv2.cvtColor(opened, cv2.COLOR_BGR2HSV)
    else :
        hsv = opened.copy()

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    #params.minThreshold = 10 too small
    params.minThreshold = 100
    params.maxThreshold = 200

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 10  # too big?
    params.minArea = 5  # still to big?
    params.minArea = 3
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


    # Set up the detector with parameters.
    detector = cv2.SimpleBlobDetector_create(params)

    # blur the image ***** MAYBE SHOULDN'T BLUR TOO MUCH - WILL MAKE A BLOB WHERE THERE'S NOT ONE
    # blurred = cv2.GaussianBlur(resized, (11, 11), 0)
    # bilateral smoothing (keep the edges)
    #blurred = cv2.bilateralFilter(hsv, 9, 75, 75)  # don't do this 2x

    # Detect blobs.
    keypoints = detector.detect(opened)

    # print out the keypoints positions
    # for key in keypoints :
    #     # x = keypoints[i].pt[0]  # i is the index of the blob you want to get the position
    #     # y = keypoints[i].pt[1]
    #     logging("keypoint : %s %s", key.pt[0], key.pt[1])

    #logging("keypoint : %s", keypoints[0].pt[0])
    # x = keypoints[0].pt[0]
    # logging.debug("keypoint : %s", x)
    # logging.debug("keypoint : %s", keypoints[0].size())

    for keyPoint in keypoints:
        y = keyPoint.pt[1]
        x = keyPoint.pt[0]
        s = keyPoint.size
        logging.debug("keypoint : %s %s %s", x, y, s)

        # Get color or nearest pixel to x,y
        ix = int(x)
        iy = int(y)

        # get the blue, green, red components of pixel[0,0]
        (h, s, v) = hsv[iy, ix]
        #logging.debug("hsv size is : x: %s y: %s", hsv.shape[1], hsv.shape[0])
        logging.debug("pixel value h, s, v : %s %s %s", h, s, v)

    logging.debug("----------------------------------------------")

    # Get list of keypoint functions
    #print (dir(keypoints))

    # Put name of file, focal length, sun elevation text on the image
    # Put this on before drawing keypoints onto the image
    issimg.put_text()

    # --------------------------------------------------------------------------------
    # Draw detected blobs as green circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle
    # corresponds to the size of blob
    # ---------------------------------------------------------------------------------
    #im_with_keypoints = cv2.drawKeypoints(opened, keypoints, np.array([]), (0, 255, 0),
    im_with_keypoints = cv2.drawKeypoints(issimg.image, keypoints, np.array([]), (0, 255, 0),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # draw contours around keypoints
    #cv2.drawContours(im, keypoints, -1, (0, 255, 0), 3)

    # set size of display window
    # cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Keypoints", 500, 300)

    # Show keypoints
    # cv2.imshow("Keypoints", im_with_keypoints)
    # cv2.waitKey(0)


    # Show images if desired
    if (showImages):

        # show the frame and the binary image
        # USE THE ISSIMAGE TO SHOW THE ORIGINAL IMAGE *******
        # cv2.imshow(imagePath, resized)
        # show the image
        #cv2.imshow("the resized image", issimg.image)
        #issimg.show()
        cv2.imshow("original image w/ keypoints", im_with_keypoints)

        if (doSmoothing):
            cv2.imshow("filtered", filtered)

        if doOpening:
            cv2.imshow("opening", opened)

        # show the smoothed, thresholded image
        #cv2.imshow("Binary", block.binary)

        cv2.waitKey(0)

        # plot this histogram
        # plot_color_hist(image)

        cv2.destroyAllWindows()

    if (writeImage and args.out):

        outname = args.out + '/' + get_filename(filename) + '_blob.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, im_with_keypoints)

        outname = args.out + '/' + get_filename(filename) + '_filter.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, filtered)


        if doOpening:
            outname = args.out + '/' + get_filename(filename) + '_open.jpg'
            cv2.imwrite(outname, opened)


