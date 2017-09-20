"""
Given a list of images, resize them, and save the resized image.

python code resize.py
LR Mayer from OpenCV book (pdf)
08/23/2016

arguments : E:\Lightning -li E:\Lightning\lightning.txt
arguments : E:\Lightning -li E:\Lightning\lightning.txt -w 500
arguments : F:\imagews\training\ -li F:\imagews\training\no_lightning.txt

Pass in either a directory where you want to resize all files, or a directory AND a list of files to resize
List has to be in same directory as where files to be resized are
"""


import numpy as np
import argparse
import imutils  # importing my imutils
import cv2
import os # for getting path & base name of input file, & rename smaller output file
import sys

# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Resize a list images")

ap.add_argument("dataset", help="Path to images")  # this is required

# Add list file argument
ap.add_argument("-li", "--list", help="List of images to read")

# Add image width option to list
ap.add_argument("-w", "--width", help="Width to resize to")

# parse the arguments
args = ap.parse_args()

# check to see if the list/directory is set :
if (args.list) :

    # if its a file, read the file to get the file list
    if os.path.isfile(args.list):
        with open(args.list) as f:
            fileList = []  # initialize fileList
            for line in f:
                fileList.append(line.strip())  # strip off newline, spaces, and append

        #logging.debug("fileList = %s",fileList)

        imagePaths = [args.dataset + '/' + i for i in fileList]

    else :
        sys.exit("list file does not exist")

else :  # the list input is a directory

    # --------------------------------------------------------------------
    # Grab the image path& name from the dataset directory and sort them
    # --------------------------------------------------------------------
    imagePaths = list(paths.list_images(args.dataset))
    imagePaths = sorted(imagePaths)


# If width not specified, set it to 500
if not(args.width) :
    args.width = 500


print("imagePath is %s", imagePaths)
# #----------------------------------------------------
# # resize the image by specifying height
# #----------------------------------------------------
#
# # compute the aspect ratio. new image width to be 150
# # pixels. In order to compute the ratio of the new height to
# # the old height, we simply define our ratio r to be the new
# # width (150 pixels) divided by the old width, image.shape[1]
# # ratio = new width/old width
# r = 150.0 / image.shape[1]
#
# # new image dimensions = 150 width x old height * ratio
# dim = (150, int(image.shape[0] * r))
#
# # new resized image : old image, dimension, interpolation method for resizing
# # From openCV book (pdf) : I find that using cv2.INTER_AREA obtains the best results when resizing; how-
# # ever, other appropriate choices include cv2.INTER_LINEAR,
# # cv2.INTER_CUBIC, and cv2.INTER_NEAREST.
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
#
# # show the resized image
# cv2.imshow("Resized (Width)", resized)
#
# cv2.waitKey(0)
#
# #----------------------------------------------------
# # resize the image by specifying height
# #----------------------------------------------------
# r = 500.0 / image.shape[0]
#
# dim = (int(image.shape[1] * r), 500)
#
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
#
# cv2.imshow("Resized (Height)", resized)
#
# cv2.waitKey(0)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:

    if args.list :
        if not os.path.isfile(imagePath) :
               sys.exit("imagePath " + imagePath + "  does not exist")

        # load the image, describe the image, update the list of data
        image = cv2.imread(imagePath)

        #----------------------------------------------
        # resize using my imutils function resize :
        #----------------------------------------------
        resized = imutils.resize(image, width = int(args.width))

        #cv2.imshow("Resized with Function", resized)
        #cv2.waitKey(0)

        # --------------------------------------------------------
        # write the image to a jpg
        # os.path.dirname("path") -> returns the dir part of path
        # --------------------------------------------------------
        path = os.path.dirname(imagePath)
        baseName = os.path.basename(imagePath)
        newName = path + "/Small" + baseName
        print "Writing image to {}".format(newName)
        cv2.imwrite(newName, resized)

