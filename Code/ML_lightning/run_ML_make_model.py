"""Python code to run ML_make_model.py
   @author: L.R. Mayer
"""


import sys

# Example of how to run the lightning_detection code
# python lightning_detection.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"

# add codeDir to python path (do this so it finds the code)
#sys.path.append(codeDir)

# usage python ML_make_model.py E:\ISS050 E:\ML_Lightning\nadir_lightning.txt E:\ML_Lightning\nadir_lightning E:\ML_Lightning\non_nadir_lightning.txt --log info --model ../Models/nadir_lightning/ --forest


# Where nadir lightning input images are
pDir = r"E:\ML_Lightning\nadir_lightning"

# List of postive input images
pList = r'E:\ML_Lightning\nadir_lightning.txt'

# Where nadir lightning input images are
nDir = r"\\EO-Web\images\ESC\large\ISS050"

# List of negaive input images
nList = r'E:\ML_Lightning\non_nadir_lightning.txt'


# logging level
logLevel = r'--log=debug'
#logLevel = r'--log=info'


# output model name
#model = r"--model=../../Models/nadir_lightning"
model = r"--model=C:\Users/lrmayer/My Documents/Mayer/CatalogImages/Models/LightningModel"


# whether to use forest classifier
forest = r"--forest"


# Print out the inputs
print ("positive input directory : {}".format(pDir))
print ("positive file list : {}".format(pList))
print ("negative input directory : {}".format(nDir))
print ("negative file list : {}".format(nList))

print ("logLevel : {}".format(logLevel))
print ("model : {}".format(model))
print ("forest ? : {}".format(forest))


# # Name of python code to run (don't change this) :
codeName = r'ML_make_model.py'
codeDir = r'./'
sys.argv = [codeName, pDir, pList, nDir, nList, logLevel, model, forest]


try :
    # Run the test code to generate the macros
    execfile(codeDir+codeName)
except :
     print("Unexpected error:", sys.exc_info()[0])
     #print("couldn't run "+codeDir+codeName + " " + pDir + " " + pList + " " + nDir + " "  + nList + " " + logLevel + " " + model + " " + forest)
     raise
