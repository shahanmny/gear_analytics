# gear_analytics
Find the Number of Teeth and the Diameter of a Gear

# Output Example
![Result](https://user-images.githubusercontent.com/31074545/122280502-42ccff00-ceb7-11eb-84b3-fad0a79eefa0.PNG)

# Prerequisites
Libraries to install: <br>
  * pip install numpy 
  * pip install opencv-python 
  * pip install PySimpleGUI 
  * pip install argparse

Git clone this repository <br>

# Setup 
Place the gear on a white background <br>
Place the camera so that it gets a brids eye view of the gear <br>
Provide adequate lighting and keep shadows to the minimum <br>
  
# Instructions 
Run in the gear_analytics folder:
  * python -m gear_analytics

The Program automatically will find the camera being used

Default Mode
* Shows a video outlining the gear, make sure it is reading all the edges and that there are no gaps
* The first slider effects the thresh, in other words whether a pixel should be assigned white or black
* The second slider dilates the frames in order to close any gaps between the gear's edges

Normal Mode
* Shows a video of the gear without any filters
