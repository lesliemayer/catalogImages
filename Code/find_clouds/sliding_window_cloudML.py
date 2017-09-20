"""
Code to search for clouds inside an image, using sliding windows and a trained machine learning model
"""

# To run :

# $ python sliding_window.py --image E:\ISS049\clouds\ISS049-E-687.jpg - good
# $ python sliding_window.py --image E:\ISS049\clouds\ISS049-E-694.jpg - good
# $ python sliding_window.py --image E:\ISS049\no_clouds\ISS049-E-1099.jpg
# $ python sliding_window.py --image E:\ISS049\no_clouds\ISS049-E-3887.jpg
# $ python sliding_window.py --image E:\ISS049\clouds\ISS049-E-2103.jpg - not good!  - why?***
# $ python sliding_window.py --image E:\ISS049\clouds\ISS049-E-4385.jpg - not good!  - why?***
# $ python sliding_window.py --image E:\ISS050\NoClouds\ISS050-E-18492.jpg
# $ python sliding_window.py --image E:\ISS050\NoClouds\ISS050-E-19830.jpg
# $ python sliding_window.py --image E:\ISS050\Clouds\ISS050-E-20712.jpg - good!
# $ python sliding_window.py --image E:\ISS050\Clouds\ISS050-E-19267.jpg
# $ python sliding_window.py --image I:\ISS051\ISS051-E-45661.jpg
# $ python sliding_window.py --image I:\ISS030\ISS030-E-228193.jpg
# $ python sliding_window.py --image I:\ISS030\ISS030-E-228194.jpg - very good
# $ python sliding_window.py --image I:\ISS051\ISS051-E-47623.jpg - very bad
# $ python sliding_window.py --image I:\ISS051\ISS051-E-47585.jpg - very bad
# $ python sliding_window.py --image I:\ISS037\ISS037-E-20198.jpg - miss cirrus clouds
# $ python sliding_window.py --image I:\ISS037\ISS037-E-20277.jpg - misses a bunch of clouds!!
# $ python sliding_window.py --image I:\ISS037\ISS037-E-22035.jpg - pretty good


# to get the local binary patterns descriptor
import sys
#sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\Texture_code/')
sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel/')

# from pyimagesearch.helpers import pyramid
# from pyimagesearch.helpers import sliding_window
from pyimagesearch.localbinarypatterns import LocalBinaryPatterns
from pyimagesearch.cloudfeaturehistogram import CloudFeatureHistogram
import argparse
import time
import cv2
import cPickle
import os

# =============================================================================
def sliding_window(image, stepSize, windowSize):
    """
    Slide a window across an image
    :param image:  Image to loop over
    :param stepSize: determined on a per-dataset basis
    and is tuned to give optimal performance based on your dataset of images.
    In practice, it's common to use a stepSize  of 4 to 8 pixels.
    :param windowSize:  width and height (in terms of pixels) of the window we are
    going to extract from our imag
    :return:
    """
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

# =============================================================================

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# ---------------------------------------
# Get the trained model name, load it in
# ---------------------------------------
# modelName = r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\Texture_code\cloudLinearSVC.pickle'
modelName = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel\cloud_hsv_lbp_LinearSVC.pickle'

# Check for model existence
if os.path.exists(modelName) :
    with open(modelName, 'rb') as f:
        try :
            model = cPickle.load(f)
        except :
            print ("Error reading in the model!!! exiting")
            sys.exit(1)
else :
    print ("Error : {} does not exist".format(modelName))
    sys.exit(1)


# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)

# load the image and define the window width and height
origImage = cv2.imread(args["image"])

# resize the image
image = cv2.resize(origImage,None,fx=.25, fy=.25, interpolation = cv2.INTER_AREA)

# window size for sliding window
(winW, winH) = (128, 128)
stepSize = 64
# (winW, winH) = (64, 64)  # too small
# stepSize = 32
# (winW, winH) = (256, 256)  # works, but maybe too big
# stepSize = 128


# To get the cloud features of the image
#cloudFeature = CloudFeatureHistogram(False)


# counter for what sliding window we are on
nn = 0


# loop over the image pyramid
# for resized in pyramid(image, scale=1.5):
#     # loop over the sliding window for each layer of the pyramid
#for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
#for (x, y, window) in sliding_window(image, stepSize=32, windowSize=(winW, winH)):
for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
    # if the window does not meet our desired window size, ignore it
    if window.shape[0] != winH or window.shape[1] != winW:
            continue

    # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
    # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
    # WINDOW
    # WORKS WITH THIS...........BUT NOT THE cloudFeature call *****************
    gray = cv2.cvtColor(window, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    claheGray = clahe.apply(gray)

    hist = desc.describe(claheGray)

    # set up histogram
    #hist = cloudFeature.get_feature_histogram(image)


    prediction = model.predict([hist])[0]

    # draw the window
    clone = image.copy()
    cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)

    # display the image and the prediction
    cv2.putText(clone, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 255), 3)

    cv2.imshow("Window", clone)

    if nn == 0 :
        cv2.waitKey(0)
        #time.sleep(10.)

    # Pause if there is clouds
    if prediction == 'cloud':
        cv2.waitKey(1)
        time.sleep(1.)

    cv2.waitKey(1)
    time.sleep(0.025)

    nn =+ 1



