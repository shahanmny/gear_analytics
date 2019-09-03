import PySimpleGUI as sg

class settingsGui:
    def settings(default_thresh, something):

        layout = [[sg.Text('Default Thresh')] +
                  [sg.InputText(default_thresh, key='default_thresh')],
                  [sg.Text('Something')] +
                  [sg.InputText(something, key='something')],
                  [sg.Button('Reset', button_color = ('white','#bfbfbf'))] +
                  [sg.Button('Exit', button_color = ('white','#bfbfbf'))]]
        
        window = sg.Window('Setting', layout, location=(300,200))
        while True:
            event, values = window.Read(timeout=20)
            if event == 'Reset':
                window.FindElement('default_thresh').Update(default_thresh)
                window.FindElement('something').Update(something)
            elif event is None or event == 'Exit':
                if values['default_thresh'] == '' || values['default_thresh'] > 255:
                    values['default_thresh'] = default_thresh
                if values['something'] == '':
                    values['something'] = something
                window.Close()
                return int(values['default_thresh']), float(values['something'])
    