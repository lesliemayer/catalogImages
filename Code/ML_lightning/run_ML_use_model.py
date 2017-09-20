"""Python code to run ML_use_model.py
   @author: L.R. Mayer
"""

import sys

# Example of how to run the lightning_detection code
# python lightning_detection.py E:\Lightning --log=debug --list="E:\Lightning\lightning.txt" --out="E:\Lightning\Blobs"

# usage python ML_make_model.py E:\ISS050 E:\ML_Lightning\nadir_lightning.txt E:\ML_Lightning\nadir_lightning E:\ML_Lightning\non_nadir_lightning.txt --log info --model ../Models/nadir_lightning/ --forest

# Where nadir lightning input images are
#testDir = r"\\EO-Web\images\ESC\large\ISS049"
testDir = r"\\EO-Web\images\ESC\large\ISS050"

# List of input images to classify
#testList = r'E:\ML_Lightning\ISS049.txt'
testList = r'E:\NadirLightning\nadirtest.txt'

# output model name
model = r"C:\Users/lrmayer/My Documents/Mayer/CatalogImages/Models/LightningModel/nadir_lightning_RFC.pickle"


# where results should go
results = r'--results=E:\NadirLightning\NadirTest_results'


# logging level
logLevel = r'--log=debug'
#logLevel = r'--log=info'




# Print out the inputs
print ("test input directory : {}".format(testDir))
print ("test file list : {}".format(testList))


print ("logLevel : {}".format(logLevel))
print ("model : {}".format(model))


# # Name of python code to run (don't change this) :
codeName = r'ML_use_model.py'
codeDir = r'./'
sys.argv = [codeName, testDir, testList, model, logLevel, results]
#sys.argv = [codeName, testDir, model, logLevel, results]


try :
    # Run the test code to generate the macros
    execfile(codeDir+codeName)
except :
     print("could not run "+codeDir+codeName + " " + testDir + " " + testList + " " + str(logLevel) + " " + str(model))
     print("Unexpected error:", sys.exc_info()[0])
     raise
