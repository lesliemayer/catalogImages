"""Python code to read in an image and determine if there is
lightning in the image by using simple blob detection and color blocking.  This version of the code is being tuned
for nadir viewed lightning.
Usage :  python lightning_detection_nadir.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt
"""

# usage :
# python lightning_detection_nadir.py F:\imagews\training --log=debug --list="F:\imagews\training\small_lightning_test.txt"
# python lightning_detection_nadir.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\BetterLightning\Blobs"
# python lightning_detection_nadir.py F:\imagews\training\ --log=debug --list="F:\imagews\training\no_lightning.txt"
# python lightning_detection_nadir.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt"
# python lightning_detection_nadir.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"
# python lightning_detection_nadir.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt" --out="E:\BetterLightning\BlobColorTest"
# python lightning_detection_nadir.py E:\BetterLightning --log=debug --list="E:\BetterLightning\testlightning.txt" --out="E:\BetterLightning\BlobColorTest"
# python lightning_detection_nadir.py E:\BetterLightning --log=debug --list="E:\BetterLightning\testlightning.txt" --out="E:\BetterLightning\minThresh150"

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
writeImage = False


# -----------------------------------------------
# Display the images while looping through them?
# -----------------------------------------------
showImages = True

# ----------------------------------------------------
# Get rid of stars by eroding the dilating (opening)
# ----------------------------------------------------
doOpening = True  # Need this, even for nadir, gets rid of extra little white/purple areas
                  # Actually get less blobs w/ the opening than without!!!
                  # Could maybe do less of an opening though.
#doOpening = False

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

# Minimum % of white/blue/purple  for it to be a nadir lightning image
minPercentWhiteBluePurple = .1


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

# # Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()


print "default params :"
print "filterByColor = " + str(params.filterByColor)
print "filterByArea = " + str(params.filterByArea)
print "default min Area : " + str(params.minArea)
print "default max Area : " + str(params.maxArea)
print "filterByCircularity = " + str(params.filterByCircularity)
print "filterByInertia = " + str(params.filterByInertia)
print "filterByConvexity = " + str(params.filterByConvexity)


# Change thresholds
# params.minThreshold = 10 too small
#params.minThreshold = 100
params.minThreshold = 50
#params.minThreshold = 150  # leaves out some lightning
#params.maxThreshold = 200
params.maxThreshold = 255  # 01/31/2017  test

# Filter by Area.
params.filterByArea = True


# Filter by Circularity (4*Pi*Area/Perimeter*Perimeter)
# A circle has circularity = 1, square = .785
params.filterByCircularity = False
# params.minCircularity = 0.1
#params.maxCircularity = 1.1


# Filter by Convexity  : this is needed for lightning shape
# Area of blob/Area of convex hull
params.filterByConvexity = False
# params.minConvexity = 0.5
# params.maxConvexity = 1.1  #LEAVE THIS COMMENTED OUT, ELSE WILL LEAVE OUT SOME BLOBS ******* (why, I don't know)
#                            #  if leave out maxConvexity is a huge number.   Set to > 1 , not 1!


# Filter by Inertia
params.filterByInertia = True
#params.minInertiaRatio = 0.5
params.minInertiaRatio = 0.2  # 05/01/2017
params.maxInertiaRatio = 1.1


# Filter by color?
params.filterByColor = True

# By default the detector looks for dark blobs. You can tell it instead to
# look for light blobs by setting params.blobColor = 255
params.blobColor = 255

print "set params :"
print "filterByColor = " + str(params.filterByColor)
print "filterByArea = " + str(params.filterByArea)
print "default min Area : " + str(params.minArea)
print "default max Area : " + str(params.maxArea)
print "filterByCircularity = " + str(params.filterByCircularity)
print "filterByInertia = " + str(params.filterByInertia)
print "filterByConvexity = " + str(params.filterByConvexity)



# Need to have this AFTER params are set by focal length, down below
# # initialize blob detector object
# blobDetect = BLOBDETECT(params)

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

# new test : 04/13/2017
colorLower = np.array([100, 40, 100], dtype="uint8")
colorUpper = np.array([155, 150, 255], dtype="uint8")

logging.info("colorLower = %s", colorLower)
logging.info("colorUpper = %s", colorUpper)

minSunElev = -20.
logging.info("min Sun Elevation allowed : %s", minSunElev)


# color mask for bright white light
# Great for getting really bright white light
whiteLower = np.array([0, 0, 250], dtype="uint8")
whiteUpper = np.array([255, 20, 255], dtype="uint8")
# Trying to get not as bright white light :
#whiteLower = np.array([0, 0, 240], dtype="uint8")  # leaves s050 is61120 out
# whiteLower = np.array([0, 0, 230], dtype="uint8")  # leaves s050 is61120 out
# whiteUpper = np.array([255, 15, 255], dtype="uint8")

# This gets too much city lights
# whiteLower = np.array([0, 0, 250], dtype="uint8")  # Get only the super white spots  - gets the moon ***
# whiteUpper = np.array([255, 15, 255], dtype="uint8")

whiteLower = np.array([0, 0, 250], dtype="uint8")  # Get only the super white spots  - gets the moon ***
whiteUpper = np.array([0, 0, 255], dtype="uint8")

allWhitesLower = np.array([0, 0, 165], dtype="uint8")
allWhitesUpper = np.array([255, 39, 255], dtype="uint8")

logging.info("lightning_detection_nadir : whiteLower = %s", whiteLower)
logging.info("lightning_detection_nadir : whiteUpper = %s", whiteUpper)

logging.info("lightning_detection_nadir : allWhitesLower = %s", allWhitesLower)
logging.info("lightning_detection_nadir : allwhitesUpper = %s", allWhitesUpper)

blackLower = np.array([0, 0, 0], dtype="uint8")
blackUpper = np.array([255, 255, 25], dtype="uint8")

logging.info("lightning_detection_nadir : blackLower = %s", blackLower)
logging.info("lightning_detection_nadir : blackUpper = %s", blackUpper)




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
        logging.info("SunElev too large, skipping")
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

    # Algorithm won't work on very large focal lengths :
    # if (focalLength > 200) :
    #     logging.info("Focal length > 200, skipping")
    #     continue


    # The attribute .size is the diameter of the blob, not its area!!!!!!!!!!
    # Size determines the diameter of the meaningful keypoint neighborhood.
    # # You can use that size and roughly calculate the area of the blob.

    # intitialize min/max area
    params.minArea = 50.
    params.maxArea = 10000.
    kNum = 7

    # COMMENTED OUT FOR TESTING 05/01/2017 ***************
    if (focalLength <= 30):
        kNum = 7
        #kNum = 15  # 05/01/2017
        #params.minArea = 10.
        params.minArea = 100.  # 05/01/2017
        #params.maxArea = 60.
    elif (focalLength >30 and focalLength <=50):
        kNum = 9
        #kNum = 15 # 05/01/2017
        #params.minArea = 15.
        params.minArea = 100.  # 05/01/2017
        #params.maxArea = 80.
    elif (focalLength > 50 and focalLength <= 70):
        kNum = 11
        #kNum = 15  # 05/01/2017
        #params.minArea = 20.
        params.minArea = 100.  # 05/01/2017
        #params.maxArea = 100.
    elif (focalLength > 70 and focalLength <= 150):
        kNum = 15
        #params.minArea = 25.
        params.minArea = 100.
        #params.maxArea = 150.
    elif (focalLength > 70 and focalLength <= 150):
        kNum = 15
        #params.minArea = 30.
        params.minArea = 100.  # 05/01/2017
        #params.maxArea = 200.
    elif (focalLength > 150 and focalLength <= 250):
        kNum = 15
        params.minArea = 100.  # 05/01/2017
        #params.maxArea = 200.
    elif (focalLength > 250 and focalLength <= 350):
        kNum = 15
        params.minArea = 150.
    else  :
        kNum = 15
        params.minArea = 300.
        #params.maxArea = 300.

    # Check the parameters for the blob detector:
    logging.debug("kNum, params.minArea = %s, %s",kNum, params.minArea)

    # # initialize blob detector object
    blobDetect = BLOBDETECT(params)

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
    logging.debug("xyList of keypoints = %s",xyList)

    # Get the bright white pixels
    whiteBlock = HSVCOLORBLOCK(filtered, whiteLower, whiteUpper)

    # Add together the two color blocked images
    bothMasks = cv2.add(block.binary, whiteBlock.binary)

    # Get number of ALL the white pixels (not just bright ones)
    allWhitesBlock = HSVCOLORBLOCK(filtered, allWhitesLower, allWhitesUpper)

    # Want to check how many dark pixels there are
    blackBlock = HSVCOLORBLOCK(filtered, blackLower, blackUpper)

    # ---------------------------------------------------------------
    # Check the sum of pixels that are all white, white, black, or blue/purple
    # ---------------------------------------------------------------
    temp = cv2.add(bothMasks, blackBlock.binary)
    allColors = cv2.add(allWhitesBlock.binary, temp)

    # ------------------------------------
    # Get % of pixels that are this color
    # -------------------------------------
    #allMasksObject = HSVCOLORBLOCK(allMasks)

    #percentAllColor = allMasksObject.get_percent()

    totalPix = allColors.shape[0] * allColors.shape[1]
    #logging.debug("total Pixels in resized image : %s * %s = %s", self.binary.shape[1], self.binary.shape[0], totalPix)

    # For testing, create array of all 1's
    # nonZero = np.count_nonzero(np.ones((self.binary.shape[0], self.binary.shape[1])))

    # Get number of non-zero pixels :
    nonZero = np.count_nonzero(allColors)
    logging.debug("Number of non-zero pixels in allMasks array : %s", nonZero)

    # Calculate the percentage from the non zero pixels
    percentAllColor = (float(nonZero) / float(totalPix)) * 100.

    logging.info("percentAllColor = %s", percentAllColor)

    if percentAllColor < 80. :
         logging.info("Not black, white, purple/blue enough, skipping %s", percentAllColor)
         continue

    # ---------------------------------------------------
    # Now check if a large portion is white, blue/purple
    # ---------------------------------------------------
    whiteBluePurpleSum = cv2.add(block.binary, allWhitesBlock.binary)

    # Check % of image :

    # Get number of non-zero pixels :
    nonZero = np.count_nonzero(whiteBluePurpleSum)
    logging.debug("Number of non-zero pixels in whiteBluePurpleSum array : %s", nonZero)

    # Calculate the percentage from the non zero pixels
    percentWhiteBluePurpleColor = (float(nonZero) / float(totalPix)) * 100.

    logging.info("percentWhiteBluePurpleColor = %s", percentWhiteBluePurpleColor)

    # Make sure this is enough % of white/blue/purple to qualify as nadir lightning
    if percentWhiteBluePurpleColor < minPercentWhiteBluePurple :
         logging.info("Not white, purple/blue enough, skipping %s", percentWhiteBluePurpleColor)
         continue


    # ------------------------------------
    # Get % of pixels that are this color
    # -------------------------------------
    # percentBlackColor = blackBlock.get_percent()
    #
    # logging.info("percentBlackColor = %s", percentBlackColor)
    #
    # if percentBlackColor < .7 :
    #     logging.info("Not black enough, skipping")
    #     continue


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

    # Do opening on binary mask to get rid of tiny white/blue/purple areas



    logging.info("focal length = %s",focalLength)
    logging.info("dilation kernel number = %s",kNum)
    kernel = np.ones((kNum, kNum), np.uint8)
    #dilation = cv2.dilate(block.binary,kernel,iterations = 1)
    # Dilate the sum of masks
    dilation = cv2.dilate(bothMasks, kernel, iterations=1)


    # only do this for long focal lengths :
    #if (focalLength > 70):
    if (focalLength > 70):  # 05/01/2017
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
    # xyList are the rounded xy values of keypoints
    # blobDetect.keypoints are real (the center of the keypoint)
    for xy, kp in zip(xyList, blobDetect.keypoints) :
        ix = xy[0]
        iy = xy[1]
        logging.debug("xy, kp = %s %s %s", xy, kp.pt[0], kp.pt[1])
        logging.debug("dilation[iy,ix] = %s", dilation[iy, ix])
        if dilation[iy, ix] > 0 :
            logging.debug("Adding on the color keypoint")
            colorKeypoints.append(kp)
            # Check size of the keypoint :
            # Only do this if want to check by diameter size, instead of Area
            #if (kp.size > minSize)
            lightningExists = True

    # Check the list of keypoints
    logging.debug(" ")
    logging.debug("colorKeypoints = ")
    for keyPoint in colorKeypoints:
        y = keyPoint.pt[1]
        x = keyPoint.pt[0]
        s = keyPoint.size  # THIS IS THE SIZE OF THE DIAMETER!!!
        logging.debug("color keypoint x,y, diameter size : %s %s %s", x, y, s)


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

    if (lightningExists and args.out):
        # outname = args.out + '/' + get_filename(filename) + '_blob.jpg'
        # logging.debug("Writing output to %s", outname)
        # cv2.imwrite(outname, im_with_keypoints)

        # show both keypoints
        outname = args.out + '/' + get_filename(filename) + '_blob.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, im_with_color_keypoints)

    logging.debug("writeImage = %s", writeImage)
    if (writeImage and args.out):

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

        # Write out the white color block image
        outname = args.out + '/' + get_filename(filename) + '_white.jpg'
        logging.debug("Writing output to %s", outname)
        cv2.imwrite(outname, whiteBlock.binary)


        if doOpening:
            outname = args.out + '/' + get_filename(filename) + '_open.jpg'
            cv2.imwrite(outname, opened)


    logging.debug(" ")
    # End of for loop

