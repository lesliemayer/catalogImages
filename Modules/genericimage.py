# Show images if desired
#    if (showImages) :

import logging
import cv2
import os # to get the basename

from imutils import resize
from imageutils import plot_color_hist

class GENERICIMAGE:

    # function to translate an image in the x & y direction
    def __init__(self, imagePath):

        # get basename of image
        self.imageName = os.path.basename(imagePath)

        # load the image
        self.image = cv2.imread(imagePath)

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

