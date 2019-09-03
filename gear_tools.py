import cv2

#ysed by CV2 b/c it is much faster then your python array or list or whatever they call now
import numpy as np

#mainly used to make plots, dont know why its here may use it later
from matplotlib import pyplot as plt
 
np.set_printoptions(threshold=np.inf)  

class tools: 
    def __init__(self, img, thresh, something): 
        self.something = something
        self.img = img
        self.thresh = thresh
        self.threshold = None
        self.num_of_teeth = None
    
    def color_to_thresh(self):
        #frame has been converted in gray scale needed for the cornerHarris function
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        ret, self.threshold = cv2.threshold(gray, self.thresh, 255, cv2.THRESH_BINARY)
        
    def find_teeth(self):
        contours, hierarchy =  cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
        if len(contours) < 2:
            self.num_of_teeth = 'None'
            cv2.putText(self.img, 'No Gear Detected', (40, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, cv2.LINE_AA )
            return
        
        max = 0
        for c in range(len(contours)):
            if(len(contours[max]) < len(contours[c]) and c != 0):
                max = c
        contours = contours[max]
        arc_length = cv2.arcLength(contours, True)
        curve = cv2.approxPolyDP(contours, self.something * arc_length, True)
        self.num_of_teeth = str(int(len(curve)/2))
        cv2.drawContours(self.img, curve, -1, (0, 255, 0), 3)
    
        looped = 0
        for c in curve:
            if(looped % 2 == 0):
                x_coordinate = c[0][0] 
                y_coordinate = c[0][1]  
                cv2.putText(self.img, str(int(looped / 2 + 1)), (x_coordinate, y_coordinate), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1, cv2.LINE_AA)    
            looped+=1   

