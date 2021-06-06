import PySimpleGUI as sg

class SettingsGui:
    def settings(default_thresh, parameter, background_size):
        layout = [[sg.Text('Default Thresh')] +
                  [sg.InputText(default_thresh, key='default_thresh')],
                  [sg.Text('Parameter')] +
                  [sg.InputText(parameter, key='parameter')],
                  [sg.Text('Background Size')] +
                  [sg.InputText(background_size, key='background_size')] +
                  [sg.Text('Inches')],
                  [sg.Button('Reset', button_color = ('white','#bfbfbf'))] +
                  [sg.Button('Save & Exit', button_color = ('white','#bfbfbf'))]]
        
        window = sg.Window('Setting', layout, location=(300,200))
        
        while True:
            event, values = window.Read(timeout=20)
            
            if event == 'Reset':
                window.FindElement('default_thresh').Update(230)
                window.FindElement('parameter').Update(0.008)
                window.FindElement('background_size').Update(5)
            
            elif event == None or event == 'Save & Exit':
                new_default_thresh = None
                new_parameter = None
                new_background_size = None

                try:
                    if values == None:
                        raise Exception('User Exited') 
                    
                    new_default_thresh = values['default_thresh']
                    new_parameter = values['parameter']
                    new_background_size = values['background_size']
                
                    window.Close()
                    
                    return int(new_default_thresh), float(new_parameter), float(new_background_size)
                
                except:
                    return default_thresh, parameter, background_size
                          
                    