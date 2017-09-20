'''
Created on Dec 23, 2015

@author: jslee3

Modified by lrmayer

Oct 4, 2016



'''

# --------------------------------------------------
# Run make_histo_dict.py 1st, then find_match.py
# --------------------------------------------------
# USAGE
# python find_match.py E:\catalog_data\queries\Aurora\ISS026-E-7702.jpg E:\catalog_data\imagews\training\rgbdict\rgbdict.pkl query.csv
# python find_match.py E:\catalog_data\queries\Aurora\ISS026-E-13907.jpg E:\catalog_data\imagews\training\rgbdict\rgbdict.pkl query.csv
# E:\catalog_data\imagews\training\rgbdict\rgbdict.pkl


#  This script defines the Searcher class and distance
# measurements for the search query (search_external.py)

# NEED TO UPDATE RESULTS RANGE EVERY TIME  - what does this mean????? *

# import the necessary packages
import numpy as np
import argparse
import cPickle
import cv2
import csv

# ------------------------------------------------------
# Construct the argument parser and parse the arguments
# ------------------------------------------------------
ap = argparse.ArgumentParser()

ap = argparse.ArgumentParser(description="Given an image, find a matching one quantized by rgb histogram")
ap.add_argument("query", help="Path to image to match")  # this is required
ap.add_argument("dictionary", help="Path to where dictionary is stored")  # this is required
ap.add_argument("outName", help="Name of csv results file")  # this is required

# parse the arguments
args = ap.parse_args()



# This image descriptor script creates a 3D RGB histogram
# with 8 bins per red, green and blue channels. 
class RGBHistogram:
    def __init__(self, bins):
        # store the number of bins the histogram will use
        self.bins = bins

    def describe(self, image):
        # compute a 3D histogram in the RGB colorspace,
        # then normalize the histogram so that images
        # with the same content, but either scaled larger
        # or smaller will have (roughly) the same histogram
        hist = cv2.calcHist([image], [0, 1, 2],
            None, self.bins, [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist)

        # return out 3D histogram as a flattened array
        return hist.flatten()


class Searcher:
    def __init__(self, index):
        # store our index of images
        self.index = index

    def search(self, queryFeatures):
        # initialize our dictionary of results
        results = {}

        # loop over the index
        for (k, features) in self.index.items():

            # --------------------------------------------------------
            # compute the chi-squared distance between the features
            # in our index and our query features -- using the
            # chi-squared distance which is normally used in the
            # computer vision field to compare histograms. Lower values
            # are better
            # ---------------------------------------------------------
            d = self.chi2_distance(features, queryFeatures)

            # now that we have the distance between the two feature
            # vectors, we can udpate the results dictionary -- the
            # key is the current image ID in the index and the
            # value is the distance we just computed, representing
            # how 'similar' the image in the index is to our query
            results[k] = d

        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        results = sorted([(v, k) for (k, v) in results.items()])

        # return our results
        return results

    # this is from : http://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])
 
        # return the chi-squared distance
        return d

# ----------------------------------
# Load the query image and show it
# ----------------------------------
queryImage = cv2.imread(args.query)

# Resize the image for viewing
# images are too big, need to make smaller for display
# ----------------------------------------------------
# resize the image by specifying height
# ----------------------------------------------------

# compute the aspect ratio. new image width to be X
# pixels. In order to compute the ratio of the new height to
# the old height, we simply define our ratio r to be the new
# width (X pixels) divided by the old width, image.shape[1]
# ratio = new width/old width

pixelHeight = 500.
r = pixelHeight / queryImage.shape[1]

# new image dimensions = pixelHeight width x old height * ratio
dim = (int(pixelHeight), int(queryImage.shape[0] * r))

# new resized image : old image, dimension, interpolation method for resizing
# From openCV book (pdf) : I find that using cv2.INTER_AREA obtains the best results when resizing; how-
# ever, other appropriate choices include cv2.INTER_LINEAR,
# cv2.INTER_CUBIC, and cv2.INTER_NEAREST.
resized = cv2.resize(queryImage, dim, interpolation=cv2.INTER_AREA)


#cv2.imshow("Image to match", queryImage)
cv2.imshow("(resized) Image to match", resized)

cv2.waitKey(0)
  
# -------------------------------------------------------------
# describe the query in the same way that we did in
# make_histo_dict.py -- a 3D RGB histogram with 8 bins per
# channel
# --------------------------------------------------------------
desc = RGBHistogram([8, 8, 8])
queryFeatures = desc.describe(queryImage)

# ----------------------------------
# Load the index perform the search
# ----------------------------------
index = cPickle.loads(open(args.dictionary).read())

# Initialize the searcher object with the dictionary
searcher = Searcher(index)

# Search for best matching image
results = searcher.search(queryFeatures)

# Open the results output file and write to it
with open(args.outName, 'wb') as csvfile:

    # loop over the top results
    for j in xrange(0, len(results)):
    #for j in xrange(0, 35):
        # grab the result (we are using row-major order)
        (score, imageName) = results[j]
        path = args.dictionary + "/%s" % (imageName)
        #result = cv2.imread(path)  # not using this
        qresult = "\n%d: %s : %.3f" % (j + 1, imageName, score)

        #update_data(qresult, args.outName)
        csvfile.write(qresult)


# # loop over the results
# for (score, imageName) in results(:):
#     # grab the result (we are using row-major order) 
#     (score, imageName) = results[j]
#     path = args["dictionary"] + "/%s" % (imageName)
#     result = cv2.imread(path)
#     qresult = "\t%d: %s : %.3f" % (j + 1, imageName, score)
#     print qresult
#     update_data(qresult)

