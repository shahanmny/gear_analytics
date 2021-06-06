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
                if values == None or not values['default_thresh'].strip():
                    new_default_thresh = default_thresh
                else:
                    new_default_thresh = values['default_thresh']
                
                if values == None or not values['parameter'].strip():
                    new_parameter = parameter
                else:
                    new_parameter = values['parameter']
                if values == None or not values['background_size'].strip():
                    new_background_size = background_size
                else:
                    new_background_size = values['background_size']
                      
                window.Close()
                
                return int(new_default_thresh), float(new_parameter), float(new_background_size)
    