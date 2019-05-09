from DirectXKeyCodes import PressKey, ReleaseKey, xivInput
import time
from main import *

"""
Insert and edit your rotations here, and be careful to make sure state variables are working in practice
assign abilities to variables with these scan codes to represent buttons: 
http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

xivInput(key) to input a single key
xivInput([key,key,key, ...]) to input a key combo
"""
# Optons ------------------------------------------------------------------------------------------------------------
threshhold=0.9                     # Image-Template similarity threshhold from 0.00 to 1.00
script_view=True                    # Preview of what the program sees
biting_frame_diff=5                 # The frame y-coord difference between current and previous frame to consider a biting animation
winX=1600                           # Game window width
winY=900                            # Game window height
templateImage = 'cast-light.png'    # Name of template image for fishing rod light

setRotation = 'level_grind_cast'
setHook = 'default_hook'
# Buttons ----------------------------------------------------------------------------------------------------------
btn = {
    "LControl":0x1D,
    "Alt":0x38,
    "LShift":0x2A,
    "cast_line":0x02,
    "LMenu": 0x1A,
    "RMenu": 0x1B,
    "Confirm": 0x52,
    "hook":0x03,
    "release":0x04,
    "mooch":0x05,
    "patience":0x07,
    "quit":0x22,
    "cordial":0x21,
}
# Do not delete pre_cast(), unless you know what you are doing ----------------------------------------------------
def pre_cast(reset=30):
    for x in range(1): xivInput(btn["patience"], 0.4)
    for x in range(2): xivInput(btn["cast_line"], 0.4)
    can_press = False
    casted = True

    return can_press, casted, reset

def collectible():
    xivInput(btn["LMenu"])
    time.sleep(0.25)
    xivInput(btn["Confirm"])

# Your rotation methods ------------------------------------------------------------------------------------------
def level_grind_cast(reset=6):
    for x in range(1): xivInput(btn["patience"], 0.4)
    for x in range(1): xivInput(btn["cordial"], 0.4)
    for x in range(1): xivInput(btn["mooch"], 0.4)
    for x in range(2): xivInput(btn["cast_line"], 1)

    return reset

def default_hook(reset=30):
    for x in range(2): xivInput(btn["hook"], 0.5)
        
    return reset

# If running from this file -------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()