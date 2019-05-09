import cv2
import numpy as np
from PIL import ImageGrab
import time
import glob
import os
from pprint import pprint
import pyautogui
import rotations
from rotations import *

# Edit which rotations you are choosing here:
def register_inputs(can_press, casted, reset, current_animation):
    if can_press and current_animation is not None:
            if current_animation == 0 and not casted:
                reset = getattr(rotations, setRotation)()
                can_press = False
                casted = True
            elif current_animation > biting_frame_diff or current_animation < -biting_frame_diff and casted:
                reset = getattr(rotations, setHook)()
                can_press = False
                casted = False
            return can_press, casted, reset
    return can_press, casted, reset

def main():
    can_press, casted, reset = pre_cast()
    loc_memory = [] #index [-1] is the latest location
    template = cv2.imread(templateImage, 0)
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
        cv2.putText(current_frame, str(current_animation) + " frame difference, Casted: " + str(casted) + ", can_press: " + str(can_press),\
            (75, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)

        can_press, casted, reset = register_inputs(can_press, casted, reset, current_animation)

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

if __name__ == "__main__":
    main()