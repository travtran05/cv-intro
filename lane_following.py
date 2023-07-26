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

    