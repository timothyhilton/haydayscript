import pyautogui
import time
import os
from pathlib import Path

pyautogui.FAILSAFE = True

print("beginning in 3 seconds")
time.sleep(3)

def getImgLoc(directory, confidence=0.8, grayscale=False):
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    full_directory = Path("./assets") / directory

    if not full_directory.exists():
        return None

    image_files = [f for f in full_directory.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

    for image_file in image_files:
        try:
            location = pyautogui.locateCenterOnScreen(str(image_file), confidence=confidence, grayscale=grayscale)
            if location:
                x, y = location
                target_x = x / 2
                target_y = y / 2
                return (target_x, target_y)
        except Exception as e:
            pass
    return None

def attemptReset():
    reset = getImgLoc("misc/reset", confidence=0.8)
    pyautogui.moveTo(reset)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.click()

def main():
    while(1):
        if(getImgLoc("misc/homecheck", confidence=0.7) == None):
            print("ruh roh")
        else:
            ready = getImgLoc("wheat/ready")
            if(ready):
                pyautogui.moveTo(ready)
                time.sleep(0.1)
                pyautogui.click()
                
                sycthe = getImgLoc("wheat/sycthe")
                if(sycthe == None):
                    print("sycthe not found")
                    attemptReset()
                    continue
                
                pyautogui.moveTo(sycthe)
                    time.sleep(0.1)
                    pyautogui.click()

                pyautogui.moveRel(100, 100, duration=1)
                pyautogui.mouseUp()
        time.sleep(0.1)

main()

