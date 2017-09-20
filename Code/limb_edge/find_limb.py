# USAGE
# python find_limb.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"
# python find_limb.py F:\imagews\training --log=debug --list="F:\imagews\training\earthlimb.txt"
# python find_limb.py F:\imagews\training --log=debug --list="F:\imagews\training\circle.txt"
# python find_limb.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python find_limb.py F:\imagews\training --log=debug --list="F:\imagews\training\ISS.txt"


# import the necessary packages
import argparse
import os # to check list file existence
import sys
import logging #  To write messages to a logfile

import cv2
import numpy as np
from imutils import paths
from imutils import resize

# for getting focal length from the jpg file
from jpgutils import getFocalLength

# for getting focal length from the photos database
from photosdb import PHOTOSDB

# -----------------------
# For checking the path
# -----------------------
#print '\n'.join(sys.path)
#sys.exit(0)

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Find the earth limb in images")
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


# ------------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='find_limb.log', filemode='w')

# ----------------------------------
# Write run parameters to log file
# ----------------------------------
logging.info("input path is %s", args.dataset)
logging.info("log level : %s", args.log)

# initialize photosdb class for reading the database
xx = PHOTOSDB()

# --------------------------------
# Read the file names into a list
# --------------------------------
if (args.list) :

    if os.path.isfile(args.list):
        with open(args.list) as f:
            fileList = []  # initialize fileList
            for line in f:
                fileList.append(line.strip())  # strip off newline, spaces, and append filename to list

        logging.debug("fileList = %s",fileList)
        imagePaths = [args.dataset + '/' + i for i in fileList]

    else :
        sys.exit("list file does not exist")

else :

    # -----------------------------------------------------
    # Grab the image paths from the dataset directory
    # -----------------------------------------------------
    imagePaths = list(paths.list_images(args.dataset))

    # sort the filenames
    imagePaths = sorted(imagePaths)


logging.debug("imagePaths is %s", imagePaths)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")

    # ----------------
    # Load the image
    # ----------------
    image = cv2.imread(imagePath)

    # -------------------
    # Resize the image
    # -------------------
    # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
    resized = resize(image, width=500)

    # -----------------------
    # Convert to gray scale
    # -----------------------
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # smooth the image
    # nn = the neighborhood size
    nn = 11
    # nn = 5
    blurred = cv2.GaussianBlur(gray, (nn, nn), 0, borderType=cv2.BORDER_REFLECT)

    # --------------------------------------------------------
    # Compute edges on the smoothed image
    # any gradient values below 30 are considered
    # non-edges whereas any values above 150 are considered
    # sure edges.
    # --------------------------------------------------------
    #edged = cv2.Canny(blurred, 30, 150)  # not getting some limbs
    #edged = cv2.Canny(blurred, 30, 100)
    edged = cv2.Canny(blurred, 30, 50)  # gets all the limbs
    cv2.imshow("Edges", edged)


    # Show images if desired
    if (showImages) :

        imageName = os.path.basename(imagePath)

        # get the focal length & write on image
        fl = xx.getField('fclt', imageName)

        # get the sun elevation
        elev = xx.getField('elev', imageName)

        # Add text w/ % of green pixels to the image

        # draw text string of the digit on the image a x-10,y-10
        # (above & to left of bounding box)
        # putText(img, text, textOrg, fontFace, fontScale,
        #        Scalar::all(255), thickness, 8);
        cv2.putText(resized, 'fl: ' + str(fl), (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(resized, 'elev: ' + str(elev), (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


        # show the frame and the binary image
        cv2.imshow(imagePath, resized)

        cv2.waitKey(0)
        # plot this histogram
        #plot_color_hist(image)

        cv2.destroyAllWindows()



# destroy pointer & all windows
cv2.destroyAllWindows()