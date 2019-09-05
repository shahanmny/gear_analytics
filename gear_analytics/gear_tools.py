import cv2
import numpy as np
 
#prints the whole entire np array 
np.set_printoptions(threshold=np.inf)  

class tools: 
    def __init__(self, img, thresh, parameter): 
        self.img = img
        self.thresh = thresh
        self.threshold = None
        self.parameter = parameter
        self.num_of_teeth = None
    
    def color_to_thresh(self):
        #frame has been converted to black and white needed for finding the contour
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        ret, self.threshold = cv2.threshold(gray, self.thresh, 255, cv2.THRESH_BINARY)
        
    def find_teeth(self):
        contours, hierarchy =  cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(contours) < 2:
            self.num_of_teeth = 'None'
            cv2.putText(self.img, 'No Gear Detected', (40, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, cv2.LINE_AA )
            return
        
        #finds the largest contour which is the one around the gear and draws it on the image
        #https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html explains functions used below in detail
        max = 0
        for cnt in range(len(contours)):
            if len(contours[max]) < len(contours[cnt]) and cnt != 0:
                max = cnt
        cnt = contours[max]
        epsilon = cv2.arcLength(cnt, True)
        approx  = cv2.approxPolyDP(cnt, self.parameter * epsilon, True)
        self.num_of_teeth = str(int(len(approx)/2))
        cv2.drawContours(self.img, approx, -1, (0, 255, 0), 3)

        #numbers the gear's teeth makes it easily to find an error
        looped = 0
        for point in approx:
            if(looped % 2 == 0):
                x_coordinate = point[0][0] 
                y_coordinate = point[0][1]  
                cv2.putText(self.img, str(int(looped / 2 + 1)), (x_coordinate, y_coordinate), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1, cv2.LINE_AA)    
            looped+=1   

