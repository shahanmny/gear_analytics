import PySimpleGUI as sg
import cv2
from gear_analytics.gear import Gear
from gear_analytics.settings_gui import SettingsGui

class Gui:
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

        #default_threshold, parameter and background size can be changed in the settings
        
        #thresh value which is used to classify the pixel values
        #must be between 0 and 255
        default_thresh = 230
        #selection of epsilon, effects the accuracy, used in gear_tools.py
        parameter = 0.008  
        #background size is the size in inches of the background 
        background_size = 5
        
        button_size = (15, 2)
        font_size = 'Helvetica 22'
        color = ('white','#bfbfbf')
        slider_message = "The Slider is Disabled Unless it is in Gray Scale Mode"        

        #GUI components
        control_panel = [[sg.Button('', key = 'setting', image_filename='imgs/setting_icon.png', pad=((180, 0), 0))],
                         [sg.Button('Gray Scale', key='first_button', size=button_size, font=font_size, button_color=color, pad=(0, (10, 0)))],
                         [sg.Button('', size=(12, 1), button_color=('gray', '#EFEFEF'), pad=(0, 0), border_width=0)],
                         [sg.Button('Capture', key='second_button', size=button_size, font=font_size, button_color=color, pad=(0, 0))],
                         [sg.Slider(range=(0, 255), key='thresh_slider', orientation='h', trough_color='#bfbfbf', size=(29, 30), default_value=default_thresh, tooltip=slider_message, pad=(0, (10, 0)), disabled=True)],
                         [sg.Multiline('Teeth# None\nDiameter# None', key='output', font=font_size, size=(16, 2), no_scrollbar=True, pad=(0, (15, 0)), disabled=True)]]
        #GUI layout
        layout = [[sg.Image(filename='', key='display', background_color='gray')] +
                  [sg.Column(control_panel, vertical_alignment='top', element_justification='right')]]

        #GUI window
        window = sg.Window('Gear Analytics', layout, location=(200,100))    
        
        #called before while loop so gui pops up with everthing inside without the need to load
        ret, frame = self.cap.read()    
        
        #the current page that the user is on
        page = 'home_page'

        while True:
            #Get the latest event from the GUI and the latest frame captured from the camera
            event, values = window.Read(timeout=20)
            ret, frame = self.cap.read()

            #handle the incoming events from the GUI
            #setting button was pressed
            if event == 'setting':
                #create the settings window
                default_thresh, parameter, background_size = SettingsGui.settings(default_thresh, parameter, background_size)
                window.FindElement('thresh_slider').Update(default_thresh) 
            
            #first button was pressed
            elif event == 'first_button':
                #if user is on the home page that means they want to go to the gray scale page
                if page == 'home_page':
                    page = 'gray_scale_page'
                #otherwise just return the user to the home page
                else:
                    page = 'home_page'

                #based off the page disable and update the components accordingly
                if page == 'home_page':
                    window.FindElement('first_button').Update('Gray Scale')
                    window.FindElement('thresh_slider').Update(disabled=True)                                       

                elif page == 'gray_scale_page':
                    window.FindElement('first_button').Update('Back')
                    window.FindElement('thresh_slider').Update(disabled=False) 

                #updates that are needed for both the home and gray scale pages
                window.FindElement('second_button').Update(disabled=False) 
                window.FindElement('output').Update('Teeth# None\nDiameter# None')                                      
            
            #second button was pressed
            elif event == 'second_button':
                #user wants to get the results, hence the page is the result page
                page = 'result_page'
                
                #disable and update the components accordingly
                window.FindElement('first_button').Update('Back') 
                window.FindElement('thresh_slider').Update(disabled=True)
                window.FindElement('second_button').Update(disabled=True) 
                
                #run the frame through the gear class and gets the results
                gear_result = Gear(frame, values['thresh_slider'], parameter, background_size)   
                gear_result.color_to_thresh()
                gear_result.find_contour()
                gear_result.find_products()
                
                #write out the output to the GUI
                output = ('Teeth# {}\nDiameter# {} in').format(gear_result.num_of_teeth, gear_result.diameter)
                window.FindElement('output').Update(output)
                
                #update the image on the GUI to hold the frame that was captured
                imgbytes=cv2.imencode('.png', gear_result.img)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)   
            
            #if window is turned off end the program
            elif event == None or event == 'Exit':
                window.Close()
                exit()  
            
            #update the image on the GUI with the latest frame that was captured
            if page == 'home_page':
                imgbytes=cv2.imencode('.png', frame)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)   
            #update the image on the GUI with the latest frame which is converted to the gray scale
            elif page == 'gray_scale_page':                    
                convert = Gear(frame, values['thresh_slider'], parameter, background_size)
                convert.color_to_thresh()

                imgbytes=cv2.imencode('.png', convert.threshold)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes) 