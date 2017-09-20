'''Create either a decision tree or random forest classifier using python lists of positive and
   negative training files, set up an HSV color and texture image descriptor, make a list of labels
   and features for the positive and negative images, convert the lists to numpy arrays, and use as
   inputs to the classifier. (recently added pList, code needs to be fixed so pList works)

    Created on Feb 20, 2017

    @author: lrmayer
'''

# orig: https://gurus.pyimagesearch.com/topic/decision-trees/ (modified)

# usage: python ML_make_model.py training
# usage: python ML_make_model.py F:\imagews\training  --log critical
# usage: python ML_make_model.py E:\catalog_data\imagews\training  --log info  --model mName

# shorter dataset for testing the code on (& for benchmark)
# usage python ML_make_model.py E:\catalog_data\imagews\training --log info --model ../Models/TestModelPickle/Test --forest
# Full training set : takes 2.5 hours to run - might be able to set to use 2 processes : see
#    info on random forest classifier
# usage python ML_make_model.py F:\imagews\training --log info --model ../Models/FullDataModel/FullData --forest
# usage python ML_make_model.py E:\ISS050 E:\ML_Lightning\nadir_lightning.txt E:\ML_Lightning\nadir_lightning E:\ML_Lightning\non_nadir_lightning.txt --log info --model ../Models/nadir_lightning/ --forest


# import necessary packages
from __future__ import print_function

import sys
sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\CatalogImages/Code')
from hsvcolortexture import HSVColorTexture  # used to 'describe' the images  *** finds this***

from sklearn.cross_validation import train_test_split  # for splitting the training & test data
from sklearn.metrics import classification_report  # for the validation part
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
#from sklearn.externals import joblib  # to dump the trained model to file
import cPickle  # for saving the model to a file (had an error trying to read a joblib saved model)


# code will look in here for paths.py :
sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\pyimagesearch_code\imutils-master\imutils')

from filelist import FileList

import numpy as np
import argparse
import cv2
import warnings
import logging  # lrm - to write messages to a logfile
import os  # to get the basename of the file and check directory existence

# =====================================================================
# ignore deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# construct argument parser and parse args
ap = argparse.ArgumentParser(description="Train a classification model and save it")
ap.add_argument("pDir", help="Path to positive training data")
ap.add_argument("pList", help="List of positive training data")

ap.add_argument("nDir", help="Path to negative training data")
ap.add_argument("nList", help="List of negative training data")

# optional arg
ap.add_argument("-f", "--forest", help="Use the random forest classifier", action="store_true")

# add the optional modelType output
ap.add_argument("-m", "--model", help="Model output filename")

# lrm :  add logging file argument
ap.add_argument("-l", "--log", help="Logging Value")

# parse the arguments
args = ap.parse_args()

# ------------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
# loglevel =
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='run_ML_make_model.log', filemode='w')

# write run parameters to log file
logging.info("log level : %s", args.log)
logging.info("ptraining directory : %s", args.pDir)
logging.info((pList + " files : %s"), args.pList)

#  -------------------------------------------------------------------------------
# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.pDir,  args.pList)
imagePaths = theList.getPathFilenames()

logging.info("imagePath is %s", imagePaths)

# Initialize the labels and description data
Labels = []
Data = []

nadirLabel = "nadir Lightning"
nonNadirLabel = "non-nadir"

#-----------------------------
# Set up the image descriptor
#-----------------------------
desc = HSVColorTexture()

# -----------------------------------------------------------
# Loop over images in training directory to create the model
# -----------------------------------------------------------
#for imagePath in imagePaths:
for filename in imagePaths:

    # Make sure the file exists
    if not os.path.isfile(filename):
        sys.exit("filename " + filename + "  does not exist")

    logging.info("Filename = %s", filename)

    # Read the image
    logging.info("reading the image : %s", filename)
    image = cv2.imread(filename)

    # Extract features from the image, then update the list of
    # Labels and features  (targets & data)
    features = desc.describe(image)

    Labels.append(nadirLabel)
    Data.append(features)

# Do non-nadir lightning images :
# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.nDir,  args.nList)
imagePaths = theList.getPathFilenames()

logging.info("imagePath is %s", imagePaths)
# -----------------------------------------------------------
# Loop over images in training directory to create the model
# -----------------------------------------------------------
for filename in imagePaths:

    # Make sure the file exists
    if not os.path.isfile(filename):
        sys.exit("filename " + filename + "  does not exist")

    logging.info("Filename = %s", filename)

    # Read the image
    logging.info("reading the image : %s", filename)
    image = cv2.imread(filename)

    # Extract features from the image, then update the list of
    # Labels and features  (targets & data)
    features = desc.describe(image)

    Labels.append(nonNadirLabel)
    Data.append(features)




# ------------------------------------------------------------
# Convert training data and training targets to numpy arrays
# to pass to the classification model
# ------------------------------------------------------------
theData = np.array(Data)
theLabels = np.array(Labels)

logging.debug("target Labels = %s", theLabels)

# -----------------------------------------
# Split the training & testing data sets
# -----------------------------------------
# construct the training and testing splits
# The machine learning model (in this case, a random forest)
# is trained using the training data and then evaluated
# against the testing data.
# It is extremely important to keep these two sets exclusive
# as it allows the model to be evaluated on data points that
# it has not already seen. If the model has already seen the
# data points, then the results are biased since it has an unfair
# advantage!
# test_size=0.3 - test dataset should be 30% of size of entire dataset
# DON'T NEED TO DO THIS !!! ***********
#(trainData, testData, trainTarget, testTarget) = train_test_split(theData, theLabels,
#                                                                  test_size=0.3, random_state=42)

# ----------------------------------
# Set up the type of model to use
# ----------------------------------
# Check to see if a Random Forest should be used instead
if args.forest:
    logging.info("Using Random Forest Classifier.........")  # lrm
    # initialize model as a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    modelType = "RFC"
else:
    logging.info("Using Decision Tree Classifier.........")  # lrm
    # Initialize model as a Decision Tree Classifier
    model = DecisionTreeClassifier(random_state=99)
    modelType = "DTC"

if args.model:
    modelOutname = args.model + "/" + "nadir_lightning_" + modelType
else:
    modelOutname = "../MODELS/" + modelType  # put in default directory w/ default name


modelReportName = modelOutname + '_class_report.txt'

logging.info("Output model name is : %s", modelOutname)
logging.info("Output report name is : %s", modelReportName)

# ----------------------------------------------
# Train the decision tree (fit data to model)
# ----------------------------------------------
logging.info("Training the model...")  # lrm
#model.fit(trainData, trainTarget)
model.fit(theData, theLabels)


# --------------------------------------------------------------------
# Evaluate the classifier & print out the accuracy : pass in the
# actual testing targets as the first parameter and then let
# the model predict what it thinks the flower species are for
# the testing data. The classification_report function then
# compares the predictions to the true targets and prints an accuracy
# report for both the overall system and each individual class label.
# ------------------------------------------------------------------------
# Need to set the target Names for the classification report
# grab the unique target names and encode the labels
# targetNames = np.unique(theLabels)
# print("target names = " + str(targetNames))
# logging.debug("target names = %s", str(targetNames))

# Do this when running the model to classify images
# reportText = classification_report(testTarget, model.predict(testData))
# logging.info(reportText)

# ---------------------------------------------
# Write classification report to report file
# ---------------------------------------------
# if model report directory doesn't exit, make it
# t

# ----------------------------------------
# print out the test results to log file
# ---------------------------------------
# for (x, y) in zip(testTarget, model.predict(testData)):
#     logging.info("Target %s   Prediction %s ", str(x), str(y))

# Save model here :
# joblib
# dump the model to file
logging.debug("Model output name is %s", modelOutname)

# ------------------------------------------------------------
# If the model output directory does not exist, create it :
# *** this is same directory as modelReportName ****
# ------------------------------------------------------------
#directory = os.path.dirname(modelOutname)
#if not os.path.exists(directory):
#    os.makedirs(directory)

# -------------------------------------
# Save the model as a python object :
# Dumps out .npy files (numpy arrays)
# -------------------------------------
# joblib.dump(model, modelOutname)

# to load model back in :
# >>> model = joblib.load(modelOutname)

with open(modelOutname + '.pickle', 'wb') as f:
     cPickle.dump(model, f)
#
# with open('screening_forest/screening_forest.pickle', 'rb') as f:
#     modelT = cPickle.load(f)







