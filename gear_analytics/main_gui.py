import PySimpleGUI as sg
import cv2

from gear_analytics.gear_tools import tools
from gear_analytics.settings_gui import settingsGui

class gui:
    def __init__(self):
        self.cam = None
    
    def find_port(self):
            for port in range(100):
                self.cam = cv2.VideoCapture(port)
                if self.cam.isOpened() and port != 1:
                    workingPort = port
                self.cam.release() 
            self.cam = cv2.VideoCapture(workingPort)
    
    def display_img(self):
        default_thresh = 150
        something = 0.008  
        button_size = (8, 4)
        font_size = 'Helvetica 22'
        button = ('white','#bfbfbf')
        col = [[sg.Button('', key = 'setting', image_filename='imgs/setting_icon.png', pad=((100, 0), 0))],
               [sg.Slider(range=(0, 255), key='thresh_slider', orientation='h', size=(13, 20), default_value=default_thresh, visible=False)],
               [sg.Text('Teeth# None', key='result', font=font_size, visible=False)],
               [sg.Button('Capture', key='first_button', size=button_size, font=font_size, button_color=button, pad=(0, (50, 0)))],
               [sg.Button('Convert', key='second_button', size=button_size, font=font_size, button_color=button, pad=(0, (10, 0)))]]
        
        layout = [[sg.Image(filename='', key='display', pad=(20, 0))] +
                  [sg.Column(col)]]

        window = sg.Window('Gear Tools', layout, location=(200,100))
        
        ret, frame = self.cam.read()                
        convert = False
        result = False

        while True:
            event, values = window.Read(timeout=20)
            ret, frame = self.cam.read()

            if event == 'setting':
                default_thresh, something = settingsGui.settings(default_thresh, something)
                window.FindElement('thresh_slider').Update(default_thresh)
            
            elif event == 'first_button':
                result = True
                window.FindElement('thresh_slider').Update(visible=False)
                window.FindElement('first_button').Update(visible=False) 
                window.FindElement('second_button').Update('Back') 
                window.FindElement('result').Update(visible=True) 
                gear_result = tools(frame, values['thresh_slider'], something)   
                gear_result.color_to_thresh()
                gear_result.find_teeth()
                teeth = 'Teeth# ' + gear_result.num_of_teeth
                window.FindElement('result').Update(teeth) 
            
            elif event == 'second_button':
                window.FindElement('first_button').Update(visible=True)
                window.FindElement('result').Update(visible=False)             
                if result ==  True:
                    convert = False
                else:
                    convert = not convert
                result = False 
                window.FindElement('second_button').Update('Back') 
                if convert is True:
                    window.FindElement('thresh_slider').Update(visible=True) 
                else:
                    window.FindElement('second_button').Update('Convert') 
                    window.FindElement('thresh_slider').Update(visible=False)                                       
            
            elif event is None or event == 'Exit':
                exit()  
            
            if result == True:
                imgbytes=cv2.imencode('.png', gear_result.img)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)  
                               
            elif convert == True:
                conversion = tools(frame, values['thresh_slider'], something)
                conversion.color_to_thresh()
                imgbytes=cv2.imencode('.png', conversion.threshold)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)          
            else:
                imgbytes=cv2.imencode('.png', frame)[1].tobytes() 
                window.FindElement('display').Update(data=imgbytes)        
                    
        window.Close()
