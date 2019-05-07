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

def xivInput(key, delay=0.0):
    focus_window()
    PressKey(key)
    ReleaseKey(key)
    focus_window()
    time.sleep(delay)

def main(cast_line=0x02, hook=0x03, release=0x04, mooch=0x05, patience=0x07, quit=0x22, cordial=0x21,\
    threshhold = 0.93, winX=1600, winY=900, script_view=True, use_skills=True, use_mooch=True):
    xivInput(cast_line)
    can_press = False
    casted = True
    reset = 30
    loc_memory = [] #index [-1] is the latest location
    template = cv2.imread('cast-light.png', 0)
    w,h = template.shape[::-1]
    while True:
        current_frame =  np.array(ImageGrab.grab(bbox=(10+(int(winX/4)),60,int(winX*0.75),int(winY/1.5))))
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
        cv2.putText(current_frame, str(current_animation) + " frame difference",\
            (20,int((winX/3)-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
        if can_press and current_animation is not None:
            if current_animation == 0 and not casted:
                print('0 frame, idle - attempt cast')
                if use_skills:
                    for x in range(2): xivInput(patience, 0.25)
                    for x in range(2): xivInput(mooch, 0.25)
                for x in range(2): xivInput(cast_line, 1)

                can_press = False
                casted = True
                reset = 6
            elif current_animation > 4 or current_animation < -4 and casted:
                print(str(current_animation) + " frame difference - Catching Bite")
                for x in range(2): xivInput(hook, 0.5)
                can_press = False
                casted = False
                reset = 30

        if not can_press:
            reset -= 1
            if reset == 0:
                can_press = True

        if script_view:
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

def focus_window(winName="FINAL FANTASY XIV"):
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if winName in i[1].upper():
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break

if __name__ == "__main__":
    focus_window()
    main()