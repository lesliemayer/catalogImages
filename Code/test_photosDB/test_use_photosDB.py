""" Code for testing reading the photos database using the PHOTOSDB class
    written by lrmayer
    10/13/2016
"""

import logging

# for getting focal length from the photos database
from photosdb import PHOTOSDB

# set logging level
logging.basicConfig(level=logging.DEBUG)

#imageName = 'ISS028-E-26493.jpg'
imageName = 'ISS028-E-26366.jpg'

# initialize
xx = PHOTOSDB()

# get all the info about imageName
logging.debug("xx.getAll :")
allInfo = xx.getAll(imageName)

logging.info("info for %s %s ",imageName, allInfo)


# get the focal length
fl = xx.getField('fclt', imageName)
logging.info(" ")
logging.info("focal length for %s is %s ", imageName, fl)

# get the sun elevation
elev = xx.getField('elev', imageName)
logging.info(" ")
logging.info("sun elevation for %s is %s ", imageName, elev)

