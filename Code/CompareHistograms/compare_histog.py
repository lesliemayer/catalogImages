"""Uses histogram comparison tests to compare histograms of images"""

"""How to run :
# --dataset="E:\BetterLightning\CompHist"
# --dataset="E:\BetterLightning\CompHistDis"   """

# --dataset="E:\compareHistograms\ISS045nadir"



# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="Path to the directory of images")
args = vars(ap.parse_args())

# initialize the index dictionary to store the image name
# and corresponding histograms and the images dictionary
# to store the images themselves
index = {}
images = {}

# loop over the image paths
#for imagePath in glob.glob(args["dataset"] + "/*.png"):
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    # extract the image filename (assumed to be unique) and
    # load the image, updating the images dictionary
    #filename = imagePath[imagePath.rfind("/") + 1:]
    #filename = imagePath[imagePath.rfind(r"\") + 1:]
    filename = imagePath[imagePath.rfind("ISS") :]
    print "filename = {}".format(filename)
    image = cv2.imread(imagePath)
    images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    #hist = cv2.normalize(hist).flatten()  # error : "the required argument 'dst' < pos2 >
    hist = cv2.normalize(hist, hist).flatten()

    index[filename] = hist

# METHOD #1: UTILIZING OPENCV
# initialize OpenCV methods for histogram comparison
#OPENCV_METHODS = (   #  4 IS TOO MANY ******* RUNS OUT OF MEMORY ***************
    #("Correlation", cv2.HISTCMP_CORREL),
    #("Chi-Squared", cv2.HISTCMP_CHISQR),
    #("Intersection", cv2.HISTCMP_INTERSECT),
    #("Hellinger", cv2.HISTCMP_BHATTACHARYYA))

OPENCV_METHODS = (   #  4 IS TOO MANY ******* RUNS OUT OF MEMORY ***************
     ("Correlation", cv2.HISTCMP_CORREL),
     ("Chi-Squared", cv2.HISTCMP_CHISQR),
     )

OPENCV_METHODS = (
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA),
    )



# loop over the comparison methods
for (methodName, method) in OPENCV_METHODS:
    # initialize the results dictionary and the sort
    # direction
    results = {}
    reverse = False

    # if we are using the correlation or intersection
    # method, then sort the results in reverse order
    if methodName in ("Correlation", "Intersection"):
        reverse = True

    # The image to compare to :
    imageCompName = "ISS045-E-3500.jpg"
    #imageCompName = "ISS045-E-165.jpg"
    #imageCompName = "ISS045-E-22096.jpg"

    for (k, hist) in index.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = cv2.compareHist(index[imageCompName], hist, method)
        results[k] = d

    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)

    # show the query image
    fig = plt.figure("Query")
    ax = fig.add_subplot(1, 1, 1)
    #ax.imshow(images["doge.png"])
    #ax.imshow(images["ISS045-E-3500.jpg"])
    ax.imshow(images[imageCompName])
    plt.axis("off")

    # initialize the results figure
    fig = plt.figure("Results: %s" % (methodName))
    fig.suptitle(methodName, fontsize=20)

    # loop over the results
    for (i, (v, k)) in enumerate(results):
        # show the result
        ax = fig.add_subplot(1, len(images), i + 1)
        ax.set_title("%s: %.2f" % (k, v))
        plt.imshow(images[k])
        plt.axis("off")

# show the OpenCV methods
plt.show()





