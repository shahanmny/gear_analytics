import sys
from gear_analytics.main_gui import Gui

if __name__ == '__main__':
    second_camera = False
    if(len(sys.argv) > 1):
        second_camera = True if sys.argv[1] == '-second' else False;

    gui = Gui(second_camera)

    gui.find_cam()

    gui.display_gui()



