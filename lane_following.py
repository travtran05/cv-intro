'''

Created by Travis Tran on July 26, 2023
Problems 1 and 2 for simple computer vision

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import lane_detection

def get_lane_center(lanes):
    '''
    takes a list of lanes as an input and returns the center of the closest lane and its slope

    parameters:
        lanes: the list of lanes to process

    
    '''
    center = (lanes[0][0]+lanes[1][0])/2
    x1, y1, x2, y2 = lanes[0]
    slope1 = (y1-y2)/(x1-x2)
    x1, y1, x2, y2 = lanes[1]
    slope2 = (y1-y2)/(x1-x2)
    slope = (slope1+slope2)/2

    

    return center, slope


def recommend_direction(center, slope):
    '''
    takes the center of the closest lane and its slope as inputs and returns a direction


    parameters:
        center: the center of the closest lane
        slope: the slope of the closest lane
    
    
    '''

    halfOfRes = 4096/2
    if center == halfOfRes:
        direction = "forward"
    elif center > halfOfRes: # more than halfway
        print("strafe right")
        direction = "right"
    else:
        print("strafe left")
        direction = "left"
    if 1/slope > 0:
        print("turn right")
    if 1/slope < 0:
        print("turn Left")
    return direction