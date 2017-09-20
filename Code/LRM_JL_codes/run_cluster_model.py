'''


Created on Apr 14, 2016
@author: jslee3
Modified by lrmayer  Sept 28, 2016
'''
# original: pyimagesearch_gurus_10.3

# usage: python run_cluster_model.py  E:\catalog_data\imagews\training --clusters 8

# ------------------------------
# Import the necessary Packages
# ------------------------------
from sklearn.cluster import KMeans
from imutils import paths 
import numpy as np 
import argparse 
import cv2

# ------------------------------------
# Show the images & their category?
# ------------------------------------
showImages = True

# ----------------------------------
# Resize the image b/f displaying?
# ----------------------------------
resizeImage = True

# ------------------------------------------------------
# Construct the argument parser and parse the arguments
# ------------------------------------------------------
ap = argparse.ArgumentParser()

ap = argparse.ArgumentParser(description="Run a Kmeans Cluster model")
ap.add_argument("dataset", help="Path to input images")  # this is required
ap.add_argument("-c", "--clusters", type=int, default=2, help="# of clusters to generate")


# parse the arguments
args = ap.parse_args()





class LabHistogram:
    def __init__(self,bins):
        # store the number of bins for the histogram
        self.bins=bins 
        
    def describe(self, image, mask=None):
        """"------------------------------------------------------------------
        convert the image to the L*a*b color space, compute a histogram,
        and normalize it
        ------------------------------------------------------------------"""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        hist = cv2.calcHist([lab], [0,1,2], mask, self.bins,
                            [0,256,0,256,0,256])
        hist = cv2.normalize(hist, hist).flatten()
        
        # return the histogram
        return hist 

# ------------------------------------------------------------
# initialize the image descriptor along with the image matrix
# ------------------------------------------------------------
desc = LabHistogram([8,8,8])
data = [] 

# -----------------------------------------------------
# Grab the image paths from the dataset directory
# -----------------------------------------------------
imagePaths = list(paths.list_images(args.dataset))

imagePaths = np.array(sorted(imagePaths))

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for imagePath in imagePaths:
    # load the image, describe the image, update the list of data
    image = cv2.imread(imagePath)
    hist = desc.describe(image)

    # Append the histogram to the data list
    data.append(hist)

# ------------------------------
# Cluster the color histograms
# ------------------------------
clt = KMeans(n_clusters=args.clusters)
labels = clt.fit_predict(data)

# -----------------------------------------------
# This function writes query results to csv file
# -----------------------------------------------
# def update_data(results):
#     # Define where to store results of script
#     #with open(r'kmeans_results.csv', 'ab') as csvfile:
#     with open(r'kmeans_results.csv', 'wb') as csvfile:
#         csvfile.write(results)

# ----------------------------------
# Open the output file for writing
# ----------------------------------
with open(r'kmeans_results.csv', 'wb') as csvfile:

    # ------------------------------
    # Loop over the unique labels
    # ------------------------------
    for label in np.unique(labels):
        # grab all image paths that are assigned to current label
        labelPaths = imagePaths[np.where(labels == label)]

        # -----------------------------------------------------------
        # Loop over the image paths that belong to the current label
        # -----------------------------------------------------------
        for (i, path) in enumerate(labelPaths):
            output = "\n%d: %s" % (label + 1, path)
            #print output
            #update_data(output)
            csvfile.write(output)

            # -----------------------------------
            # Show the images and their category
            # -----------------------------------
            if (showImages) :
                # load the image and display it
                image = cv2.imread(path)

                if (resizeImage) :
                    # images are too big, need to make smaller for display
                    # ----------------------------------------------------
                    # resize the image by specifying height
                    # ----------------------------------------------------

                    # compute the aspect ratio. new image width to be X
                    # pixels. In order to compute the ratio of the new height to
                    # the old height, we simply define our ratio r to be the new
                    # width (X pixels) divided by the old width, image.shape[1]
                    # ratio = new width/old width
                    #r = X / image.shape[1]

                    pixelHeight = 500.
                    r = pixelHeight / image.shape[1]

                    # new image dimensions = pixelHeight width x old height * ratio
                    dim = (int(pixelHeight), int(image.shape[0] * r))

                    # new resized image : old image, dimension, interpolation method for resizing
                    # From openCV book (pdf) : I find that using cv2.INTER_AREA obtains the best results when resizing; how-
                    # ever, other appropriate choices include cv2.INTER_LINEAR,
                    # cv2.INTER_CUBIC, and cv2.INTER_NEAREST.
                    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

                    # show the resized image
                    cv2.imshow("Cluster {}, Image #{}".format(label + 1, i + 1), resized)

                else :

                    cv2.imshow("Cluster {}, Image #{}".format(label + 1, i + 1), image)


                # wait for a keypress and then close all open windows
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
#       # load the image and display it
#       image = cv2.imread(path)
#       cv2.imshow("Cluster {}, Image #{}".format(label + 1, i + 1), image)
#         
#     # wait for a keypress and then close all open windows 
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# 
# # loop over the unique labels
# for label in np.unique(labels):
#     # grab all image paths that are assigned to current label
#     labelPaths = imagePaths[np.where(labels == label)]
#         
#     # loop over the image paths that belong to the current label
#     for (i, path) in enumerate(labelPaths):
#         # load the image and display it 
#         filename = path[path.rfind("/") +1:]
#         kindex[filename] = label
#

# -------------------------------------------------------------------
# This sorts images according to how well they fit in a category
# -------------------------------------------------------------------
# class Searcher:
#     def __init__(self, index):
#         # store our index of images
#         self.index = index
# 
#     def search(self, queryFeatures):
#         # initialize our dictionary of results
#         results = {}
# 
#         # loop over the index
#         for (k, features) in self.index.items():
#             # compute the chi-squared distance between the features
#             # in our index and our query features -- using the
#             # chi-squared distance which is normally used in the
#             # computer vision field to compare histograms
#             d = self.chi2_distance(features, queryFeatures)
# 
#             # now that we have the distance between the two feature
#             # vectors, we can udpate the results dictionary -- the
#             # key is the current image ID in the index and the
#             # value is the distance we just computed, representing
#             # how 'similar' the image in the index is to our query
#             results[k] = d
# 
#         # sort our results, so that the smaller distances (i.e. the
#         # more relevant images are at the front of the list)
#         results = sorted([(v, k) for (k, v) in results.items()])
# 
#         # return our results
#         return results
# 
# 
# #            
# # # sort our results, so that the smaller distances (i.e. the
# # # more relevant images are at the front of the list)
# # results = sorted([(v, k) for (k, v) in results.items()])
# # 
# # 
# # # loop over the results
# # for j in xrange(0, 13058):
# #     # grab the result (we are using row-major order) 
# #     (score, imageName) = results[j]
# #     path = args["dataset"] + "/%s" % (imageName)
# #     result = cv2.imread(path)
# #     qresult = "\n%d: %s : %.3f" % (j + 1, imageName, score)
# # #    print qresult
# #     update_data(qresult)
