import argparse
from gear_stats.main_gui import gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type = str, help = 'File name')
    parser.add_argument('-s', type = float, help = 'Something')
    args = parser.parse_args()

    args.f = 'python_test/imgs/' + args.f

    gui = gui()
    gui.find_port()
    gui.display_img()



