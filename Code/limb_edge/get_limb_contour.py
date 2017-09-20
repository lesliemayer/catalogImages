import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from imutils import resize
from filelist import FileList  # import the filelist class
import logging
import argparse
import sys

# # for getting focal length from the photos database
from issimage import ISSIMAGE


# python get_limb_contour.py E:\BetterLightning --log=debug --list="E:\BetterLightning\limb_edge.txt"
# python get_limb_contour.py E:\BetterLightning --log=debug --list="E:\BetterLightning\make_limb_edge.txt"
# python get_limb_contour.py E:\Lightning --log=debug --list="E:\Lightning\limb_edge.txt"


# -------------------------------------------
# Thresholding for finding where the limb is
# -------------------------------------------
doThreshold = False
threshold = 50

# -------------------------------------------------
# Get rid of small bright features (stars,  noise)
# -------------------------------------------------
doOpening = True

# -------------------------------------------------
# Get rid of small bright features (stars,  noise)
# -------------------------------------------------
doClosing = True

# Set color green
green = (0,255,0)


# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Save earth limb as edge")
ap.add_argument("dataset", help="Path to images")  # this is required

# Add logging file argument
ap.add_argument("-l", "--log", help="Logging Value", default="info")

# Add list file argument
ap.add_argument("-li", "--list", help="List of images to read")

# parse the arguments
args = ap.parse_args()

# -------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
# -------------------------------------------------------------
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='get_limb_contour.log', filemode='w')


logging.info("dataset, list = %s  %s",args.dataset, args.list)


# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.dataset,  args.list)
imagePaths = theList.getPathFilenames()

logging.info("imagePaths is %s", imagePaths)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for filename in imagePaths:

    if args.list :
        if not os.path.isfile(filename) :
               sys.exit("filename " + filename + "  does not exist")

        # Read image
        img = cv2.imread(filename)

        # resize the image
        # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
        resized = resize(img, width=500)
        #resized = resize(img, width=800)

        # initialize ISSIMAGE class for setting up the image
        xx = ISSIMAGE(filename)

        xx.resize()

        xx.show()

        # ----------------------
        # Get the sun elevation
        # ----------------------
        sunElev = xx.get_sun_elev()
        logging.debug("Sun elevation = %s", sunElev)

        # ----------------------
        # Get the focal length
        # ----------------------
        focalLength = xx.get_focal_length()
        logging.debug("Focal length = %s", focalLength)


        # -----------------
        # convert to gray
        # -----------------
        gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)

        # Do histogram equalization ??? (only needed for night time limb)
        # equalize the histogram of the image
        eq = cv2.equalizeHist(gray)
        cv2.imshow("histogram of open/close", eq)

        # ------------------------------------------------------
        # Smooth the image
        # nn = the neighborhood size
        # For finding the limb, want the image to be very smooth
        # -------------------------------------------------------
        nn = 11  # Get less edges w/ higher n
        #nn = 5
        #gray = cv2.GaussianBlur(gray, (nn, nn), 0)

        # -----------------------------------------------
        # Bilateral filtering preserves the edges
        # 2nd parameter is the window size for smoothing
        # -----------------------------------------------
        #filtered = cv2.bilateralFilter(gray,9,75,75)
        filtered = cv2.bilateralFilter(gray,19,75,75)

        cv2.imshow("bilateral filter", filtered)



        # ==================================================================
        # Do an opening to get rid of more noise (the small bright areas)
        # ==================================================================
        if (doOpening):
            #kernel = np.ones((3, 3), np.uint8)
            kernel = np.ones((9, 9), np.uint8)
            #kernel = np.ones((19, 19), np.uint8)  # to big for night images
            opened = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
        else:
            opened = filtered.copy()

        # ---------------------------------------
        # Do closing to get of small dark spots
        # ---------------------------------------
        if (doClosing):
            #kernel = np.ones((3, 3), np.uint8)
            #kernel = np.ones((9, 9), np.uint8)
            #kernel = np.ones((19, 19), np.uint8)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        else:
            closed = opened.copy()

        cv2.imshow("opened/closed", closed)


        # ---------------------------------------------------------------------------------------------
        # Show the gradient image (for testing whether this is a viable method for getting night limb)
        # ---------------------------------------------------------------------------------------------
        kernel = np.ones((3, 3), np.uint8)
        gradient = cv2.morphologyEx(closed, cv2.MORPH_GRADIENT, kernel)
        cv2.imshow("gradient of opened/closed", gradient)


        # ---------------------
        # Threshold the image
        # ---------------------
        if (doThreshold) :

            if (sunElev > 10) :
                # image needs to be 1D for threshold function
                # Simple, binary thresholding
                #ret, thresh = cv2.threshold(opened, 100, 255, cv2.THRESH_BINARY)  # not bad, but may be too high
                # pretty good, but not good w/ very bright limb images : Earthlimb_ISS009-E-16194.jpg - Earthlimb_ISS009-E-16199.jpg
                # May need to figure out peaks of bimodal color histogram on the gray image or something like that

                logging.debug("threshold = %s", threshold)
                ret, thresh = cv2.threshold(closed, threshold, 255, cv2.THRESH_BINARY)

            elif (sunElev < -30. and sunElev > -70.) :

                #threshold = 75  # to get the bright limb  # too low
                #threshold = 100  # to get the bright limb # too high
                #threshold = 90  # too high
                #threshold = 85 # too high
                threshold = 80
                #logging.debug("threshold = %s", threshold)
                # this global thresholding not really working b/c of variable lighting
                #ret, thresh = cv2.threshold(closed, threshold, 255, cv2.THRESH_BINARY)

                # adaptive gaussian thresholding
                logging.debug("Adaptive Gaussian threshold")
                nn = 11  # not good - too many, lots of them dots
                nn = 5  # better, but only gets the really big contrasts
                nn = 3  # same as above
                #nn = 9  # not sure why there is a bunch of dot contours above limb
                #thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nn, 2)
                thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nn, 10)
                #  This only gets the egdes that are very big in contrast (very dark next to very light)
                #thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nn, -10)
                #ret, thresh = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)\

            else:

                logging.debug("binary + otsu threshold")
                ret, thresh = cv2.threshold(closed,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        else:
            thresh = opened.copy()   # gives too many contours

        # ---------------------------------------------------------------
        # compute edges on the smoothed image
        # any gradient values below 30 are considered
        # non-edges whereas any values above 150 are considered
        # sure edges.
        # ----------------------------------------------------------------
        edgeThresh1 = 30
        edgeThresh2 = 50  # use for thresholded day limb


        # too many contours when sun elev is high (by night standards)
        # no contours in very low sun elev : -76
        edgeThresh1 = 50
        edgeThresh2 = 100  # alot of contours, but maybe its ok, as long as it gets the limb

        edged = cv2.Canny(thresh, edgeThresh1, edgeThresh2)  # use for day limb

        # run the canny edge detection on smoothed image
        #                image, threshold1, threshold2
        # Any gradient value larger than threshold2 is considered
        # to be an edge. Any value below threshold1 is considered
        # not to be an edge. Values in between threshold1
        # and threshold2 are either classified as edges or non-edges
        # based on how their intensities are 'connected'

        # Get the contour & draw it :
        contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        print ("img1 : Length of contours = {}".format(len(contours)))
        #cnt1 = contours[0]

        # draw contours found
        #cv2.drawContours(resized, [cnt1], 0, green, 2)
        cv2.drawContours(resized, contours, -1, green, 2)
        cv2.imshow("1st contour", resized)


        cv2.imshow("Edges", edged)
        cv2.waitKey(0)

        # Save the edge
        cv2.imwrite("limb_edge.jpg", edged)

        # Save image w/ contour drawn
        cv2.imwrite("contour_edge.jpg",resized)


