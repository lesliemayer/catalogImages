# Show images if desired
#    if (showImages) :

import logging
import cv2
import os # to get the basename
# for getting focal length from the photos database
from photosdb import PHOTOSDB
from imutils import resize
from imageutils import plot_color_hist

class ISSIMAGE:

    # function to translate an image in the x & y direction
    def __init__(self, imagePath):

        # get basename of image
        self.imageName = os.path.basename(imagePath)

        # load the image
        self.image = cv2.imread(imagePath)

        # initialize a connection to the photos database
        db = PHOTOSDB()

        # get the focal length & write on image
        self.fl = db.getField('fclt', self.imageName)

        # get the sun elevation
        self.elev = db.getField('elev', self.imageName)


    def show(self):

        # show the frame and the binary image
        #cv2.imshow(self.imageName, self.image)
        cv2.imshow("Image", self.image)

        return


    def put_text(self):

        # Add text w/ % of green pixels to the image

        # draw text string of the digit on the image a x-10,y-10
        # (above & to left of bounding box)
        # putText(img, text, textOrg, fontFace, fontScale,
        #        Scalar::all(255), thickness, 8);
        cv2.putText(self.image, 'fl: ' + str(self.fl), (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(self.image, 'elev: ' + str(self.elev), (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Display name of image on the image
        cv2.putText(self.image, str(self.imageName), (200, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return

    def resize(self, width=500):
        self.image = resize(self.image, width=width)
        return


    def plot_color_hist(self):
        logging.debug("plot_color_hist : Plotting color histogram")
        plot_color_hist(self.image)
        return

    # ---------------------------------------
    # Return the sun elevation of the image
    # ---------------------------------------
    def get_sun_elev(self):
        return self.elev

    # ---------------------------------------
    # Return the focal length of the image
    # ---------------------------------------
    def get_focal_length(self):
        return self.fl