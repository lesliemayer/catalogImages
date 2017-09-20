# python code jpgutils.py
#
# utilities for working w/ jpg images
# 10/13/2016
#

import piexif



# function to translate an image in the x & y direction
def getFocalLength(imageName):
    # Return exif data as dictionary
    exif_dict = piexif.load(imageName)

    length = ""

    # print out the focal length if it's there :
    if piexif.ExifIFD.FocalLength in exif_dict["Exif"]:
        length = exif_dict["Exif"][piexif.ExifIFD.FocalLength]
        print("Focal Length is ", length)


    return length

