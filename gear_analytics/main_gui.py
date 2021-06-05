#gui library
import PySimpleGUI as sg

#computer vision library
import cv2

from gear_analytics.gear import gear
from gear_analytics.settings_gui import settingsGui

class gui:
    def __init__(self, second_camera):
        self.cap = None
        self.second_camera = second_camera
    
    #looks through each device index to find a camera
    def find_cam(self):  
            working_device = None

            for index in range(100):
                
                #index 0 can be the laptop camera
                if index == 0 and self.second_camera == True:
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
        sg.theme('LightGray1')

        #default_threshold and parameter can be changed in the settings
        
        #threshold value which is used to classify the pixel values
        #must be between 0 and 255
        default_thresh = 230
        #selection of epsilon, effects the accuracy, used in gear_tools.py
        parameter = 0.008  
        
        button_size = (15, 2)
        font_size = 'Helvetica 22'
        color = ('white','#bfbfbf')
        
        #GUI components
        control_panel = [[sg.Button('', key = 'setting', image_filename='imgs/setting_icon.png', pad=((180, 0), 0))],
                         [sg.Button('Gray Scale', key='first_button', size=button_size, font=font_size, button_color=color, pad=(0, (10, 0)))],
                         [sg.Button('', size=(12, 1), button_color=('gray', '#EFEFEF'), pad=(0, 0), border_width=0)],
                         [sg.Button('Capture', key='second_button', size=button_size, font=font_size, button_color=color, pad=(0, 0))],
                         [sg.Slider(range=(0, 255), key='thresh_slider', orientation='h', trough_color='#bfbfbf', size=(29, 30), default_value=default_thresh, pad=(0, (10, 0)), disabled=True)],
                         [sg.Multiline('Teeth# None\nDiameter# None', key='output', font=font_size, size=(16, 2), no_scrollbar=True, pad=(0, (15, 0)), disabled=True)]]
        #GUI layout
        layout = [[sg.Image(filename='', key='display', background_color='gray')] +
                  [sg.Column(control_panel, vertical_alignment='top', element_justification='right')]]

        #GUI window
        window = sg.Window('Gear Analytics', layout, location=(200,100))    
        
        #called before while loop so gui pops up with everthing inside without the need to load
        ret, frame = self.cap.read()    
        
        page = 'home_page'
        #if video needs to be converted to black/white            
        convert = False
        #to show the results or not
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
                if page == 'home_page':
                    page = 'gray_scale_page'
                else:
                    page = 'home_page'

                if page == 'home_page':
                    window.FindElement('first_button').Update('Gray Scale')
                    window.FindElement('thresh_slider').Update(disabled=True)                                       

                elif page == 'gray_scale_page':
                    window.FindElement('first_button').Update('Back')
                    window.FindElement('thresh_slider').Update(disabled=False) 

                window.FindElement('second_button').Update(disabled=False) 
                window.FindElement('output').Update('Teeth# None\nDiameter# None')                                      
            
            elif event == 'second_button':
                page = 'result_page'
                
                window.FindElement('first_button').Update('Back') 
                window.FindElement('thresh_slider').Update(disabled=True)
                window.FindElement('second_button').Update(disabled=True) 
                
                #run the frame through the gear tools class and gets the results
                gear_result = gear(frame, values['thresh_slider'], parameter)   
                gear_result.color_to_thresh()
                gear_result.find_contour()
                gear_result.find_products()
                
                output = ('Teeth# {}\nDiameter# {} in').format(gear_result.num_of_teeth, gear_result.diameter)
                window.FindElement('output').Update(output)
                
                imgbytes=cv2.imencode('.png', gear_result.img)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)   
            
            #if window is turned off end the program
            elif event == None or event == 'Exit':
                window.Close()
                exit()  
            
            if page == 'home_page':
                imgbytes=cv2.imencode('.png', frame)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)   

            elif page == 'gray_scale_page':                    
                convert = gear(frame, values['thresh_slider'], parameter)
                convert.color_to_thresh()

                imgbytes=cv2.imencode('.png', convert.threshold)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes) 