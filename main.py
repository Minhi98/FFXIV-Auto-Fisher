import cv2
import numpy as np
from PIL import ImageGrab
import time
import glob
import os
from pprint import pprint
import win32gui
import pyautogui
from DirectXKeyCodes import PressKey, ReleaseKey

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def main(cast_line=0x02, hook=0x03, release=0x04, mooch=0x05, threshhold = 0.92):
    PressKey(cast_line)
    ReleaseKey(cast_line)
    can_press = False
    casted = True
    reset = 30
    loc_memory = [] #index [-1] is the latest location
    template = cv2.imread('cast-light.png', 0)
    w,h = template.shape[::-1]
    while True:
        current_frame =  np.array(ImageGrab.grab(bbox=(10,60,1600,950)))
        cf_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        res = cv2.matchTemplate(cf_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshhold)
        loc_memory.append(loc)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(current_frame, pt, (pt[0] + w, pt[1] + h),(0,255,255),2)

        if len(loc_memory) > 60:
            loc_memory.pop(0)

        current_animation = sense_motion(loc_memory)
        if can_press and current_animation is not None:
            if current_animation == 0 and not casted:
                print('0 frame, idle - attempt cast')
                focus_on_game()
                PressKey(cast_line)
                ReleaseKey(cast_line)
                time.sleep(1)
                PressKey(cast_line)
                ReleaseKey(cast_line)
                time.sleep(1)
                PressKey(cast_line)
                ReleaseKey(cast_line)
                time.sleep(1)
                PressKey(cast_line)
                ReleaseKey(cast_line)
                casted = True
                can_press = False
                reset = 6
            elif current_animation > 4 or current_animation < -4 and casted:
                print(str(current_animation) + " frame difference - Catching Bite")
                focus_on_game()
                for x in range(4): 
                    PressKey(hook)
                    ReleaseKey(hook)
                can_press = False
                casted = False
                reset = 30

        if not can_press:
            reset -= 1
            if reset == 0:
                can_press = True

        cv2.imshow('auto-fish', cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))


def sense_motion(loc_memory):
    y_mem = []
    for y, x in loc_memory:
        y_mem.append(y)
    if len(y_mem) > 2 and len(y_mem[-1]) != 0 and len(y_mem[-2]) != 0:
        latest = y_mem[-1].tolist()[0]
        sec_latest = y_mem[-2].tolist()[0]
        sub = sec_latest - latest
        return sub

def focus_on_game():
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "FINAL FANTASY XIV" in i[1].upper():
            print(i)
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break

if __name__ == "__main__":
    focus_on_game()
    main()