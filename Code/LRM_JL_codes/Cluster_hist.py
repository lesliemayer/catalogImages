'''
Use K-means cluster with LAB color histograms to cluster the given images.
Created on Apr 14, 2016
@author: jslee3
Modified by L.R. Mayer Sept 2016
'''
# original: pyimagesearch_gurus_10.3

# usage: python Cluster_hist.py  --dataset images --clusters 2
# usage: python Cluster_hist.py  --dataset F:\imagews\training  --clusters 8

# import the necessary Packages
from sklearn.cluster import KMeans
from imutils import paths 
import numpy as np 
import argparse 
import cv2

# construct the argument parser and parse the arguments 
ap = argparse.ArgumentParser() 
ap.add_argument("-d", "--dataset", required=True, 
                help="Path to the input dataset directory")

ap.add_argument("-k", "--clusters", type=int, default=2,
                help="# of clusters to generate")
args=vars(ap.parse_args())

class LabHistogram:
    """Describe the image using the LAB histograms"""
    def __init__(self,bins):
        # store the number of bins for the histogram
        # bins is a list of the 3 bin sizes for LAB color
        self.bins=bins 
        
    def describe(self, image, mask=None):
        # convert the image to the L*a*b color space, compute a histogram,
        # and normalize it
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        hist = cv2.calcHist([lab], [0,1,2], mask, self.bins,
                            [0,256,0,256,0,256])
        hist = cv2.normalize(hist, hist).flatten()
        
        # return the histogram
        return hist 
    
# initialize the image descriptor along with the image matrix
desc = LabHistogram([8,8,8])
data = [] 

# grab the image paths from the dataset directory 
imagePaths = list(paths.list_images(args["dataset"]))
imagePaths = np.array(sorted(imagePaths))

# loop over the input dataset of images 
for imagePath in imagePaths:
    # load the image, describe the image, update the list of data
    image = cv2.imread(imagePath)
    hist = desc.describe(image)
    data.append(hist)
    
# cluster the color histograms 
clt = KMeans(n_clusters=args["clusters"])
labels = clt.fit_predict(data)

# Define where to store results of script
def update_data(results):
    # This function writes query results to csv file
    with open(r'D:\Python_Scripts\OpenCV2\kmeans_results.csv', 'ab') as csvfile:
        csvfile.write(results)

# loop over the unique labels
for label in np.unique(labels):
    # grab all image paths that are assigned to current label
    labelPaths = imagePaths[np.where(labels == label)]

     
    # loop over the image paths that belong to the current label
    for (i, path) in enumerate(labelPaths):
        output = "\n%d: %s" % (label + 1, path)
#         print output
        update_data(output)


        
#         # load the image and display it 
#         image = cv2.imread(path)
#         cv2.imshow("Cluster {}, Image #{}".format(label + 1, i + 1), image)
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
