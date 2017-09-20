"""Automatically run the lightning_detection code"""

import sys

# Example of how to run the lightning_detection code
# python lightning_detection.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"

# add codeDir to python path (do this so it finds the code)
#sys.path.append(codeDir)


# Where input images are
# inDir = r"E:\BetterLightning"
# inDir = r"\\EO-Web\images\ESC\large\ISS030/"
inDir = r"\\EO-Web\images\ESC\large\ISS050/"
#inDir = r"\\EO-Web\images\ESC\large\ISS051/"

# List of input images
# listIN = r'--list=E:\BetterLightning\testlightning.txt'
# listIN = r'--list=E:\NadirLightning/nadirlightimages.txt'
listIN = r'--list=E:/iss050/iss050_images.txt'
# listIN = r'--list=E:/LightningSequences/ISS030_nadir_lightning_seq.txt'
#listIN = r'--list=E:\ISS050\nadir_images.txt'
#listIN = r'--list=E:\ISS051\test_images.txt'


# output directory
# outDir = r'--out=E:\BetterLightning\minThresh100Dilate/'
# outDir = r'--out=E:\NadirLightning/Results/'
# outDir = r'--out=E:\ISS030/LightningSequences/'
# outDir = r'--out=E:\ISS050\NadirResultsNoShape'
#outDir = r'--out=E:\ISS050\NadirResults/LargeMinArea/'
outDir = r'--out=E:\ISS050\NadirLargeArea/'

#outDir = r'--out=E:\ISS050\NadirCheckAllColor'
# outDir = r'--out=E:\ISS050\NadirSumAllColors'
# outDir = r'--out=E:\ISS050\SumAllColors'
# outDir = r'--out=E:\ISS050\SumInertiaBrightWhite'
# outDir = r'--out=E:\ISS050\SumWhiteBluePurple'
# output directory
#outDir = r'--out=E:\ISS051\NadirResults/testLargeMinArea/'


# logging level
logLevel = r'--log=debug'
#logLevel = r'--log=info'

# Print out the inputs
print ("input directory : {}".format(inDir))
print ("logLevel : {}".format(logLevel))
print ("input file : {}".format(listIN))
print ("outDir : {}".format(outDir))


# # Name of python code to run (don't change this) :
codeName = r'lightning_detection_nadir.py'
codeDir = r'./'
sys.argv = [codeName, inDir, logLevel, listIN, outDir]


try :
    # Run the test code to generate the macros
    execfile(codeDir+codeName)
except :
     print("couldn't run "+codeDir+codeName + " " + inDir + " " + logLevel + " " + listIN + " " + outDir)
     print("Unexpected error:", sys.exc_info()[0])
     raise
