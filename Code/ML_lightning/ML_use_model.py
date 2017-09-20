'''
Created on Feb 22, 2017

@author: lrmayer

'''
# orig: https://gurus.pyimagesearch.com/topic/decision-trees/ (modified)

#                                           query_images       model_to_use
# usage: python ML_use_model.py E:\catalog_data\imagews\test modelName --results test\results.csv  --log info
#
# Benchmodel :
# C:/Users/lrmayer/My Documents/Mayer/CatalogImages/Code/Test_RFC
# usage: python ML_use_model.py E:\catalog_data\imagews\test E:\catalog_data\imagews\test\test.txt  ../Models/TestModelPickle/Test_RFC.pickle --results ../Models/TestModelPickle/results  --log info

# Fullmodel :
# usage: python ML_use_model.py  F:\imagews\queries E:\catalog_data\imagews\test\test.txt ../Models/FullDataModel/Full_RFC.pickle --results ../Models/FullDataModel/results  --log info

# -----------------------------
# import necessary packages
# -----------------------------
from __future__ import print_function
from issimage import ISSIMAGE
from hsvcolortexture import HSVColorTexture  # used to 'describe' the images w/ HSV color and texture
from filelist import FileList  # import the filelist class

import numpy as np
import argparse
import warnings

import logging # lrm - to write messages to a logfile
import datetime  # to add date/time to results filename
import os # to get the basename of the file

import cPickle  # for saving the model to a file (had an error trying to read a joblib saved model)
import cv2
#=====================================================================


# ignore deprecation warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# ------------------------------------------
# construct argument parser and parse args
# ------------------------------------------
ap = argparse.ArgumentParser(description="Use a classification model to classify images")

# Path to the test data set
ap.add_argument("testDir", help="Path to test data")

# List of test images
ap.add_argument("testList", help="List of test data")


# Path to the model
ap.add_argument("model", help="Path to model to use")

# Add logging file argument
ap.add_argument("-l", "--log", help="Logging Value")

# Add results file argument
ap.add_argument("-r", "--results", help="Name of results file (csv file)")

# parse the arguments
args = ap.parse_args()


# ----------------------------------------------------------------------
# Get the logging level from the args
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
# ----------------------------------------------------------------------
loglevel = args.log
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='run_ML_use_model.log', filemode='w')

# write run parameters to log file
logging.info("log level : %s", loglevel)

logging.info("test dir : %s",args.testDir)
logging.info("test list : %s",args.testList)
logging.info("model : %s",args.model)


# Only look at images that are night time
minSunElev = -20.
logging.info("min Sun Elevation allowed : %s", minSunElev)



# -------------------------------------------
# Classify the images using the input model
# -------------------------------------------
logging.info("Classifying images ...")

# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.testDir,  args.testList)
imagePaths = theList.getPathFilenames()

# grab set of test images  - FIX
#imagePaths2 = sorted(paths.list_images(args.testDir))


#------------------------------------
# Open up the results output file
#------------------------------------
# add date & time to results filename
# get current date/time and convert to a string
now = datetime.datetime.now()
nowStr = now.strftime("%Y-%m-%d_%H-%M")
logging.info("nowStr = %s", nowStr)


# -----------------------------------------
# Set results output file name
# -----------------------------------------
if args.results:
    resultsName = args.results + ".csv"
else:
    resultsName = "./RESULTS/results.csv"   # put in default directory w/ default name

# -----------------------------------------------
# If results directory doesn't exist, create it
# -----------------------------------------------
directory = os.path.dirname(resultsName)
if not os.path.exists(directory):
    os.makedirs(directory)

logging.info("Results file is %s", resultsName)

# --------------------------------
# Get model name, load it in
# --------------------------------
modelName = args.model

logging.info("model name = %s", modelName)

# ---------------------------
# Check for model existence
# ---------------------------
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

#-----------------------------
# Set up the image descriptor
#-----------------------------
desc = HSVColorTexture()

#--------------------------------------------
# Loop over images in the query data set :
#--------------------------------------------
with open(resultsName, 'wb') as csvfile:

    # --------------------------------------
    # Loop over the input                        dataset of images
    # --------------------------------------
    for filename in imagePaths:
    # for imagePath2 in imagePaths2:
    #     # Grab the image and classify it
    #     # Set up the ISSIMAGE object
        issimg = ISSIMAGE(filename)

        """Only look at images with sun elevation > minSunElev"""
        if issimg.get_sun_elev() > minSunElev:
            continue

        filename = os.path.basename(filename)
        # read the image - lrm
        logging.info("Reading test file %s",filename)
        image = cv2.imread(filename)

        # describe the image
        features = desc.describe(issimg.image)

        # Run model prediction on the features
        prediction = model.predict(features)
        logging.info("Prediction is %s",prediction)
        result = "\n{},{}".format(filename, prediction)
        logging.info(result)
        csvfile.write(result)


    

