import cv2 as cv
import numpy as np
import math
import sys
 
#prints the entire np array 
np.set_printoptions(threshold=np.inf)  

class Gear: 
    """
    The Gear object contains many methods that can help filter out a gear and its properties from a frame

    Attributes:
        frame: The frame or image of the gear
        result: The frame or image that contains the result
        thresh: Effects how the threshold is calculated
        dilate: How many time the frame will be dilated
        background_width: The width of the frame in inches
        num_of_teeth: Keeps track of the number of teeth of the gear
        diameter: Keeps track of the diameter of the gear   
    """
    def __init__(self, frame, thresh, dilate, background_width):
        """
        The constructor for the Gear class
        
        Parameters:
            frame: The frame or image of the gear
            thresh: Effects how the threshold is calculated
            dilate: How many time the frame will be dilated
            background_width: The width of the frame in inches
        """
        self.frame = frame
        self.result = np.array(frame, copy=True)
        if thresh%2 == 0:
            self.thresh = int(thresh)+1
        else:
            self.thresh = int(thresh)
        self.iterations = int(dilate)
        self.background_width = background_width
        self.num_of_teeth = 0
        self.diameter = None
    
    def remove_shadow(self):
        """Removes the shadow in the frame"""
        #Separate the RGB
        rgb_planes = cv.split(self.frame)

        result_norm_planes = []
        #Go through the planes, get a dilated image and a blur image, then get the difference between the two images, then normalize the final image
        for plane in rgb_planes:
            dilated_img = cv.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv.medianBlur(dilated_img, 21)
            diff_img = 255 - cv.absdiff(plane, bg_img)
            norm_img = cv.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
            result_norm_planes.append(norm_img)

        result_norm = cv.merge(result_norm_planes)

        self.frame = result_norm

    def grayscale(self):
        """Converts the frame to grayscale"""
        self.frame = cv.cvtColor(self.frame, cv.COLOR_RGB2GRAY)

    def blur(self):
        """Blurs the frame"""
        self.frame = cv.medianBlur(self.frame, 5)
    
    def remove_noise(self):
        """Remove any noise from the frame"""
        kernel = np.ones((5, 5), np.uint8)
        self.frame = cv.morphologyEx(self.frame, cv.MORPH_CLOSE, kernel)
        self.frame = cv.morphologyEx(self.frame, cv.MORPH_OPEN, kernel)

    def dilate(self):
        """Dilates the frame"""
        kernel = np.ones((3, 3), np.uint8)
        self.frame = cv.dilate(self.frame, kernel, iterations = self.iterations)
    
    def canny_edge(self):
        """Outlines the gear's edges in the frame"""
        self.frame = cv.Canny(self.frame, 100, 200)        

    def threshold(self):
        """Get the binary threshold of the frame, such that the frame is now black and white"""
        self.frame = cv.adaptiveThreshold(self.frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, self.thresh, 2)

    def find_teeth(self):
        """Find the number of teeth of the gear in the frame"""
        try:
            #Get the contours of the gear
            contours, hierarchy =  cv.findContours(self.frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

            #Get the outermost contour
            cnt = contours[0]
            cnt_index = 0
            for i, c in enumerate(hierarchy[0]):
                if c[3] != 0 or c[3] != 1:
                    continue
                if len(cnt) < len(contours[i]):
                    cnt = contours[i]
                    cnt_index = i

            #Draw the outermost contour to the result
            cv.drawContours(self.result, contours, cnt_index, (255, 0, 0), 2)

            #Gets any deviations from the curve around the gear
            hull = cv.convexHull(cnt, returnPoints=False)
            defects = cv.convexityDefects(cnt, hull)

            #Draw the defects onto the result 
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
    
                cv.line(self.result, start, end, [0, 0, 255], 2)
                if np.array_equal(self.result[far[1], far[0]], np.array([0, 0, 255])):
                    continue
                
                cv.circle(self.result, far, 4, [0, 0, 255], -1)
                self.num_of_teeth += 1
            
        except:
            cv.putText(self.result, 'Error', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv.LINE_AA)
    
    def find_diameter(self):
        """Gets the diameter of the gear in the frame"""
        try:
            #Get the contours of the gear
            contours, hierarchy =  cv.findContours(self.frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
            
            #Get the leftmost and the rightmost point of the gear
            leftmost = (sys.maxsize, sys.maxsize)
            rightmost = (sys.maxsize*-1, sys.maxsize*-1)
            frame_area = self.frame.shape[0] * self.frame.shape[1]
            new_contours = []
            for c in contours:
                c_area = cv.contourArea(c)
                area_percentage = (c_area/frame_area) * 100
                if area_percentage > .01:
                    new_contours.append(c)

                    c_leftmost = tuple(c[c[:, :, 0].argmin()][0])
                    if leftmost[0] > c_leftmost[0]:
                        leftmost = c_leftmost

                    c_rightmost = tuple(c[c[:, :, 0].argmax()][0])
                    if rightmost[0] < c_rightmost[0]:
                        rightmost = c_rightmost

            cv.drawContours(self.result, new_contours, -1, (255, 0, 0), 3)

            cv.circle(self.result, leftmost, 4, [0, 0, 255], -1)
            cv.circle(self.result, rightmost, 4, [0, 0, 255], -1)

            #Get the distance between the two points
            distance = math.sqrt((leftmost[0] - rightmost[0])**2 + (leftmost[1] - rightmost[1])**2)

            #Convert the distance, which is in pixels to inches by using the background width as a point of reference
            self.diameter = (distance/self.frame.shape[1]) * self.background_width
            self.diameter = round(self.diameter, 2)
        
        except:
            cv.putText(self.result, 'Error', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv.LINE_AA)

