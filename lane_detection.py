

'''

Created by Travis Tran on July 26, 2023
Problems 1 and 2 for simple computer vision

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import math 

def detect_lines(img,threshold1 = 50,threshold2 = 150,apertureSize = 3,minLineLength=100,maxLineGap=10):

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
    blurred_image = cv2.GaussianBlur(gray, (9, 9), 0)
    #plt.imshow(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB))
    #plt.show()
    edges = cv2.Canny(blurred_image, threshold1, threshold2, apertureSize) # detect edges
    lines = cv2.HoughLinesP(
            edges,
            rho = 1,
            theta = np.pi/180,
            threshold = 100,
            minLineLength = minLineLength,
            maxLineGap = maxLineGap,


    )
    #plt.imshow(cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))
    #plt.show()
    #print (lines)
    #be close enough, have similar slopes, be on the same side of the image
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
        try:
            slope = (y2-y1)/(x2-x1)
        except ZeroDivisionError or RuntimeWarning:
            continue
        slopes.append(slope)
        try:
            intercept = ((((1080 - y1)/slope)  )+ x1)
        except ZeroDivisionError or RuntimeWarning:
            continue
        intercepts.append(intercept)
        
        

    return slopes, intercepts

def detect_lanes(lines):
    slopeList, xInterceptList = get_slopes_intercepts(lines)
    #print (f"slopeList:{slopeList}")
    #print (f"xInterceptList:{xInterceptList}")
    lanes = []
    #check of the lines intersect on the screen
    if len(slopeList)> 1:
        for i in range(0,len(slopeList)):
            # if (len(slopeList) > 1):
            #     i += 1
            #     print("added i")
            for j in range (i+1,len(slopeList)):
                
                InterceptDist = abs(xInterceptList[i]-xInterceptList[j])
                if slopeList[i] == 0 or slopeList[j == 0]:
                    slopeDiff = 0
                else:
                    slopeDiff = abs(1/ slopeList[i]-1 /slopeList[j])
                slopeThing = 1000000
                if  not slopeList[i] == 0:
                    slopeThing = 1/slopeList[i]
                #print(f"DistREQ:{abs(xInterceptList[i]-xInterceptList[j])}")
                #print(f"slopeREQ:{abs(1/ slopeList[i]-1 /slopeList[j])}")
                # if statement to make sure lane is not too big (multiple lanes as one) not too different in slope (wrong side/ different lanes) and not too horizontal (other lienes reced as pool lane)
                if(InterceptDist > 100 and InterceptDist< 750 and slopeDiff< 1 and abs(slopeThing) < 3 ):
                    print(f"1/ slope:{slopeThing}")
                    xPoint = ((slopeList[i] * xInterceptList[i]) - (slopeList[j] * xInterceptList[j]))/(slopeList[i]-slopeList[j])
                    yPoint = slopeList[i]*(xPoint - xInterceptList[i]) + 1080
                    
                    # avgSlope = (slopeList[i]+ slopeList[j])/2
                    # avgInterecept = (xInterceptList[i]+xInterceptList[j])/2
                    lane1 = [xInterceptList[i], 1080, xPoint, yPoint]
                    lane2 = [xInterceptList[j], 1080, xPoint, yPoint]
                    addedlanes = [lane1,lane2]
                    #print (f"thiasdfee:{(slopeList[i] * xInterceptList[i]) - slopeList[j] * xInterceptList[j]}")
                    lanes.append(addedlanes)
            #     lanes.append(lane)

    return lanes

def draw_lanes(img,lanes,color = (255, 0, 0)):

    '''
    takes an image and a list of lanes as inputs and returns an image with the lanes drawn on it. Each lane should be a different color
    parameters:
        img: the image to process
        lanes: the list of lanes to draw

    '''

    for lane in lanes:
        for line in lane:
            x1, y1, x2, y2 = line
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 6)
    return img

def draw_Single_lane(img,lanes,color = (255, 0, 0)):
    #color = (randrange(255),randrange(255),randrange(255))
    for lane in lanes:
        
        x1, y1, x2, y2 = lane
    # print ("type(x1)")
    #  print (lane)
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 6)
    return img

def pick_lane(lanes):
    maxDiff = 0
    for addedLanes in lanes:
        diff = abs(addedLanes[0][0]  - addedLanes[1][0])
        if (maxDiff < diff):
            maxDiff = diff
            pickedLane = addedLanes
    
    return pickedLane

def angle_between_lines(m1, m2):
    """
    Calculate the angle between two lines given their slopes.
    :param m1: Slope of line 1
    :param m2: Slope of line 2
    :return: Angle between the two lines in degrees
    """
    tan_theta = abs((m2 - m1) / (1 + m1 * m2))
    theta = math.atan(tan_theta)
    return math.degrees(theta)