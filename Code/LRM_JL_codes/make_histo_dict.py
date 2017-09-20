'''
Created on Dec 23, 2015

@author: jslee3

modified : lrmayer

Oct 4, 2016

'''
# This script will loop the descriptor over an image dataset,
# extract a 3D RGB histogram from each image, store the  
# features in a dictionary, and write the dictionary to file. 

 
# USAGE
# python index.py images index.cpickle
# python make_histo_dict.py E:\catalog_data\imagews\training E:\catalog_data\imagews\training\rgbdict\rgbdict.pkl

# import the necessary packages
import numpy as np
import argparse
import cPickle
import glob
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", required = True,
#     help = "Path to the directory that contains the images to be indexed")
# ap.add_argument("-i", "--index", required = True,
#     help = "Path to where the computed index will be stored")

ap = argparse.ArgumentParser(description="Make a dictionary of rgb histograms for the list of input images")
ap.add_argument("dataset", help="Directory that contains the images to be indexed")  # this is required
ap.add_argument("index", help="Path & filename where the computed index will be stored")  # this is required

args = vars(ap.parse_args())


# move RGBHistogram into its own class ********

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

# initialize the index dictionary to store our our quantified
# images, with the 'key' of the dictionary being the image
# filename and the 'value' our computed features
index = {}

# initialize our image descriptor -- a 3D RGB histogram with
# 8 bins per channel
desc = RGBHistogram([8, 8, 8])

# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # extract our unique image ID (i.e. the filename)
    k = imagePath[imagePath.rfind("/") + 1:]

    # load the image, describe it using our RGB histogram
    # descriptor, and update the index
    image = cv2.imread(imagePath)
    features = desc.describe(image)
    index[k] = features

# we are now done indexing our image -- now we can write our
# index to disk
f = open(args["index"], "w")
f.write(cPickle.dumps(index))
f.close()

# show how many images we indexed
print "done...indexed %d images" % (len(index))