'''

Created by Travis Tran on July 26, 2023
Problems 1 and 2 for simple computer vision

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_lines(img, threshold1 = 50, threshold2 = 150, apertureSize = 3, minLineLength = 100, maxLineGap = 10):
    '''
    
    takes an image as an input and returns a list of detected lines
    
    parameters:
        img: the image to process
        threshold1: the first threshold for the Canny edge detector (default: 50)
        threshold2: the second threshold for the Canny edge detector (default: 150)
        apertureSize: the aperture size for the Sobel operator (default: 3)
        minLineLength: the minimum length of a line (default: 100)
        maxLineGap: the maximum gap between two points to be considered in the same line (default: 10)
    
    '''


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize = apertureSize) # detect edges, gray is image in grayscale, 50 and 150 represent 2 images that have been 
                                                      # threshholded at 2 different levels, apertureSize controls how much light the image gets and how exposed it is
    lines = cv2.HoughLinesP(
                    edges, #described above
                    rho = 1, #1 pixel resolution parameter
                    theta = np.pi/180, # 1 degree resolution parameter
                    threshold = 125, #min number of intersections/votes
                    minLineLength = minLineLength,
                    maxLineGap = maxLineGap,
            ) # detect lines


    return lines

def draw_lines(img, lines, color = (0,255,0)):
    '''
    takes an image and a list of lines as inputs and returns an image with the lines drawn on it

    parameters:
        img: the image to process
        lines: the list of lines to draw
        color: the color of the lines (default: (0, 255, 0))
    
    '''
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), color, 2)
    except TypeError:
        pass
    return img

def get_slopes_intercepts(lines):
    '''
    takes a list of lines as an input and returns a list of slopes and a list of intercepts

    parameters:
        lines: the list of lines to process
    
    '''

    slopes = []
    intercepts = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2-y1)/(x2-x1)
        slopes.append(slope)
        intercept = y1-slope*x1
        intercepts.append(intercept)

    return slopes, intercepts

def detect_lanes(lines):

    '''
    takes a list of lines as an input and returns a list of lanes

    parameters:
        lines: the list of lines to process
    
    '''

    slopeList, xInterceptList = get_slopes_intercepts(lines)
  
    lanes = []
    if len(slopeList)> 1:
        for i in range(0,len(slopeList)):
            for j in range (i+1,len(slopeList)):
                if(abs(xInterceptList[i]-xInterceptList[j])< 500):
                    xPoint = ((slopeList[i] * xInterceptList[i]) - (slopeList[j] * xInterceptList[j]))/(slopeList[i]-slopeList[j])
                    yPoint = slopeList[i]*(xPoint - xInterceptList[i]) + 1080
                    lane1 = [xInterceptList[i], 1080, xPoint,yPoint]
                    lane2 = [xInterceptList[j], 1080, xPoint,yPoint]
                    addedlanes = [lane1,lane2]
                    lanes.append(addedlanes)

    return lanes

def draw_lanes(img,lanes,color = (255, 0, 0)):

    '''
    takes an image and a list of lanes as inputs and returns an image with the lanes drawn on it. Each lane should be a different color
    parameters:
        img: the image to process
        lanes: the list of lanes to draw

    '''

    for addedLanes in lanes:
        for lane in addedLanes:
            x1, y1, x2, y2 = lane
            print ("type(x1)")
            print (lane)
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 6)
    return img