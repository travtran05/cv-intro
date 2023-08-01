

'''

Created by Travis Tran on July 26, 2023
Problems 1 and 2 for simple computer vision

'''

import cv2
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
from dt_apriltags import Detector
import matplotlib.cm as cm
import math

global imgPixelHeight
imgPixelHeight = 1080

def crop_bottom_half(image):
    cropped_img = image[int(image.shape[0]/2):image.shape[0]]
    return cropped_img

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

    croppedImg = crop_bottom_half(img)
    lab= cv2.cvtColor(croppedImg, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    #result = np.hstack((blurred_image, enhanced_img))
    #plt.imshow(cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB))
    #plt.show()
    gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    
    
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) # detect edges
    #plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    #plt.show()
    #plt.imshow(cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))
    #plt.show()
    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #plt.show()
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
    lines = PutLinesDown(lines)
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
    halfScreen = imgPixelHeight/2
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 6)
    return img

def get_slopes_intercepts(lines):
    '''
    takes a list of lines as an input and returns a list of slopes and a list of intercepts

    parameters:
        lines: the list of lines to process
    
    '''

    resultSet = set() #stores the slope as the key, and the intercept as the data
    slopeList = []
    xInterceptList = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y1-y2)/(x1-x2)
        if slope == 0:
            slope = 0.001
        xIntercept = ((((imgPixelHeight - y1)/slope)  )+ x1)
        roundXIntercept = round(xIntercept, 0)
        if not roundXIntercept in resultSet:
            resultSet.add(roundXIntercept) 
            xInterceptList.append(xIntercept)
        #    resultSet[slope][1] += 1 # keep a counter of how many lines have been iterated through and added to the one slope for averaging later
            slopeList.append(slope) 

    
    # for result in resultSet:
    #     #result[0] = result[0]/result[1] # apply the dividing in the averaging
    #     xInterceptList.append(result)

    return slopeList, xInterceptList

    
  

    return slopeList, xInterceptList

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
                    #print(f"1/ slope:{slopeThing}")
                    xPoint = ((slopeList[i] * xInterceptList[i]) - (slopeList[j] * xInterceptList[j]))/(slopeList[i]-slopeList[j])
                    yPoint = slopeList[i]*(xPoint - xInterceptList[i]) + imgPixelHeight
                    
                    # avgSlope = (slopeList[i]+ slopeList[j])/2
                    # avgInterecept = (xInterceptList[i]+xInterceptList[j])/2
                    lane1 = [xInterceptList[i], imgPixelHeight, xPoint, yPoint]
                    lane2 = [xInterceptList[j], imgPixelHeight, xPoint, yPoint]
                    addedlanes = [lane1,lane2]
                    #print (f"thiasdfee:{(slopeList[i] * xInterceptList[i]) - slopeList[j] * xInterceptList[j]}")
                    lanes.append(addedlanes)


            #lanes.append(lane)

            #

            # if (yPoint> -500 and yPoint< 1080):
            #     avgInterceptX = (xInterceptList[i] + xInterceptList[j])/2
            #     lane = [xPoint.item(), avgInterceptX.item(), yPoint.item(), 1080.00]
            #     lanes.append(lane)

    return lanes

def draw_lanes(img,lanes,color = (255, 0, 0)):

    '''
    takes an image and a list of lanes as inputs and returns an image with the lanes drawn on it. Each lane should be a different color
    parameters:
        img: the image to process
        lanes: the list of lanes to draw

    '''

    for addedLanes in lanes:
        color = (randrange(255),randrange(255),randrange(255))
        for lane in addedLanes:
            
            x1, y1, x2, y2 = lane
       #     print ("type(x1)")
         #  print (lane)
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
    maxLaneFitness = -10000000000
    maxDiff = 0
    
    for addedLanes in lanes:
        center_slope_weight = 1000
        try:
            x1, y1, x2, y2 = addedLanes[0]
            slope1 = (y1-y2)/(x1-x2)
            x1, y1, x2, y2 = addedLanes[1]
            slope2 = (y1-y2)/(x1-x2)
            LineAngle = angle_between_lines(slope1, slope2)
            #print(f"I works")
            center_slope = abs((1/(((1/slope1)+(1/slope2))/2) )* center_slope_weight)
            
        except:
            center_slope = .0001
            LineAngle = .001
        diff = abs(addedLanes[0][0]  - addedLanes[1][0])
        yPoint = addedLanes[0][3]
        #print(f"yPoint:{yPoint}")
        VertDistToCenter = abs(yPoint - (imgPixelHeight/2))
        xPoint = addedLanes[0][2]
        HortDistToCenter = abs(xPoint - (1920/2))
        trueDistToCenter = np.sqrt(pow(VertDistToCenter,2)+pow(HortDistToCenter,2))
        #print (f"trueDistToCenter:{trueDistToCenter}")
        #print (f"diff:{diff}")
        #print (f"center_slope:{center_slope}")
        #laneFitness = diff - trueDistToCenter/2 + center_slope # calculate fitness, bigger = better, closer to center = better, lower centerline slope = better
        laneFitness = LineAngle * 10- VertDistToCenter #use lineangle as a analog for how close the lane is 
        print (laneFitness)
        
        if (maxLaneFitness < laneFitness and LineAngle < 50):
            maxLaneFitness = laneFitness
            pickedLane = addedLanes
            print (f"picked new lane! fitness: {laneFitness} <---------------------------------------")
    #print(f"picked: {pickedLane}")
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

def PutLinesDown(lines):
    screenThing = imgPixelHeight/2
    for line in lines:
        line[0][1] += screenThing
        line[0][3] += screenThing
    return lines