import sys
import argparse
from gear_analytics.main_gui import Gui

if __name__ == '__main__':
    #Parse the user arguments
    parser = argparse.ArgumentParser(description='Gear Analytics Optional Arguments')
    
    second_camera = False
    background_width = 5

    parser.add_argument('-b', type=int, default=5, dest='background_width', help='The length of the background width in inches')
    parser.add_argument('--second', action='store_true', dest='second_camera', help='Use the second camera connected to the computer')

    args = parser.parse_args()

    #Begin the program
    gui = Gui(args.second_camera, args.background_width)
    gui.find_cam()
    gui.display_gui()



