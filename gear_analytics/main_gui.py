import PySimpleGUI as sg
import cv2
from gear_analytics.gear import Gear
from gear_analytics.settings_gui import SettingsGui

class Gui:
    """
    The Primary GUI

    Attributes:
    cap: The camera that is used for the video capture
    second_camera: Whether or not if the second camera should be used
    background_width: The width of the frame in inches
    """

    def __init__(self, second_camera, background_width):
        """
        The constructor for the GUI class
        
        Parameters:
            cap: The camera that is used for the video capture
            second_camera: Whether or not if the second camera should be used
            background_width: The width of the frame in inches
        """
        self.cap = None
        self.second_camera = second_camera
        self.background_width = background_width
    
    def find_cam(self):
        """Find the camera"""  
        working_device = None
        
        for index in range(100):
            
            #If the user wants to use the second camera, then skip the first one
            if index == 0 and self.second_camera == True:
                continue
            
            #Get the device and capture a image
            self.cap = cv2.VideoCapture(index)
            ret, frame = self.cap.read()
            
            #Check if the camera works
            if self.cap.isOpened() and ret:
                working_device = index
                break
            
            self.cap.release() 
        
        #If no camera was found, then exit the program
        if working_device == None:
            print('Camera Not Found')
            exit()
        
        #Assign the camera to a object property
        self.cap = cv2.VideoCapture(working_device)
            
    def display_gui(self):
        """Displays and Runs the GUI"""
        sg.theme('LightGray1')

        #default_threshold and background_width can be changed in the settings
        
        #thresh value which is used to classify the pixel values
        default_thresh = 3
        #the number of times the frame will be dilated
        default_dilate = 1

        #Some of the properties of the GUI       
        button_size = (15, 2)
        font_size = 'Helvetica 22'
        color = ('white','#bfbfbf')
        slider_message = "The Slider is Disabled in the Normal Mode"   
        thresh_slider_message = "Effects the Threshold \n" + slider_message
        dilate_slider_message = "The Number of Times the Image has been Dilated \n" + slider_message     

        #GUI components
        control_panel = [[sg.Button('', key = 'setting', image_filename='imgs/setting_icon.png', pad=((180, 0), 0))],
                         [sg.Button('Normal Mode', key='first_button', size=button_size, font=font_size, button_color=color, pad=(0, (10, 0)))],
                         [sg.Button('', size=(12, 1), button_color=('gray', '#EFEFEF'), pad=(0, 0), border_width=0)],
                         [sg.Button('Capture', key='second_button', size=button_size, font=font_size, button_color=color, pad=(0, 0))],
                         [sg.Slider(range=(3, 45), key='thresh_slider', orientation='h', trough_color='#bfbfbf', size=(29, 30), default_value=default_thresh, tooltip=thresh_slider_message, pad=(0, (10, 0)))],
                         [sg.Slider(range=(1, 5), key='dilate_slider', orientation='h', trough_color='#bfbfbf', size=(29, 30), default_value=default_dilate, tooltip=dilate_slider_message, pad=(0, (10, 0)))],
                         [sg.Multiline('Teeth# None\nDiameter# None', key='output', font=font_size, size=(16, 2), no_scrollbar=True, pad=(0, (15, 0)), disabled=True)]]
        
        #GUI layout
        layout = [[sg.Image(filename='', key='display', background_color='gray')] +
                  [sg.Column(control_panel, vertical_alignment='top', element_justification='right')]]

        #GUI window
        window = sg.Window('Gear Analytics', layout, location=(200,100))    
        
        #Get the first frame
        ret, frame = self.cap.read()    
        
        #The current page that the user is on
        page = 'default_page'

        while True:
            #Get the latest events from the GUI and the latest frame captured from the camera
            event, values = window.Read(timeout=20)
            ret, frame = self.cap.read()

            #Handle the incoming events from the GUI
            #Setting button was pressed
            if event == 'setting':
                #create the settings window and get back the things that were changed
                default_thresh, self.background_width = SettingsGui.settings(default_thresh, self.background_width)
                window.FindElement('thresh_slider').Update(default_thresh) 
            
            #First button was pressed
            elif event == 'first_button':
                #If user is on the default page that means they want to go to the normal mode page
                if page == 'default_page':
                    page = 'normal_mode_page'
                #Otherwise just return the user to the default page
                else:
                    page = 'default_page'

                #Based off the page disable and update the components accordingly
                if page == 'default_page':
                    window.FindElement('first_button').Update('Normal Mode')
                    window.FindElement('thresh_slider').Update(disabled=False)                                       
                    window.FindElement('dilate_slider').Update(disabled=False)                                       

                elif page == 'normal_mode_page':
                    window.FindElement('first_button').Update('Back')
                    window.FindElement('thresh_slider').Update(disabled=True) 
                    window.FindElement('dilate_slider').Update(disabled=True) 

                #Updates that are needed for both the default and normal mode pages
                window.FindElement('second_button').Update(disabled=False) 
                window.FindElement('output').Update('Teeth# None\nDiameter# None')                                      
            
            #Second button was pressed
            elif event == 'second_button':
                #User wants to get the results that means the page is the result page
                page = 'result_page'
                
                #Disable and update the components accordingly
                window.FindElement('first_button').Update('Back') 
                window.FindElement('thresh_slider').Update(disabled=True)
                window.FindElement('second_button').Update(disabled=True) 
                
                #Create a Gear object to find the number of teeth on the gear
                gear_teeth = Gear(frame, values['thresh_slider'], values['dilate_slider'], self.background_width)   
                gear_teeth.grayscale()
                gear_teeth.canny_edge()
                gear_teeth.dilate()   
                gear_teeth.threshold()
                gear_teeth.find_teeth()
                
                #Create another Gear object to find the diameter of the gear
                gear_diameter = Gear(frame, values['thresh_slider'], values['dilate_slider'], self.background_width)   
                gear_diameter.grayscale()
                gear_diameter.blur()
                gear_diameter.remove_noise()
                gear_diameter.threshold()
                gear_diameter.find_diameter()

                #write out the output to the GUI
                output = ('Teeth# {}\nDiameter# {} in').format(gear_teeth.num_of_teeth, gear_diameter.diameter)
                window.FindElement('output').Update(output)
                
                #Update the image on the GUI to hold the frame that was captured
                imgbytes=cv2.imencode('.png', gear_teeth.result)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)    
            
            #If window is turned off, then end the program
            elif event == None or event == 'Exit':
                window.Close()
                exit()  
            
            #Update the image on the GUI with the latest frame that was captured
            if page == 'default_page':
                #Create a new Gear object which will convert the frame such that the user will be able to see if the gear is being captured properly 
                convert = Gear(frame, values['thresh_slider'], values['dilate_slider'], self.background_width)
                convert.grayscale()
                convert.canny_edge()
                convert.dilate()
                convert.threshold()

                #Update the GUI with the converted frame
                imgbytes=cv2.imencode('.png', convert.frame)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes) 

            #If the page is in normal mode, then update the GUI with a normal frame
            elif page == 'normal_mode_page':                    
                imgbytes=cv2.imencode('.png', frame)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)   
