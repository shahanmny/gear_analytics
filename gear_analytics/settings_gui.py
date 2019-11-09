import PySimpleGUI as sg

class settingsGui:
    def settings(default_thresh, parameter):
        layout = [[sg.Text('Default Thresh')] +
                  [sg.InputText(default_thresh, key='default_thresh')],
                  [sg.Text('Parameter')] +
                  [sg.InputText(parameter, key='parameter')],
                  [sg.Button('Reset', button_color = ('white','#bfbfbf'))] +
                  [sg.Button('Exit', button_color = ('white','#bfbfbf'))]]
        
        window = sg.Window('Setting', layout, location=(300,200))
        
        while True:
            event, values = window.Read(timeout=20)
            
            if event == 'Reset':
                window.FindElement('default_thresh').Update(default_thresh)
                window.FindElement('parameter').Update(parameter)
            
            elif event == None or event == 'Exit':
                new_default_thresh = values['default_thresh']
                new_parameter = values['parameter']
                      
                if new_default_thresh == '':
                    new_default_thresh = 230
                if new_parameter == '':
                    new_parameter = 0.008
                
                window.Close()
                
                return int(new_default_thresh), float(new_parameter)
    