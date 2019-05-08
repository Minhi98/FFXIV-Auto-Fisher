from DirectXKeyCodes import PressKey, ReleaseKey, xivInput
import time

"""
Insert and edit your rotations here, and be careful to make sure state variables are working in practice
assign abilities to variables with these scan codes to represent buttons: 
http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

xivInput(key) to input a single key
xivInput([key,key,key, ...]) to input a key combo
"""
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
    xivInput(btn["cast_line"])
    can_press = False
    casted = True

    return can_press, casted, reset

def collectible():
    xivInput(btn["LMenu"])
    time.sleep(0.25)
    xivInput(btn["Confirm"])

# Your rotation methods ------------------------------------------------------------------------------------------
def level_grind_cast(reset=6):
    for x in range(2): xivInput(btn["patience"], 0.25)
    for x in range(2): xivInput(btn["mooch"], 0.25)
    for x in range(2): xivInput(btn["cast_line"], 1)

    return reset

def level_grind_hook(reset=30):
    for x in range(2): xivInput(btn["hook"], 0.5)
        
    return reset
