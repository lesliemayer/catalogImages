# how to run :
# python recognize.py --training images/training --testing images/testing

# import the necessary packages
#from pyimagesearch.localbinarypatterns import LocalBinaryPatterns
from pyimagesearch.cloudfeaturehistogram import CloudFeatureHistogram
from sklearn.svm import LinearSVC
from  imutils import paths
import argparse
import cv2
import os
import cPickle  # for saving the model to a file
import logging

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
                help="path to the training images")
ap.add_argument("-e", "--testing", required=True,
                help="path to the testing images")
args = vars(ap.parse_args())

# Set up logging file
logging.basicConfig(level=logging.DEBUG, filename='recognize_cloud.log', filemode='w')

# initialize the local binary patterns descriptor along with
# the data and label lists
# desc = LocalBinaryPatterns(24, 8)
data = []
labels = []

# ======================================================================
# def get_feature_histogram(image):
#     # load the image, convert it to grayscale, describe it,
#     # and classify it
#
#     # Use the hsv histogram as a feature?
#     doHSVhist = False
#
#     # TOO SMOOTH
#     #filtered = cv2.bilateralFilter(image, 7, 75, 75)
#     # Median blur : remove large outliers
#     filtered = cv2.medianBlur(image, 5)
#     #gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Do a histogram equalization to bring out contrast
#     # create a CLAHE object (Arguments are optional).
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     claheGray = clahe.apply(gray)
#
#     # show the new image
#     cv2.imshow('image', claheGray)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#     # local binary pattern histogram
#     lbpHist = desc.describe(claheGray)
#
#     logging.debug("lbpHist = %s", lbpHist)
#
#     if doHSVhist :
#
#         # HSV histogram
#         # channels = [0, 1] because we need to process both H and S plane.
#         # bins = [180, 256] 180 for H plane and 256 for S plane.
#         # range = [0, 180, 0, 256]
#         # Hue value lies between 0 and 180 & Saturation lies between 0 and 256.
#         hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
#
#         # hsvHistTest = cv2.calcHist([hsv], [1], None, [256], [0, 255])
#         # cv2.normalize(hsvHistTest, hsvHistTest, 0, 255, cv2.NORM_MINMAX)
#         #logging.debug("hsvHistTest = %s", hsvHistTest)
#
#         # only look at the saturation.  Saturation of white/gray < 0.15 * 255 = 38
#         (hsvHist, _) = np.histogram(hsv[:,:,1].ravel(),
#                                  bins=np.arange(0, 255),
#                                  #bins=np.arange(0, 7),
#                                  range=(0, 255))
#
#         # normalize the histogram
#         eps = 1e-7
#         hsvHist = hsvHist.astype("float")
#         hsvHist /= (hsvHist.sum() + eps)
#
#         logging.debug("hsvHist.sum() = %s", hsvHist.sum())
#         logging.debug("hsvHist = %s", hsvHist)
#
#         # Now normalize hsvHist :
#         # normalize the histogram
#         # eps = 1e-7
#         # hsvHist = hsvHist.astype("float")
#         # hsvHist /= (hsvHist.sum() + eps)
#
#         #print "hsvHist = " + str(hsvHist)
#         #print "hsvHist = " + str(hsvHist.flatten)
#
#
#     if doHSVhist:
#         # Make a concatenated feature vector of color statistics and lbp
#         # texture features
#         # (horizontally stack the two numpy arrays) [1,2,3] [4,5,6]  ->  [1,2,3,4,5,6]
#         hist = np.hstack([lbpHist, hsvHist])
#
#         #logging.debug("hist = %s", hist )
#
#         return hist
#
#     return lbpHist

# ======================================================================

# loop over the training images
for imagePath in paths.list_images(args["training"]):
    logging.info("training image : %s", imagePath)

    # load the image, convert it to grayscale, and describe it
    # image = cv2.imread(imagePath)
    # filtered = cv2.bilateralFilter(image, 7, 75, 75)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # filtered = cv2.bilateralFilter(gray, 7, 75, 75)
    # hist = desc.describe(filtered)

    image = cv2.imread(imagePath)

    # set up histogram
    cloudFeature = CloudFeatureHistogram(False)
    hist = cloudFeature.get_feature_histogram(image)

    # extract the label from the image path, then update the
    # label and data lists
    labels.append(os.path.split(os.path.dirname(imagePath))[-1])

    data.append(hist)

#print "training labels : " + str(labels)

# train a Linear SVM on the data
#model = LinearSVC(C=100.0, random_state=42)
model = LinearSVC(C=10000.0, random_state=42)
model.fit(data, labels)

# Save the trained model
# modelOutname = r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\Texture_code\cloudLinearSVC'
#modelOutname = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel\cloud_hsv_lbp_LinearSVC'
modelOutname = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Models\CloudModel\cloud_hsv_lbp_LinearSVC_v2

with open(modelOutname + '.pickle', 'wb') as f:
    cPickle.dump(model, f)

# loop over the testing images
for imagePath in paths.list_images(args["testing"]):

    image = cv2.imread(imagePath)

    hist = cloudFeature.get_feature_histogram(image)

    # prediction = model.predict(hist)[0]
    # wrap hist as a list
    prediction = model.predict([hist])[0]

    # display the image and the prediction
    cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 255), 3)
    cv2.imshow("Image", image)
    cv2.waitKey(0)







