import PySimpleGUI as sg

class SettingsGui:
    def settings(default_thresh, parameter):
        layout = [[sg.Text('Default Thresh')] +
                  [sg.InputText(default_thresh, key='default_thresh')],
                  [sg.Text('Parameter')] +
                  [sg.InputText(parameter, key='parameter')],
                  [sg.Button('Reset', button_color = ('white','#bfbfbf'))] +
                  [sg.Button('Save & Exit', button_color = ('white','#bfbfbf'))]]
        
        window = sg.Window('Setting', layout, location=(300,200))
        
        while True:
            event, values = window.Read(timeout=20)
            
            if event == 'Reset':
                window.FindElement('default_thresh').Update(default_thresh)
                window.FindElement('parameter').Update(parameter)
            
            elif event == None or event == 'Exit':
                if values == None or not values['default_thresh'].strip():
                    new_default_thresh = 230
                else:
                    new_default_thresh = values['default_thresh']
                
                if values == None or not values['parameter'].strip():
                    new_parameter = 0.008
                else:
                    new_parameter = values['parameter']
                      
                window.Close()
                
                return int(new_default_thresh), float(new_parameter)
    