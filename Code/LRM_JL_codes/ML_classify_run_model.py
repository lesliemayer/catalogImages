'''
Classify images using the classifier created in ML_classify_create_model.py

Created on Apr 27, 2016
@author: jslee3
Modified lrmayer - Changed code to read in model & run on set of files
                 - Parameters saved to a file
'''
# orig: https://gurus.pyimagesearch.com/topic/decision-trees/ (modified)

#                                           query_images       model_to_use
# usage: python ML_classify_run_model.py.py F:\imagews\queries modelName
# usage: python ML_classify_run_model.py.py F:\imagews\queries modelName --log debug
# usage: python ML_classify_run_model.py.py E:\catalog_data\imagews\test modelName --results test\results.csv  --log info
#
# Benchmodel :
# C:/Users/lrmayer/My Documents/Mayer/CatalogImages/Code/Test_RFC
# usage: python ML_classify_run_model.py E:\catalog_data\imagews\test ../Models/TestModelPickle/Test_RFC.pickle --results ../Models/TestModelPickle/results  --log info

# Fullmodel :
# usage: python ML_classify_run_model.py  F:\imagews\queries ../Models/FullDataModel/Full_RFC.pickle --results ../Models/FullDataModel/results  --log info

# -----------------------------
# import necessary packages
# -----------------------------
from __future__ import print_function

from hsvcolortexture import HSVColorTexture  # used to 'describe' the images

# had to get from github, this is in - lrm
# C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\pyimagesearch_code\imutils-master\imutils-master\imutils
import sys
# code will look in here for paths.py :
sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\pyimagesearch_code\imutils-master\imutils')
import paths

import numpy as np
import argparse
import warnings

import logging # lrm - to write messages to a logfile
import datetime  # to add date/time to results filename
import os # to get the basename of the file

#from sklearn.externals import joblib
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
ap.add_argument("test", help="Path to test data")

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
logging.basicConfig(level=numeric_level, filename='run_ML_classify_run_model.log', filemode='w')

# write run parameters to log file
logging.info("log level : %s", loglevel)

logging.info("test files : %s",args.test)
logging.info("model : %s",args.model)





# -------------------------------------------
# Classify the images using the input model
# -------------------------------------------
logging.info("Classifying images ...")

# grab set of test images
imagePaths2 = sorted(paths.list_images(args.test))

#------------------------------------
# Open up the results output file
#------------------------------------
# add date & time to results filename
# get current date/time and convert to a string
now = datetime.datetime.now()
nowStr = now.strftime("%Y-%m-%d_%H-%M")
logging.info("nowStr = %s", nowStr)

# ----------------------------------------------
# Set the results output filename from the args
# ----------------------------------------------
#outFileName = r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\classify_output\ML_results_' + nowStr + '.csv'


# -----------------------------------------
# Set results output file name
# -----------------------------------------
if args.results:
    resultsName = args.results + ".csv"
else:
    resultsName = "./RESULTS/results.csv"   # put in default directory w/ default name

# If results directory doesn't exist, create it
directory = os.path.dirname(resultsName)
if not os.path.exists(directory):
    os.makedirs(directory)

logging.info("Results file is %s", resultsName)

# --------------------------------
# Get model name, load it in
# --------------------------------
modelName = args.model
#model = joblib.load(modelName)

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

#-----------------------------
# Set up the image descriptor
#-----------------------------
desc = HSVColorTexture()

#--------------------------------------------
# Loop over images in the query data set :
#--------------------------------------------
with open(resultsName, 'wb') as csvfile:

    for imagePath2 in imagePaths2:
        # grab the image and classify it
        # get filename at end of the path - lrm
        #filename = imagePath2[imagePath2.rfind("/") + 1:]
        # use basename instead ?
        filename = os.path.basename(imagePath2)
        # read the image - lrm
        logging.info("Reading test file %s",filename)
        image = cv2.imread(imagePath2)

        # describe the image
        features = desc.describe(image)

        # Run model prediction on the features
        prediction = model.predict(features)
        logging.info("Prediction is %s",prediction)
        result = "\n{},{}".format(filename, prediction)
        logging.info(result)
        csvfile.write(result)


    

