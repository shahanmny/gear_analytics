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
            working_device = 0
            
            # for index in range(100):
            #     self.cap = cv2.VideoCapture(index)
            #     ret, frame = self.cap.read()
                
            #     if self.cap.isOpened() and ret:
            #         working_device = index
                
            #     self.cap.release() 
            
            # if working_device == None:
            #     print('No Camera Found')
            #     exit()
            
            self.cap = cv2.VideoCapture(working_device)
    
    def display_gui(self):
        #default_threshold and parameter can be changed in the settings
        
        #threshold value which is used to classify the pixel values
        #must be between 0 and 255
        default_thresh = 150
        #selection of epsilon, effects the accuracy, used in gear_tools.py
        parameter = 0.008  
        
        button_size = (9, 4)
        font_size = 'Helvetica 20'
        color = ('white','#bfbfbf')
        
        control_panel = [[sg.Button('', key = 'setting', image_filename='imgs/setting_icon.png', pad=((100, 0), 0))],
               [sg.Slider(range=(0, 255), key='thresh_slider', orientation='h', size=(13, 20), default_value=default_thresh, visible=False)],
               [sg.Text('Teeth# None', key='result', font=font_size, visible=False)],
               [sg.Button('Capture', key='first_button', size=button_size, font=font_size, button_color=color, pad=(0, (35, 0)))],
               [sg.Button('Black/White', key='second_button', size=button_size, font=font_size, button_color=color, pad=(0, (10, 0)))]]
        
        layout = [[sg.Image(filename='', key='display', pad=(25, 0))] +
                  [sg.Column(control_panel)]]

        window = sg.Window('Gear Analytics', layout, location=(200,100))
        
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
                result = True
                window.FindElement('thresh_slider').Update(visible=False)
                window.FindElement('first_button').Update(visible=False) 
                window.FindElement('second_button').Update('Back') 
                window.FindElement('result').Update(visible=True) 
                
                #run the frame through the gear tools class and gets the results
                gear_result = tools(frame, values['thresh_slider'], parameter)   
                gear_result.color_to_thresh()
                gear_result.find_teeth()
                
                teeth = 'Teeth# ' + gear_result.num_of_teeth
                window.FindElement('result').Update(teeth) 
            
            elif event == 'second_button':
                window.FindElement('thresh_slider').Update(visible=False)
                window.FindElement('result').Update(visible=False)             
                window.FindElement('first_button').Update(visible=True)
                
                #if statement is to make sure convert stays false after user presses back from the result screen
                if result == True:
                    convert = False
                else: convert = not convert
                
                result = False 
                window.FindElement('second_button').Update('Back') 
                
                if convert == True:
                    window.FindElement('thresh_slider').Update(visible=True) 
                else:
                    window.FindElement('second_button').Update('Black/White') 
                    window.FindElement('thresh_slider').Update(visible=False)                                       
            
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
    