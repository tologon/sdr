# ------------------------------------------------------------------------------
# Author:   Tologon Eshimkanov (https://github.com/tologon)
# Course:   COMP 3770-01 - Introduction to Artificial Intelligence
# School:   Wentworth Institute of Technology
# Project:  Image Text Recognition
# ------------------------------------------------------------------------------

# required package(s)
import sys, cv2
import numpy as np

from properties import aspectRatio, extent, solidity

# ignore sys.argv[0] as it is a name of an invoked Python script
# print 'Number of arguments:', len(sys.argv[1:]), 'arguments.'
# print 'Argument list:', str(sys.argv[1:])

# constants
DEFAULT_SINGLE_DIGIT = 'default_single_digit.png'
RESULT_TYPE = 'curve'
DEFAULT_COLOR = (0, 255, 0) # RGB values; doesn't matter on grayscale
ASPECT_RATIO_THRESHOLD = 0.29
LOW_EXTENT_THRESHOLD = 0.3
HIGH_EXTENT_THRESHOLD = 0.59
SOLIDITY_THRESHOLD = 1.1

class Pipeline:
    """
    The pipeline takes an image as input and detects
    any present digits with some degree of accuracy.
    """

    def __init__(self, image = DEFAULT_SINGLE_DIGIT):
        """ Reads and stores an image for future processing. """
        # possible options for image reading:
        # cv2.IMREAD_COLOR      : Loads a color image (default)
        # cv2.IMREAD_GRAYSCALE  : Loads image in grayscale mode
        # cv2.IMREAD_UNCHANGED  : Loads image as such including alpha channel

        # add check for image existence on a given path
        self.image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    def detectRegions(self):
        """
        Detects MSER regions and subsequently converting
        those regions into convex hulls, rectangles, and contours.
        """
        mser = cv2.MSER_create()
        bboxes = None # no documentation available
        self.regions = mser.detectRegions(self.image, bboxes)
        self.hulls = self.regionsToHulls() # hulls == convex hulls
        self.rectangles = self.regionsToRectangles()
        self.contours = self.regionsToContours()

    def regionsToHulls(self):
        """ Converts present MSER regions into convex hulls. """
        return [ cv2.convexHull( r.reshape(-1, 1, 2) ) for r in self.regions ]

    def regionsToRectangles(self):
        """ Converts present MSER regions into rectangles. """
        return [ cv2.boundingRect(region) for region in self.regions ]

    def regionsToContours(self):
        """ Converts present MSER regions into contours. """
        closed = True
        contours = []
        for region in self.regions:
            epsilon = 0.01 * cv2.arcLength(region, True)
            contours.append( cv2.approxPolyDP(region, epsilon, closed) )
        return contours

    # TODO: refactor resultType into something more sensible (w/o user input)
    def drawResults(self, results, resultType = RESULT_TYPE):
        """ Draws given results on the original image. """
        imageCopy = self.image.copy()
        isClosed = 1 # no documentation available
        if resultType == 'curve':
            cv2.polylines(imageCopy, results, isClosed, DEFAULT_COLOR)
        elif resultType == 'straight':
            self.drawRectangles(imageCopy, results)
        cv2.imshow('Results', imageCopy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def drawRectangles(self, image, rectangles):
        """ Draws rectangles on the image. """
        for rectangle in rectangles:
            x, y, w, h = rectangle
            topLeftCorner = (x, y)
            bottomRightCorner = (x + w, y + h)
            # print "top left corner: {} | bottom right corner: {}".format(topLeftCorner, bottomRightCorner)
            cv2.rectangle(image, topLeftCorner, bottomRightCorner, DEFAULT_COLOR)

    def filterByGeoProps(self, properties = []):
        """
        Filters out convex hulls of an image by given geometric properties.
        """
        for prop in properties:
            filterByProperty = getattr(self, 'filterBy' + prop)
            filterByProperty()

    def filterByAspectRatio(self):
        """ Filters out convex hulls of an image by aspect ratio. """
        self.hulls = [hull for hull in self.hulls if aspectRatio(hull) > ASPECT_RATIO_THRESHOLD]

    def filterByExtent(self):
        """ Filters out convex hulls of an image by extent. """
        self.hulls = [hull for hull in self.hulls if extent(hull) < LOW_EXTENT_THRESHOLD or extent(hull) > HIGH_EXTENT_THRESHOLD]

    def filterBySolidity(self):
        """ Filters out convex hulls of an image by solidity. """
        self.hulls = [hull for hull in self.hulls if solidity(hull) < SOLIDITY_THRESHOLD]

if __name__ == "__main__":
    image, pipeline = None, None
    if len(sys.argv) > 1:
        image = str(sys.argv[1])
        pipeline = Pipeline(image)
    else:
        pipeline = Pipeline()
    pipeline.detectRegions()

    print "original hulls: {}".format( len(pipeline.hulls) )

    # pipeline.drawResults( pipeline.hulls, 'curve' )
    # pipeline.drawResults( pipeline.contours, 'curve' )
    pipeline.drawResults( pipeline.rectangles, 'straight' )

    properties = ['AspectRatio', 'Extent', 'Solidity']
    pipeline.filterByGeoProps(properties)
    print "after filtering by geometric properties, hulls: {}".format( len(pipeline.hulls) )

    pipeline.drawResults( pipeline.rectangles, 'straight' )
