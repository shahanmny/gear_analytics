from gear_analytics.main_gui import gui

if __name__ == "__main__":
    gui = gui()
    #If no usb camera is found the webcam will be used
    gui.find_cam()

    gui.display_gui()



