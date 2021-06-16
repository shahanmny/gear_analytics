import PySimpleGUI as sg

class SettingsGui:
    """
    Contains the methods to run the Settings GUI
    """
    def settings(default_thresh, background_width):
        """
        Runs the Settings GUI, where users can change several options

        Parameters:
            default_thresh: The current default thresh
            background_width: The current width of the background frame

        Returns:
            new_default_thresh: The new default thresh
            new_background_width: The new background width
        """
        #The Setting GUI layout
        layout = [[sg.Text('Default Thresh')] +
                  [sg.InputText(default_thresh, key='default_thresh')],
                  [sg.Text('Background Size')] +
                  [sg.InputText(background_width, key='background_width')] +
                  [sg.Text('Inches')],
                  [sg.Button('Reset', button_color = ('white','#bfbfbf'))] +
                  [sg.Button('Save & Exit', button_color = ('white','#bfbfbf'))]]
        
        #The Setting GUI window
        window = sg.Window('Setting', layout, location=(300,200))
        
        while True:
            #Incoming Events from the Setting GUI
            event, values = window.Read(timeout=20)
            
            #Reset the options
            if event == 'Reset':
                window.FindElement('default_thresh').Update(230)
                window.FindElement('background_width').Update(5)
            
            #Save and Exit the Setting GUI, by returning the new changes
            elif event == None or event == 'Save & Exit':
                new_default_thresh = None
                new_background_width = None

                try:
                    if values == None:
                        raise Exception('User Exited') 
                    
                    new_default_thresh = values['default_thresh']
                    new_background_width = values['background_width']
                
                    window.Close()
                    
                    return int(new_default_thresh), float(new_background_width)
                
                except:
                    return default_thresh, background_width
                          
                    