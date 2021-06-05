import cv2
import numpy as np
import math
 
#prints the whole entire np array 
np.set_printoptions(threshold=np.inf)  

class Gear: 
    def __init__(self, img, thresh, parameter): 
        self.img = img
        self.thresh = thresh
        self.threshold = None
        self.cnt = None
        self.parameter = parameter
        self.num_of_teeth = None
        self.diameter = None
    
    def color_to_thresh(self):
        #frame has been converted to black and white needed for finding the contour
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        ret, self.threshold = cv2.threshold(gray, self.thresh, 255, cv2.THRESH_BINARY)
    
    def find_contour(self):
        contours, hierarchy =  cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours) < 2:
            print('Error: No Gears Detected')
            exit()
    
        #finds the largest contour which is the one around the gear and draws it on the image
        #https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html explains functions used below in detail
        max = 0
        for cnt in range(len(contours)):
            if len(contours[max]) < len(contours[cnt]) and cnt != 0:
                max = cnt
        self.cnt = contours[max]
        
    def find_products(self):
        epsilon = cv2.arcLength(self.cnt, True)
        approx  = cv2.approxPolyDP(self.cnt, self.parameter * epsilon, True)
        
        self.num_of_teeth = str(int(len(approx)/2))
        cv2.drawContours(self.img, approx, -1, (0, 0, 255), 3)

        looped = 0
        for point in approx:
            #numbers the gear's teeth makes it easily to find an error
            if(looped % 2 == 0):
                x_coordinate = point[0][0] 
                y_coordinate = point[0][1]  
                cv2.putText(self.img, str(int(looped / 2 + 1)), (x_coordinate, y_coordinate), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)  
           
            #find the numbers needed for the distance formula
            if(looped == 0):
                    first_coordinate_x = point[0][0]
                    first_coordinate_y = point[0][1]
            elif(looped == int(self.num_of_teeth)):
                    second_coordinate_x = point[0][0]
                    second_coordinate_y = point[0][1]
                      
            looped+=1 

        frame_width = 5
        frame_width_pxl = self.img.shape[1]
        diameter_pxl = math.sqrt((first_coordinate_x - second_coordinate_x)**2 + (first_coordinate_y - second_coordinate_y)**2)     

        self.diameter = str(round((frame_width * diameter_pxl) / frame_width_pxl, 2))