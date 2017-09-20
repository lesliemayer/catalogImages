'''
Created on Apr 27, 2016

@author: jslee3

Modified by L.R. Mayer
Sept 2016
'''
# orig: https://gurus.pyimagesearch.com/topic/decision-trees/ (modified)

# usage: python ML_classify.py --train training --test STS081
# usage: python ML_classify.py --train F:\imagews\training --test F:\imagews\queries --log C:\Users\lrmayer\Documents\Mayer\CatalogImages\classify_output
# usage: python ML_classify.py --train F:\imagews\training --test F:\imagews\images74 --log debug

# import necessary packages 
from __future__ import print_function 
from sklearn import cross_validation 
from sklearn.metrics import classification_report 
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

import sys
# code will look in here for paths.py :
sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\pyimagesearch_code\imutils-master\imutils')
import paths


import numpy as np 
import argparse 
import mahotas 
import cv2 
import warnings

import logging # lrm - to write messages to a logfile

#=====================================================================



warnings.filterwarnings("ignore",category=DeprecationWarning)

#--------------------------------------------------------------------------------------------------------------------
def update_data(results):
    """Define where to store results of script"""
    # This function writes query results to csv file
    #with open(r'F:\imagews\ML_results4.csv', 'ab') as csvfile:
    #with open(r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\classify_output\ML_results4.csv', 'ab') as csvfile:
    with open(r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\classify_output\ML_results_images74.csv', 'wb') as csvfile:
        csvfile.write(results)
# --------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------
def describe(image):
    """Describe the image"""
    # extract the mean and standard deviation from each
    # channel of image in HSV color space

    # convert image to HSV color space, then compute the mean & stand. dev. for each channel - lrm
    (means, stds) = cv2.meanStdDev(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    # concatenate : Join a sequence of arrays along an existing axis. returns a ndarray - lrm
    # np.ndarray.flatten : Return a copy of the array collapsed into one dimension.
    colorStats = np.concatenate([means, stds]).flatten()

    # extract Haralick texture features
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    haralick = mahotas.features.haralick(gray).mean(axis=0)

    # return a concatenated feature vector of color statistics and Haralick
    # texture features
    return np.hstack([colorStats, haralick])

#------------------------------------------------------------------------------------------------------------


# construct argument parser and parse args 
ap = argparse.ArgumentParser() 
ap.add_argument("-n", "--train", required=True, help="path to training dataset")
ap.add_argument("-t", "--test", required=True, help="dataset to classify")
ap.add_argument("-f", "--forest", type=int, default=0, help="whether or not Random Forest should be used")

# lrm :  add logging file argument
ap.add_argument("-l", "--log", required=True, help="Logging Value")

args=vars(ap.parse_args())

# lrm -------------------------------------------------------------------------------
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
loglevel = args["log"]
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='example.log', filemode='w')
# lrm -------------------------------------------------------------------------------


# grab the set of training image paths and initialize the list of training labels and matrix of features 
print("[INFO] extracting features...")
imagePaths = sorted(paths.list_images(args["train"]))
Labels = []
Data = []

# loop over images in training directory 
for imagePath in imagePaths:
    # extract the label and load image from disk
    label = imagePath[imagePath.rfind("/") + 1:].split("_")[0]
    logging.info("reading the image : %s", imagePath)
    image = cv2.imread(imagePath)
    
    # extract features from the image, then update the list of
    # labels and features 
    features = describe(image)
    Labels.append(label)
    Data.append(features)

# construct the training and testing data 
trainData = np.array(Data)
trainLabel = np.array(Labels)

    
# initialize the model as a decision tree 
model = DecisionTreeClassifier(random_state=99)

# check to see if a Random Forest should be used instead 
if args["forest"] > 0:
    logging.info("Using Random Forest Classifier.........")  # lrm
    # initialize model as a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=20, random_state=42)

# train the decision tree (first fit data to model)
print("[INFO] training model...")
logging.info("[INFO] training model...")  # lrm
model.fit(trainData, trainLabel)

# evaluate the classifier (then use model to predict)
print("[INFO] evaluating...")

# grab set of test images
imagePaths2 = sorted(paths.list_images(args["test"]))

for imagePath2 in imagePaths2:
    # grab the image and classify it
    # get filename at end of the path - lrm
    filename = imagePath2[imagePath2.rfind("/") + 1:]
    # read the image - lrm
    image = cv2.imread(imagePath2)

    # describe the image - lrm
    features = describe(image)

    # run model predict on the features
    prediction = model.predict(features)
#     print("[PREDICTION] {}: {}".format(filename, prediction))
    result = "\n{},{}".format(filename, prediction)
    logging.info(result)  # lrm
    update_data(result)   # write result to a file




# scores = cross_validation.cross_val_score(predictions, trainData, trainLabel, cv=3)
# print(scores)
# print("Classification report:\n%s" % classification_report(testLabel, predictions))
# print("Classification accuracy: %f" % accuracy_score(testLabel, predictions))

# # now for a visual inspection of a sample of images
# # loop over a few random images 
# for i in np.random.randint(0, high=len(imagePaths), size=(10,)):
#     # grab the image and classify it
#     imagePath = imagePaths[i]
#     filename = imagePath[imagePath.rfind("/") + 1:]
#     image = cv2.imread(imagePath)
#     features = describe(image)
#     prediction = model.predict(features)[0]
#     
#     # show the prediction 
#     print("[PREDICTION] {}: {}".format(filename, prediction))
#     cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), 2)
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)


    

