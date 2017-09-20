# USAGE
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# out specifies where output images will be saved
# python find_color_hsv.py F:\imagews\training --log=info --list="F:\imagews\training\aurora.txt" --out="F:\imagews\training\Aurora_Color_Block"
# python find_color_hsv.py F:\imagews\training --log=info --list="F:\imagews\training\various.txt" --out="F:\imagews\training\Various_Color_Block"
# python find_color_hsv.py F:\imagews\training --log=info --list="F:\imagews\training\aurora_nightlimb.txt" --out="F:\imagews\training\Airglow_Color_Block"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\limbnight.txt"
# python find_color_hsv.py F:\imagews\training --log=debug --list="F:\imagews\training\iss.txt"

# Lightning images to test :
# python find_color_hsv.py E:\Lightning\ --log=info --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Color_Block"
# python find_color_hsv.py F:\imagews\training --log=info --list="F:\imagews\training\no_lightning.txt" --out="F:\imagews\training\Lightning_Color_Block"
# python find_color_hsv.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt" --out="E:\BetterLightning\Color_Block"

# import the necessary packages
import argparse
import os # to check list file existence
import sys
import logging #  To write messages to a logfile

import cv2
import numpy as np
from imutils import paths
from imutils import resize
from filelist import FileList  # import the filelist class for getting the files to read
from filelist import get_filename
from hsvcolorblock import HSVCOLORBLOCK
from issimage import ISSIMAGE
#from imageutils import plot_color_hist (if want to look at color bins)

# ------------------------------------------
# Do we want to save the images to a file?
# ------------------------------------------
writeImage = True

# -----------------------------------------------
# Display the images while looping through them?
# -----------------------------------------------
showImages = True
showContours = True

# Remove noise?
blurImage = True

# ----------------------------------
# Find the aurora or the lightning
# ----------------------------------
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
name = 'find_color_hsv.log'
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


# Write out the kernel size to the log file
if doOpening :
    openKernelSize = 5  # gets rid of stars much better than 3,3
    logging.info("Opening of %s, %s", openKernelSize, openKernelSize)


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
    #colorLower = np.array([53, 110, 30],  dtype = "uint8") # if this gets > .1%, def is aurora
    #colorUpper = np.array([65, 255, 255], dtype = "uint8")

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
    #colorLower = np.array([107, 200, 200],  dtype = "uint8")  # 256 = 0
    #colorUpper = np.array([119, 255, 255], dtype = "uint8")

    # Best so far
    colorLower = np.array([100, 0, 50],  dtype = "uint8")
    colorUpper = np.array([160, 255, 255], dtype = "uint8")

    #Blue -> Purple
    colorLower = np.array([90, 127, 25],  dtype = "uint8")
    colorUpper = np.array([155, 255, 255], dtype = "uint8")

    # white
    colorLower = np.array([0, 0, 165],  dtype = "uint8")
    colorUpper = np.array([179, 38, 255], dtype = "uint8")

    # new test : 01/18/2017  (picked colors by hovering over pixels)  BETTER !!! FOR THE ISS045-E-1603.jpg pics
    # 90 maybe gives too much?   make want to get rid of the green
    colorLower = np.array([90, 30, 100], dtype="uint8")
    colorUpper = np.array([155, 100, 255], dtype="uint8")

    # new test : 01/19/2017
    colorLower = np.array([100, 30, 100], dtype="uint8")
    colorUpper = np.array([155, 150, 255], dtype="uint8")


else :
    # throw an exception
    sys.exit("findAurora or findLightning has to be true")

logging.info("colorLower = %s",colorLower)   # **** check pixel values
logging.info("colorUpper = %s",colorUpper)

# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.dataset,  args.list)
imagePaths = theList.getPathFilenames()


logging.info("find_aurora_hsv : imagePaths is %s", imagePaths)


# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")


    # load the image, describe the image, update the list of data
    #image = cv2.imread(imagePath)
    issimg = ISSIMAGE(imagePath)

    # resize the image
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    issimg.resize(800)

    if (blurImage) :
        #resized = cv2.GaussianBlur(resized, (5,5), 0)
        #filtered = cv2.bilateralFilter(resized, 9, 75, 75)  # preserves edges better
        filtered = cv2.bilateralFilter(issimg.image, 9, 75, 75)  # preserves edges better
    else:
        filtered = resized.copy()

    if (doOpening) :
        # n = 3
        # n = 5
        kernel = np.ones((openKernelSize, openKernelSize), np.uint8)
        opened = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    else:
        opened =  filtered.copy()


    # Get the color blocked binary image
    block = HSVCOLORBLOCK(opened, colorLower, colorUpper)



    # Get % of pixels that are this color
    percentColor = block.get_percent()
    if showContours and (percentColor > 0) :

        # Get the largest contour around the color block
        cnt = block.get_largest_contour()
        # compute the (rotated) bounding box around then
        # contour and then draw it
        # minAreaRect gets min. bounding box around contour
        # cv2.boxPoints re-shapes the bounding box to be a list of points,
        # so in can be drawn w/ drawContours
        if cnt.any() :
	        rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))

	        # draw the boundaries of the box
	        cv2.drawContours(issimg.image, [rect], -1, (0, 255, 0), 2)


    # Add text w/ % of green pixels to the image
    # draw text string of the digit on the image a x-10,y-10
    # (above & to left of bounding box)
    # putText(img, text, textOrg, fontFace, fontScale,
    #        Scalar::all(255), thickness, 8);
    #cv2.putText(resized, str(percentColor)+'%', (20, 20),
    cv2.putText(issimg.image, str(percentColor)+'%', (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Put name of file, focal length, sun elevation text on the image
    issimg.put_text()

    # Show images if desired
    if (showImages) :

        # show the frame and the binary image
        # USE THE ISSIMAGE TO SHOW THE ORIGINAL IMAGE *******
        #cv2.imshow(imagePath, resized)
        issimg.show()

        cv2.imshow("filtered",filtered)

        if doOpening:
            cv2.imshow("opening",opened)

        # show the smoothed, thresholded image
        cv2.imshow("Binary", block.binary)

        cv2.waitKey(0)

        # plot this histogram
        #plot_color_hist(image)

        cv2.destroyAllWindows()

    if (writeImage and args.out) :

        outname = args.out + '/' + get_filename(imagePath) + '_block.jpg'

        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, issimg.image)

        if doOpening:
            outname = args.out + '/' + get_filename(imagePath) + '_open.jpg'
            cv2.imwrite(outname,opened)

        outname = args.out + '/' + get_filename(imagePath) + '_binary.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, block.binary)



# destroy pointer & all windows
cv2.destroyAllWindows()