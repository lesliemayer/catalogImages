# USAGE
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora_nightlimb.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\limbnight.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\iss.txt"
# python find_color_hsv.py E:\Lightning\ --log=debug --list="E:\Lightning\lightning.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\no_lightning.txt"
# python find_color_hsv.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt"

# import the necessary packages
import argparse
import os # to check list file existence
import sys
import logging #  To write messages to a logfile

import cv2
import numpy as np
from imutils import paths
from imutils import resize
#from imageutils import plot_color_hist

# -----------------------
# For checking the path
# -----------------------
#print '\n'.join(sys.path)
#sys.exit(0)

findAurora = False
findLightning = True

doOpening = True

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

# -----------------------------------------------
# Display the images while looping through them?
# -----------------------------------------------
showImages = True
showContours = False
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
logging.basicConfig(level=numeric_level, filename='find_color_hsv.log', filemode='w')



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
if findAurora :
    # 60 may be to low for value
    #colorLower = np.array([53, 30, 60], dtype = "uint8")
    #colorUpper = np.array([65, 255, 255], dtype = "uint8")

    # I think saturation needs to be increased to get rid of airglow
    #colorLower = np.array([53, 110, 30], dtype = "uint8") # still gets some airglow
    #colorLower = np.array([53, 130, 30],  dtype = "uint8") # still gets a little airglow

    colorLower = np.array([53, 150, 30],  dtype = "uint8") # if this gets > .1%, def is aurora
    colorUpper = np.array([65, 255, 255], dtype = "uint8")

    # may be aurora or airglow, check # of pixels, and sun elev?
    colorLower = np.array([53, 110, 30],  dtype = "uint8") # if this gets > .1%, def is aurora
    colorUpper = np.array([65, 255, 255], dtype = "uint8")

    # Make %green pixel cut off at .1%????
    # problem images :
    # F:\imagews\training\ :
    # ISS_ISS026-E-28071.jpg
    # Limbnight_ISS037-E-8497.jpg  (only .058% though)
    # Night_ISS028-E-26587.jpg (.01 %)
    # ISS_ISS026-E-28063.jpg (.127%)
    # ISS_ISS026-E-28064.jpg (.13%)
    # ISS_ISS026-E-28066.jpg (.1%)
    # ISS_ISS026-E-28068.jpg (.05%)
    # ISS_ISS026-E-28069.jpg (.04%)
    # ISS_ISS026-E-28071.jpg (.04 %)

    # Aurora_ISS009-E-28575.jpg ***** is aurora but isn't getting it :-(
    # Aurora_ISS009-E-28576.jpg ***** is aurora but isn't getting it :-(
    # Aurora_ISS037-E-6342.jpg  **** not getting the real bright green aurora
    # Aurora_ISS037-E-6345.jpg **** not getting the real bright green aurora
    # Aurora_ISS037-E-7528.jpg **** not getting the real bright green aurora

elif findLightning :
    # Doesn't find any lightning
    colorLower = np.array([107, 200, 200],  dtype = "uint8")  # 256 = 0
    colorUpper = np.array([119, 255, 255], dtype = "uint8")

    #
    colorLower = np.array([100, 0, 50],  dtype = "uint8")
    colorUpper = np.array([160, 255, 255], dtype = "uint8")

    # may be aurora or airglow, check # of pixels, and sun elev?
    #colorLower = np.array([53, 110, 30],  dtype = "uint8") # if this gets > .1%, def is aurora
    #colorUpper = np.array([65, 255, 255], dtype = "uint8")

else :
    # throw an exception
    sys.exit("findAurora or findLightning has to be true")

logging.info("colorLower = %s",colorLower)   # **** check pixel values
logging.info("colorLower = %s",colorUpper)

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


    # load the image, describe the image, update the list of data
    image = cv2.imread(imagePath)

    # resize the image
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    resized = resize(image, width=500)

    if (blurImage) :
        #resized = cv2.GaussianBlur(resized, (5,5), 0)
        filtered = cv2.bilateralFilter(resized, 9, 75, 75)
    else:
        filtered = resized.copy()

    if (doOpening) :
        kernel = np.ones((3, 3), np.uint8)
        opened = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    else:
        opened =  filtered.copy()


    # Convert the image color space to HSV
    #hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    #hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(opened, cv2.COLOR_BGR2HSV)



    # ---------------------------------------------------------------
    # Determine which pixels fall within the green boundaries
    # and then blur the binary image
    # inRange takes the image, lower threshold, upper threshold color,
    # and the result is a thresholded image, with pixels in range => white,
    # pixels out of range => black
    # ----------------------------------------------------------------
    green = cv2.inRange(hsv, colorLower, colorUpper)

    # -----------------------------------
    # Get % of pixels that are in range
    # -----------------------------------
    # get # of white pixels, divide by total pixels (total = h X w)
    totalPix = green.shape[0] * green.shape[1]
    logging.debug("total Pixels in resized image : %s * %s = %s", green.shape[1],green.shape[0],totalPix)

    # Get number of non-zero pixels :
    nonZero = np.count_nonzero(green)
    logging.debug("Number of non-zero pixels in binary array : %s", nonZero)

    percentGreen = (float(nonZero)/float(totalPix)) * 100.
    logging.info("%s %s",imagePath, percentGreen)

    #sys.exit(0)

    # ALREADY DOING THIS ABOVE !!!!!!!!!***********
    # smooth the image to make finding contours more accurate
    #green = cv2.GaussianBlur(green, (3, 3), 0)

    # find contours in the thresholded image
    # cv2.findContour function is destructive to the NumPy array that is passed in.
    (_, cnts, _) = cv2.findContours(green.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)

    # check to see if any contours were found
    if len(cnts) > 0  and showContours :
	    # sort the contours and find the largest one -- we
	    # will assume this contour corresponds to the area
	    # of my phone.
	    # Larger contours in front of list, grab the one w/ largest area,
	    # assuming this is the outline of the phone.
	    cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

	    # compute the (rotated) bounding box around then
	    # contour and then draw it
	    # minAreaRect gets min. bounding box around contour
	    # cv2.boxPoints re-shapes the bounding box to be a list of points,
	    # so in can be drawn w/ drawContours
	    rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
	    # draw the boundaries of the box
	    cv2.drawContours(resized, [rect], -1, (0, 255, 0), 2)

        # Get the number of pixels in the binary image that are true

    # Show images if desires
    if (showImages) :

        # Add text w/ % of green pixels to the image

        # draw text string of the digit on the image a x-10,y-10
        # (above & to left of bounding box)
        # putText(img, text, textOrg, fontFace, fontScale,
        #        Scalar::all(255), thickness, 8);
        cv2.putText(resized, str(percentGreen)+'%', (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # show the frame and the binary image
        cv2.imshow(imagePath, resized)

        # show the smoothed, thresholded image
        cv2.imshow("Binary", green)

        cv2.waitKey(0)
        # plot this histogram
        #plot_color_hist(image)

        cv2.destroyAllWindows()



# destroy pointer & all windows
cv2.destroyAllWindows()