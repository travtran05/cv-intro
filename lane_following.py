'''

Created by Travis Tran on July 26, 2023
Problems 1 and 2 for simple computer vision

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import lane_detection


def pick_lane(lanes):
    '''
    helper function for get_lane_center
    finds the closet lane from a list of lanes
    
    '''

    maxDiff = 0
    for addedLanes in lanes:
        diff = abs(addedLanes[0][0]  - addedLanes[1][0])
        if (maxDiff < diff):
            maxDiff = diff
            pickedLane = addedLanes
    
    return pickedLane


def get_lane_center(lanes):
    '''
    takes a list of lanes as an input and returns the center of the closest lane and its slope

    parameters:
        lanes: the list of lanes to process

    
    '''

    center_intercept = (lanes[0][0]+lanes[1][0])/2
    x1, y1, x2, y2 = lanes[0]
    slope1 = (y1-y2)/(x1-x2)
    x1, y1, x2, y2 = lanes[1]
    slope2 = (y1-y2)/(x1-x2)
    center_slope = 1/(((1/slope1)+(1/slope2))/2)
    center_intercept = ((((1080 - y2)/center_slope)  )+ x2)
    return center_intercept, center_slope

def draw_center_lane(img, center_intercept, center_slope, xPoint = 0, yPoint = 0):
    global imgPixelHeight 
    imgPixelHeight  = img.shape[0]
    cv2.line(img, (int(center_intercept), imgPixelHeight), (int(xPoint), int(yPoint)), (0,0,255), 6)
    return img


def recommend_direction(center, slope):
    '''
    takes the center of the closest lane and its slope as inputs and returns a direction


    parameters:
        center: the center of the closest lane
        slope: the slope of the closest lane
    
    
    '''

    halfOfRes = 1920/2
    HorizontalDiff = halfOfRes-center
    centerTolerance = 2.5
    if abs(HorizontalDiff) < centerTolerance:
        direction = "Go Forward!"
    elif HorizontalDiff > 0:# more than halfway
        #print("strafe right")
        direction = f"Strafe Left by {HorizontalDiff}"
    else:
        #print("strafe left")
        direction = f"Strafe Right by {HorizontalDiff}"

    AproxAUVAngle = 90 - angle_between_lines(slope, 0)  
    # get the approx angle of the auv with the line by calculating the slope of the 
    #center line with a horizontal line relative to the rov
    if slope > 0:
        AproxAUVAngle = -AproxAUVAngle
        direction += f" turn Left by: {AproxAUVAngle} degrees"
        pass#print("turn right")
    if slope < 0:
        direction += f" turn Right by: {AproxAUVAngle} degrees"
        pass#print("turn Left")
    return direction