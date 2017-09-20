"""Python code to read in an image and determine if there is
lightning in the image by using simple blob detection and color blocking.
Usage :  python lightning_detection.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt
"""

# usage :
# python lightning_detection.py F:\imagews\training --log=debug --list="F:\imagews\training\small_lightning_test.txt"
# python lightning_detection.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\BetterLightning\Blobs"
# python lightning_detection.py F:\imagews\training\ --log=debug --list="F:\imagews\training\no_lightning.txt"
# python lightning_detection.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt"
# python lightning_detection.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"
# python lightning_detection.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt" --out="E:\BetterLightning\BlobColorTest"
# python lightning_detection.py E:\BetterLightning --log=debug --list="E:\BetterLightning\testlightning.txt" --out="E:\BetterLightning\BlobColorTest"
# python lightning_detection.py E:\BetterLightning --log=debug --list="E:\BetterLightning\testlightning.txt" --out="E:\BetterLightning\minThresh150"

# Standard imports
import sys
import os
import cv2
import numpy as np
import argparse
import logging
from filelist import FileList  # import the filelist class
from filelist import get_filename
from issimage import ISSIMAGE
from blobdetect import BLOBDETECT
from hsvcolorblock import HSVCOLORBLOCK

# ------------------------------------------
# Do we want to save the images to a file?
# ------------------------------------------
writeImage = True

# -----------------------------------------------
# Display the images while looping through them?
# -----------------------------------------------
showImages = False

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

# Draw contours around color blocks?
showContours = False


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
name = 'lightning_detection.log'
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

# blob detector -------------------------------------------------------------

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
# params.minThreshold = 10 too small
#params.minThreshold = 100
params.minThreshold = 50
#params.minThreshold = 150  # leaves out some lightning
#params.maxThreshold = 200
params.maxThreshold = 255  # 01/31/2017  test

# Filter by Area.
params.filterByArea = True
# params.minArea = 10  # too big?
# params.minArea = 5  # still to big?
params.minArea = 3
params.maxArea = 100


# Filter by Circularity (4*Pi*Area/Perimeter*Perimeter)
# A circle has circularity = 1, square = .785
params.filterByCircularity = False
params.minCircularity = 0.1
#params.maxCircularity = 1.1


# Filter by Convexity  : this is needed for lightning shape
# Area of blob/Area of convex hull
params.filterByConvexity = True
params.minConvexity = 0.5
params.maxConvexity = 1.1  #LEAVE THIS COMMENTED OUT, ELSE WILL LEAVE OUT SOME BLOBS ******* (why, I don't know)
                           #  if leave out maxConvexity is a huge number.   Set to > 1 , not 1!


# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01
#params.maxInertiaRatio = 1.1


# Filter by color?
params.filterByColor = True

# By default the detector looks for dark blobs. You can tell it instead to
# look for light blobs by setting params.blobColor = 255
params.blobColor = 255

# initialize blob detector object
blobDetect = BLOBDETECT(params)

"""Define the lower and upper limits of color to find"""
# Best so far
colorLower = np.array([100, 0, 50], dtype="uint8")
colorUpper = np.array([160, 255, 255], dtype="uint8")

# Blue -> Purple
colorLower = np.array([90, 127, 25], dtype="uint8")
colorUpper = np.array([155, 255, 255], dtype="uint8")

# white
colorLower = np.array([0, 0, 165], dtype="uint8")
colorUpper = np.array([179, 38, 255], dtype="uint8")

# new test : 01/18/2017  (picked colors by hovering over pixels)  BETTER !!! FOR THE ISS045-E-1603.jpg pics
# 90 maybe gives too much?   make want to get rid of the green
colorLower = np.array([90, 30, 100], dtype="uint8")
colorUpper = np.array([155, 100, 255], dtype="uint8")

# new test : 01/19/2017
colorLower = np.array([100, 30, 100], dtype="uint8")
colorUpper = np.array([155, 150, 255], dtype="uint8")

logging.info("colorLower = %s", colorLower)
logging.info("colorUpper = %s", colorUpper)

minSunElev = -25.
logging.info("min Sun Elevation allowed : %s", minSunElev)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for filename in imagePaths:

    if not os.path.isfile(filename) :
            sys.exit("filename " + filename + "  does not exist")

    logging.info("Filename = %s",filename)

    # set up the ISSIMAGE object
    issimg = ISSIMAGE(filename)

    """Only look at images with sun elevation > minSunElev"""
    # if sun elev larger, skip to next file
    if issimg.get_sun_elev() > minSunElev :
        continue

    # -------------------
    # Resize the image
    # -------------------
    issimg.resize(800)


    # Smooth the image
    if (doSmoothing):
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
        hsvImage = cv2.cvtColor(opened, cv2.COLOR_BGR2HSV)
    else :
        hsvImage = opened.copy()

    # Dilate the binary image to compare binary pixel values
    focalLength = issimg.get_focal_length()
    if (focalLength <= 30):
        kNum = 7
        params.minArea = 3
        params.maxArea = 60
    elif (focalLength >30 and focalLength <=50):
        kNum = 9
        params.minArea = 5
        params.maxArea = 80
    elif (focalLength > 50 and focalLength <= 70):
        kNum = 11
        params.minArea = 7
        params.maxArea = 100
    elif (focalLength > 70 and focalLength <= 150):
        kNum = 15
        params.minArea = 10
        params.maxArea = 150
    elif (focalLength > 70 and focalLength <= 150):
        kNum = 15
        params.minArea = 15
        params.maxArea = 200
    else :
        kNum = 15
        params.minArea = 30
        params.maxArea = 300





    # Detect blobs on the opened image
    blobDetect.detect_blobs(opened)


    # Color block the image to find lightning by color
    # ---------------------------------------------------------------------
    # Define the upper and lower boundaries for a color
    # to be considered "green"
    # This defines
    # the lower and upper limits of the shades of green in the HSV
    # color space.
    # ----------------------------------------------------------------------

    # Doesn't find any lightning
    # colorLower = np.array([107, 200, 200],  dtype = "uint8")  # 256 = 0
    # colorUpper = np.array([119, 255, 255], dtype = "uint8")


    # Get the color blocked binary image
    block = HSVCOLORBLOCK(opened, colorLower, colorUpper)

    # Get list of x,y pixel values of each keypoint
    xyList = blobDetect.get_keypoints_xy(True)
    logging.debug("xyList = %s",xyList)

    # Dilate the binary image to compare binary pixel values
    # focalLength = issimg.get_focal_length()
    # if (focalLength <= 30):
    #     kNum = 7
    # elif (focalLength >30 and focalLength <=50):
    #     kNum = 9
    # elif (focalLength > 50 and focalLength <= 70):
    #     kNum = 11
    # else:
    #     kNum = 15

    logging.info("focal length = %s",focalLength)
    logging.info("dilation kernel number = %s",kNum)
    kernel = np.ones((kNum, kNum), np.uint8)
    dilation = cv2.dilate(block.binary,kernel,iterations = 1)

    # only do this for long focal lengths :
    if (focalLength > 70):
        # Do a closing of the dilation to get rid of black spots in middle of white sections
        kernel = np.ones((51, 51), np.uint8)
        temp = dilation.copy()
        dilation = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)

        # Close a few more times
        temp = dilation.copy()
        dilation = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        temp = dilation.copy()
        dilation = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        # temp = dilation.copy()
        # dilation = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
        # temp = dilation.copy()
        # dilation = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)



    if (showImages) :
        cv2.imshow("dilation", dilation)

    # Print out the keypoints of the blobs
    blobDetect.print_keypoints(hsvImage)

    # Loop through and check values of keypoints pixels in the binary dilated image
    for xy in xyList:
        # get the  blue, green, red components of pixel[0,0]
        ix = xy[0]
        iy = xy[1]
        binaryValue = block.binary[iy, ix]
        dilateValue = dilation[iy, ix]
        logging.debug("binaryValue = %s",binaryValue)
        logging.debug("dilation = %s", dilateValue)

    # -------------------------------------------------------------
    # Make a list of keypoints that are white in the dilated image
    # -------------------------------------------------------------
    lightningExists = False
    colorKeypoints = []
    for xy, kp in zip(xyList, blobDetect.keypoints) :
        ix = xy[0]
        iy = xy[1]
        logging.debug("dilation[iy,ix] = %s", dilation[iy, ix])
        if dilation[iy, ix] > 0 :
            logging.debug("Adding on the color keypoint")
            colorKeypoints.append(kp)
            lightningExists = True

    # Check the list of keypoints
    logging.debug(" ")
    logging.debug("colorKeypoints = ")
    for keyPoint in colorKeypoints:
        y = keyPoint.pt[1]
        x = keyPoint.pt[0]
        s = keyPoint.size
        logging.debug("color keypoint : %s %s %s", x, y, s)


    # ------------------------------------
    # Get % of pixels that are this color
    # -------------------------------------
    percentColor = block.get_percent()

    # -----------------------------------------
    # Show the box around the largest contour
    # -----------------------------------------
    if showContours and (percentColor > 0):

        # Get the largest contour around the color block
        cnt = block.get_largest_contour()
        # compute the (rotated) bounding box around then
        # contour and then draw it
        # minAreaRect gets min. bounding box around contour
        # cv2.boxPoints re-shapes the bounding box to be a list of points,
        # so in can be drawn w/ drawContours
        if cnt.any():
            rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))

            # draw the boundaries of the box
            cv2.drawContours(issimg.image, [rect], -1, (0, 255, 0), 2)

    # ------------------------------------------------------------------
    # Put name of file, focal length, sun elevation text on the image
    # Put this on before  drawing keypoints onto the image
    # -----------------------------------------------------------------
    issimg.put_text()

    # --------------------------------------------------------------
    # Draw detected blobs as green circles.
    # --------------------------------------------------------------
    im_with_keypoints = blobDetect.draw_keypoints(issimg.image)

    # draw color keypoints on the image (to have both sets of keypoints on the image, one green, one red)
    im_with_color_keypoints = cv2.drawKeypoints(im_with_keypoints, colorKeypoints, np.array([]), (255, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # For only show the color keypoints :
    #im_with_color_keypoints = cv2.drawKeypoints(issimg.image, colorKeypoints, np.array([]), (255, 0, 255),
    im_with_color_keypoints=cv2.drawKeypoints(im_with_color_keypoints, colorKeypoints, np.array([]), (255, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



    # write lightning text on image
    if lightningExists:
        ltext = 'Lightning'
    else:
        ltext = 'No Lightning'

    # Write result to log file
    logging.info(ltext)

    cv2.putText(im_with_color_keypoints, ltext, (400, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (69, 69, 255), 1)


    # Show images if desired
    if (showImages):

        # show the frame and the binary image
        # USE THE ISSIMAGE TO SHOW THE ORIGINAL IMAGE *******
        # cv2.imshow(imagePath, resized)
        # show the image
        #cv2.imshow("the resized image", issimg.image)
        #issimg.show()
        #cv2.imshow("original image w/ keypoints", im_with_keypoints)

        # show both keypoints
        cv2.imshow("original image w/ both keypoints", im_with_color_keypoints)

        if (doSmoothing):
            cv2.imshow("filtered", filtered)

        if doOpening:
            cv2.imshow("opening", opened)

        # show the binary image from color blocking
        cv2.imshow("Binary", block.binary)

        cv2.waitKey(0)

        # plot this histogram
        # plot_color_hist(image)

        cv2.destroyAllWindows()

    if (writeImage and args.out):



        # outname = args.out + '/' + get_filename(filename) + '_blob.jpg'
        # logging.debug("Writing output to %s", outname)
        # cv2.imwrite(outname, im_with_keypoints)

        # show both keypoints
        outname = args.out + '/' + get_filename(filename) + '_blob.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, im_with_color_keypoints)

        outname = args.out + '/' + get_filename(filename) + '_filter.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, filtered)

        #  write out the binary image
        outname = args.out + '/' + get_filename(filename) + '_binary.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, block.binary)

        #  write out the dilation image
        outname = args.out + '/' + get_filename(filename) + '_dilation.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, dilation)


        if doOpening:
            outname = args.out + '/' + get_filename(filename) + '_open.jpg'
            cv2.imwrite(outname, opened)


    logging.debug(" ")
    # End of for loop

