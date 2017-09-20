# USAGE
# python find_aurora.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# python find_aurora.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python find_aurora.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora_nightlimb.txt"
# python find_aurora.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python find_aurora.py F:\imagews\training --log=debug --list="F:\imagews\training\limbnight.txt"

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

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Find green aurora in images")
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
logging.basicConfig(level=numeric_level, filename='find_aurora.log', filemode='w')

# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

# ---------------------------------------------------------------------
# Define the upper and lower boundaries for a color
# to be considered "blue"
# This defines
# the lower and upper limits of the shades of blue in the RGB
# color space on Lines 11 and 12. Remember, OpenCV represents
# pixels in the RGB color space, but in reverse order.
# In this case, Laura defines colors as "blue" if they are
# greater than R = 0, G = 67, B = 100 and less than R =
# 50, G = 128, B = 255.  This is for tracking the blue phone case.
# ----------------------------------------------------------------------
#blueLower = np.array([100, 67, 0], dtype = "uint8")
#blueUpper = np.array([255, 128, 50], dtype = "uint8")

# This picks out anything that is bright:
#greenLower = np.array([0, 50, 0], dtype = "uint8")
#greenUpper = np.array([255, 255, 255], dtype = "uint8")

# -------------------------------------------------------
# Throws out the bright green too much
# but works pretty good.  Finds some green inside ISS
# finds some blue/green water
# --------------------------------------------------------
#greenLower = np.array([0, 50, 0], dtype = "uint8")
#greenUpper = np.array([50, 255, 50], dtype = "uint8")

# I think 40 is too low : run color_trackbar.py to see what color this is
# or red & blue are too high
greenLower = np.array([0, 40, 0], dtype = "uint8")
greenUpper = np.array([60, 200, 60], dtype = "uint8")

# THIS ONE WORKS PRETTY GOOD FOR JUST GETTING AURORA W/OUT EARTHLIMB OR ISS ****
# THIS DOESN'T GRAB THE BRIGHT GREEN IN THE AURORA, BUT MAYBE THAT IS OK
# ********** IS NOT GETTING ANY OF F:\imagews\training\Aurora_ISS037-E-6351.jpg *****
# THIS FIND ANY OF THE GREEN IN LIMBNIGHT IMAGES *** GOOD
# FINDS A LITTLE BIT IF GREEN IN CITIES AT NIGHT, BUT VERY SMALL (MINISCULE)
# *** check F:\imagews\training/Night_ISS026-E-25223.jpg, Night_ISS026-E-25224.jpg
#  - upper left corner has a weird green in it  (check focal length & latitude???? **
# also look at F:\imagews\training/Night_ISS028-E-23149.jpg, Night_ISS028-E-23150.jpg
# look at F:\imagews\training/Night_ISS028-E-23175.jpg - green refraction from lens?
# F:\imagews\training/Night_ISS028-E-23211.jpg, Night_ISS028-E-24318.jpg, Night_ISS028-E-24395.jpg
# F:\imagews\training/Night_ISS028-E-24397.jpg, Night_ISS028-E-24398.jpg and 4 or 5 after that
# what is on F:\imagews\training/Night_ISS028-E-25244.jpg - there is something that kind of
# looks like aurora but is not detected
# F:\imagews\training/Night_ISS028-E-25383.jpg, Night_ISS028-E-25388.jpg
# F:\imagews\training/Night_ISS028-E-26148.jpg  - blue green in lake/cloud showing up as aurora
# F:\imagews\training/Night_ISS028-E-26555.jpg to 26559 - gets part of the earthlimb airglow
# F:\imagews\training/Night_ISS028-E-26583.jpg - gets part of the earthlimb airglow (or is it getting
# the night lights that are brown?  - could draw contour lines around it


greenLower = np.array([0, 45, 0], dtype = "uint8")
greenUpper = np.array([60, 200, 20], dtype = "uint8")

# try getting the bright green aurora
#greenLower = np.array([0, 45, 0], dtype = "uint8")
#greenUpper = np.array([60, 200, 20], dtype = "uint8")



logging.info("greenLower = %s",greenLower)
logging.info("greenLower = %s",greenUpper)

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


    # load the image, describe the image, update the list of data
    image = cv2.imread(imagePath)

    # resize the image
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    resized = resize(image, width=500)

    if (blurImage) :
        resized = cv2.GaussianBlur(resized, (5,5), 0)



    # ---------------------------------------------------------------
    # Determine which pixels fall within the green boundaries
    # and then blur the binary image
    # inRange takes the image, lower threshold, upper threshold color,
    # and the result is a thresholded image, with pixels in range => white,
    # pixels out of range => black
    # ----------------------------------------------------------------
    green = cv2.inRange(resized, greenLower, greenUpper)

    # -----------------------------------
    # Get % of pixels that are in range
    # -----------------------------------
    # get # of white pixels, divide by total pixels (total = h X w)
    totalPix = green.shape[0] * green.shape[1]
    #logging.debug("total Pixels in resized image : %s %s %s", green.shape[1],green.shape[0],totalPix)

    # Get number of non-zero pixels :
    nonZero = np.count_nonzero(green)
    logging.debug("Number of non-zero pixels in binary array : %s", nonZero)

    percentGreen = (float(nonZero)/float(totalPix)) * 100.
    logging.info("%s %s",imagePath, percentGreen)

    #sys.exit(0)

    # smooth the image to make finding contours more accurate
    green = cv2.GaussianBlur(green, (3, 3), 0)

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