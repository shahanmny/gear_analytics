# gear_analytics
Find the Number of Teeth on a Gear | More features will be added in the Future

# Prerequisites
Libraries to install:
  pip install numpy
  pip install opencv-python
  pip install PySimpleGUI

Git clone this repository

# Setup 
Place the gear on a white background 
Place the camera so that it gets a brids eye view of the gear
Keep shadows to the minimum
  
# Instructions 
Run in the gear_analytics folder:
  python -m gear_analytics

Here is what should show up:
![picture](C:\Users\shaha\Desktop\home.PNG)

The Program automatically will find the camera being used (may not work with bluetooth)

Capture - capture the frame and return the results
Black/White - shows the contrast between the gear and the background, 
              move the slider to get a better view of the gear,
              to get the best results make sure to check this out before pressing the capture button 
Settings - change the default threshold and parameter values:
           default threshold - threshold value which is used to classify the pixel values,
                               must be between 0 and 255,
                               basically changes where the slider indicator starts from
           parameter - basically effects the accuracy,
                       based off testings 0.008 is the best                    
