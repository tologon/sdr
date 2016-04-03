# ------------------------------------------------------------------------------
# Author:   Tologon Eshimkanov (https://github.com/tologon)
# Course:   COMP 3770-01 - Introduction to Artificial Intelligence
# School:   Wentworth Institute of Technology
# Project:  Image Text Recognition
# ------------------------------------------------------------------------------

# required package(s)
import cv2

def aspectRatio(convexHull):
    """
    Aspect ratio is the ratio of width to height.
        width / height = aspect ratio
    A convex hull is not a shape from which values can be easily extracted.
    Therefore, a convex hull is transformed into a bounding rectangle,
    from which its width and height are derived.
    """
    x, y, w, h = cv2.boundingRect(convexHull)
    return float(w) / h

def extent(convexHull):
    """
    Extent is the ratio of contour area to bounding rectangle area.
    """
    area = cv2.contourArea(convexHull)
    x, y, w, h = cv2.boundingRect(convexHull)
    rectArea = w * h
    return float(area) / rectArea

def solidity(convexHull):
    """
    Solidity is the ratio of contour area to its convex hull area.
    """
    area = cv2.contourArea(convexHull)
    hullArea = cv2.contourArea(convexHull)
    return float(area) / hullArea