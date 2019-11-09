#gui library
import PySimpleGUI as sg

#computer vision library
import cv2

from gear_analytics.gear_tools import tools
from gear_analytics.settings_gui import settingsGui

class gui:
    def __init__(self):
        self.cap = None
    
    #looks through each device index to find a camera
    def find_cam(self):  
            working_device = None

            for index in range(100):
                
                #index 0 is the PC/Laptop camera
                if index == 0:
                    continue
                
                self.cap = cv2.VideoCapture(index)
                ret, frame = self.cap.read()
                
                if self.cap.isOpened() and ret:
                    working_device = index
                
                self.cap.release() 
            
            if working_device == None:
                print('No Camera Found')
                exit()
            self.cap = cv2.VideoCapture(working_device)
                
    def display_gui(self):
        #default_threshold and parameter can be changed in the settings
        
        #threshold value which is used to classify the pixel values
        #must be between 0 and 255
        default_thresh = 230
        #selection of epsilon, effects the accuracy, used in gear_tools.py
        parameter = 0.008  
        
        button_size = (12, 2)
        font_size = 'Helvetica 22'
        color = ('white','#bfbfbf')
        
        control_panel = [[sg.Button('', key = 'setting', image_filename='imgs/setting_icon.png', pad=((175, 0), 0))],
                         [sg.Button('Black/White', key='first_button', size=button_size, font=font_size, button_color=color, pad=(0, (10, 0)))],
                         [sg.Button('', size=(12, 1), button_color=('gray', '#EFEFEF'), pad=(0, (0, 0)), border_width=0)],
                         [sg.Button('Capture', key='second_button', size=button_size, font=font_size, button_color=color, pad=(0, (0, 0)))],
                         [sg.Slider(range=(0, 255), key='thresh_slider', orientation='h', size=(19, 20), default_value=default_thresh, visible=False)],
                         [sg.Text('Teeth# None', key='teeth', font=font_size, visible=False)],
                         [sg.Text('Number of Pixels# None', key='diameter', font=font_size, visible=False)]]

        layout = [[sg.Image(filename='', key='display', pad=(25, 0))] +
                  [sg.Column(control_panel)]]

        window = sg.Window('Gear Analytics', layout, background_color = '#EFEFEF', location=(200,100))    
        
        #called before while loop so gui pops up with everthing inside without the need to load
        ret, frame = self.cap.read()    
        
        #whether video needs to be converted to black/white            
        convert = False
        #whether to show the results or not
        result = False 

        while True:
            event, values = window.Read(timeout=20)
            ret, frame = self.cap.read()

            #open setting window
            if event == 'setting':
                default_thresh, parameter = settingsGui.settings(default_thresh, parameter)
                window.FindElement('thresh_slider').Update(default_thresh) 
            
            elif event == 'first_button':
                
                #if statement is to make sure convert stays false after user presses back from the result screen
                if result == True:
                    convert = False
                else: convert = not convert
                
                result = False 
                window.FindElement('first_button').Update('Back') 
                
                if convert == True:
                    window.FindElement('thresh_slider').Update(visible=True) 
                else:
                    window.FindElement('teeth').Update(visible=False) 
                    window.FindElement('diameter').Update(visible=False)                     
                    window.FindElement('thresh_slider').Update(visible=False)                                       
                    window.FindElement('first_button').Update('Black/White') 
                
                #in both cases there should always be a first button
                window.FindElement('second_button').Update(visible=True)
            
            elif event == 'second_button':
                result = True
                window.FindElement('thresh_slider').Update(visible=False)
                window.FindElement('second_button').Update(visible=False) 
                window.FindElement('first_button').Update('Back') 
                window.FindElement('teeth').Update(visible=True) 
                window.FindElement('diameter').Update(visible=True) 
                
                #run the frame through the gear tools class and gets the results
                gear_result = tools(frame, values['thresh_slider'], parameter)   
                gear_result.color_to_thresh()
                gear_result.find_contour()
                gear_result.find_products()
                
                window.FindElement('teeth').Update('Teeth# ' + gear_result.num_of_teeth) 
                window.FindElement('diameter').Update('Diameter: ' + gear_result.diameter + " in")
            
            #if window is turned off end the program
            elif event == None or event == 'Exit':
                window.Close()
                exit()  
            
            
            if result == True:
                imgbytes=cv2.imencode('.png', gear_result.img)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)                           
            
            elif convert == True:
                conversion = tools(frame, values['thresh_slider'], parameter)
                conversion.color_to_thresh()
                imgbytes=cv2.imencode('.png', conversion.threshold)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)          
            
            else:
                imgbytes=cv2.imencode('.png', frame)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)        
    