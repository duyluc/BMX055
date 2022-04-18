#!/usr/bin/python3
import curses
from time import *
from i2clibraries import i2c_itg3205, i2c_adxl345, i2c_hmc5883l
#==========================================================
#                       GY-85 Sensor monitoring 
#==========================================================

def displayITG3205(screen, col, temp, x, y, z):
    screen.addstr(1, col, "%.1f  °  ℃     " % temp)
    screen.addstr(2, col, "%.1f ° /s    " % x)
    screen.addstr(3, col, "%.1f ° /s    " % y)
    screen.addstr(4, col, "%.1f ° /s    " % z)
def displayADXL345(screen, col, x, y, z):
    """
     According to ADXL345 Method of reading 
    """
    screen.addstr(1, col, "%.2fmg    " % x)
    screen.addstr(2, col, "%.2fmg    " % y)
    screen.addstr(3, col, "%.2fmg    " % z)
def displayHMC5883L(screen, col, heading, declination, x, y, z):
    """
     According to MC5883L Method of reading 
    """
    screen.addstr(1, col, heading + "   ")
    screen.addstr(2, col, declination + "   ")
    screen.addstr(3, col, "%.2f   " % x)
    screen.addstr(4, col, "%.2f   " % y)
    screen.addstr(5, col, "%.2f   " % z)

try:
    myscreen = curses.initscr() # Initialize the curses
    myscreen.border(0)
    (screen_h, screen_w) = myscreen.getmaxyx() # Get screen height and width 
    curses.start_color() # Set the color 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN) # The bottom of the green black 
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # White with blue words 
    curses.init_pair(3, curses.COLOR_MAGENTA,curses.COLOR_BLACK) # What's in black 
    myscreen.clear() # Remove the canvas 
    #  Calculate the coordinates of each block ,  The screen 3 column ,  Each column displays one sensor 
    col1 = screen_w / 3 * 0
    col2 = screen_w / 3 * 1
    col3 = screen_w / 3 * 2
    #  The screen is divided into three horizontal sections , Write a title in the middle of each block 
    myscreen.addstr(0, int(col1 + screen_w / 3 / 2 - 3), "IGT3205", curses.color_pair(1))
    myscreen.addstr(0, int(col2 + screen_w / 3 / 2 - 4), "ADXL345", curses.color_pair(1))
    myscreen.addstr(0, int(col3 + screen_w / 3 / 2 - 4), "HMC5883L", curses.color_pair(1))
    
    # Painting line , Divide the screen into 3 column 
    for col in range(1, screen_h):
        myscreen.addstr(col, int(col2), " │ ")
        myscreen.addstr(col, int(col3), " │ ")
    #  Print in advance IGT3205 The names of the values of 
    myscreen.addstr(1, int(col1), "Temp:", curses.color_pair(2))
    myscreen.addstr(2, int(col1), "X   :", curses.color_pair(2))
    myscreen.addstr(3, int(col1), "Y   :", curses.color_pair(2))
    myscreen.addstr(4, int(col1), "z   :", curses.color_pair(2))
    #  Print in advance ADXL345 The names of the values of 
    myscreen.addstr(1, int(col2) + 1, "X:", curses.color_pair(2))
    myscreen.addstr(2, int(col2) + 1, "Y:", curses.color_pair(2))
    myscreen.addstr(3, int(col2) + 1, "z:", curses.color_pair(2))
    #  Print in advance HMC5883L The names of the values of 
    myscreen.addstr(1, int(col3) + 1, "Heading:    ", curses.color_pair(2))
    myscreen.addstr(2, int(col3) + 1, "Declination:", curses.color_pair(2))
    myscreen.addstr(3, int(col3) + 1, "X:          ", curses.color_pair(2))
    myscreen.addstr(4, int(col3) + 1, "Y:          ", curses.color_pair(2))
    myscreen.addstr(5, int(col3) + 1, "z:          ", curses.color_pair(2))
    #  Initialization sensor 
    itg3205 = i2c_itg3205.i2c_itg3205(0)
    adxl345 = i2c_adxl345.i2c_adxl345(0)
    hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
    hmc5883l.setContinuousMode() # Set to continuous update mode 
    hmc5883l.setDeclination(9,54) # Set true north magnetic offset compensation 
    while True:
        (itgready, dataready) = itg3205.getInterruptStatus()
        if dataready:
             temp = itg3205.getDieTemperature()
             (x, y, z) = itg3205.getDegPerSecAxes() 
             displayITG3205(myscreen, 6, temp, x, y, z) # Refresh the canvas 
        # read adxl345 data 
        (x, y, z) = adxl345.getAxes()
        displayADXL345(myscreen, int(col2) + 4, x, y, z) # Refresh the canvas 
        # read hmc5883l data 
        (x, y, z) = hmc5883l.getAxes()
        heading = hmc5883l.getHeadingString() # Get the pointing Angle 
        declination = hmc5883l.getDeclinationString() # Obtain the compensation information of magnetic declination Angle 
        displayHMC5883L(myscreen, int(col3) + 13, heading, declination, x, y, z) # Refresh the canvas 
        myscreen.refresh() # Application of the canvas 
        sleep(0.1) # suspended 0.1 seconds 
        myscreen.getch()
finally:
    curses.endwin()
