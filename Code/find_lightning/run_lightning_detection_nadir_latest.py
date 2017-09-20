"""Automatically run the lightning_detection code on the latest images, given the frame number to start with,
   and ISS mission,
   Written by L.R. Mayer"""

import sys
import os
from photosdb import PHOTOSDB
import logging

# Example of how to run the lightning_detection code
# python lightning_detection.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"


# All images are at :
# https://io.jsc.nasa.gov/app/collections.cfm?cid=4

# ISS mission
mission = 'ISS052'

# Roll, frame , minimum sun elevation settings
# -----------------------------------------------------------------------------
roll = 'E'
#              1234567
# firstFrame = '      0'  # frame string HAS to be this size to work!!
# firstFrame =   '  28549'
#firstFrame =   '  39972'  # running 05/23/2017 ISS051
#firstFrame =   '  46007'  # running 05/23/2017 ISS051
#firstFrame =  '      0'   # running 05/24/2017 ISS052

#firstFrame = '      0'  # running 07/07/2017 ISS052  # last image was 10935
# Ran ISS052 07/20/2017 :
#firstFrame = '  10935'

# Ran ISS052 08/01/2017 :
firstFrame = '  13664'

# ------------------------------------------------------------------------------
minSunElev = -22  # has to be in small integer, not a float
# -------------------------------------------------------------------

# Where input images are
inDir = r"\\EO-Web\images\ESC\large/" + mission + "/"

# List of input images
listName = 'E:/' + mission + '/latest_images.txt'
listIN = r'--list=' + listName



# output directory
outDirName = r'E:/' + mission + '/NadirResults/firstframe' + firstFrame.strip() + '/'

# Make the directory if it doesn't exist
directory = os.path.dirname(outDirName)
if not os.path.exists(directory):
    os.makedirs(directory)

# Make the output directory argument
outDirArg = r'--out=' + outDirName

# Set the logging level
logLevelName = 'debug'
#logLevelName = 'info'

# Make the log level argument
logLevel = r'--log=' + logLevelName

# Check the log level value
numeric_level = getattr(logging, logLevelName.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % logLevel)

# Set the logging filename
logName = "run_lightning_detection_nadir_test.log"

# Set up the logging file :
# **** if there is problem w/ logging file will quietly go on unless you catch it ********
try:
    logging.basicConfig(level=numeric_level, filename=logName, filemode='w')
except Exception, e:
    print 'Error setting up log file {}'.format(logName)
    sys.exit(1)


# Initialize the database connection
photosDB = PHOTOSDB()

# Check E:\ISS050\lightning_imagesforShultz.txt to get the last frame
table = 'nadir'  # uncatalogged
#table = 'frames'  # catalogged



# SELECT elev FROM nadir WHERE mission='ISS045' AND roll='E' AND frame='   5586'

frames = photosDB.list_frames_since(table, mission, roll, firstFrame, minSunElev)

logging.debug("frames = %s", frames)
logging.debug(" ")
logging.debug("length of frames = %s", len(frames))

# open the output file to list the image names
fout = open(listName, 'w')

# For each frame found
for frame in frames:
    # construct the filename
    logging.debug("frame = %s", frame)
    imageName = mission + '-' + roll + '-' + frame[0].strip() + '.jpg'
    logging.debug("imageName = %s", imageName)

    # write image name out to file
    fout.write(imageName + '\n')

# close the file
fout.close()


# Print out the inputs
print ("input directory : {}".format(inDir))
print ("logLevel : {}".format(logLevel))
print ("input file : {}".format(listIN))
print ("outDirArg : {}".format(outDirArg))



# # Name of python code to run (don't change this) :
codeName = r'lightning_detection_nadir.py'
codeDir = r'./'
sys.argv = [codeName, inDir, logLevel, listIN, outDirArg]

# UNCOMMENT LATER WHEN LISTING FRAMES IS WORKING
try :
    # Run the test code to generate the macros
    execfile(codeDir+codeName)
except :
     print("couldn't run "+codeDir+codeName + " " + inDir + " " + logLevel + " " + listIN + " " + outDirArg)
     print("Unexpected error:", sys.exc_info()[0])
     raise
