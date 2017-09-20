# Python class to make a list if file

import sys
import os # to check list file existence
from imutils import paths  # to get list of files in a path
import logging #  To write messages to a logfile

# Function (defined outside of the class) to get basename of a file
# minus the 4 chararcter extension (ex., .png)
def get_filename(fullpath):
    # Get the basename, ex.  Iss_23849.jpg
    baseName = os.path.basename(fullpath)

    # Remove extension
    name = baseName[:-4]

    return name

class FileList:

    def __init__(self, dataset, list):
        self.list = list  # the directory or filename that includes list of files
        self.dataset = dataset
        self.filenames = []  # empty list

        logging.debug("FileList : __init__ : list = %s", list)

    def getPathFilenames(self):
        if (self.list) :  # check to see if file list argument exists

            if os.path.isfile(self.list):
                with open(self.list) as f:
                    fileList = []  # initialize fileList
                    for line in f:
                        fileList.append(line.strip())  # strip off newline, spaces, and append

                logging.debug("fileList = %s",fileList)
                imagePaths = [self.dataset + '/' + i for i in fileList]

            else :
                sys.exit("list file does not exist")

        else :

            # -----------------------------------------------------------
            # Grab the image path & filenames from the dataset directory
            # -----------------------------------------------------------
            #imagePaths = list(paths.list_images(args.dataset))
            imagePaths = list(paths.list_images(self.dataset))

            imagePaths = sorted(imagePaths)

        #logging.debug("imagePaths = %s", imagePaths)
        logging.debug("imagePaths = %s", '\n'.join(imagePaths))

        return imagePaths





