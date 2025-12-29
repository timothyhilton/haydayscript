import pyautogui
import time
from pathlib import Path

pyautogui.FAILSAFE = True

relativeHarvestPoints = [
    (70, 7),       # Point 1 -> 2
    (113, 69),     # Point 2 -> 3
    (75, -40),     # Point 3 -> 4
    (-90, -48),    # Point 4 -> 5
    (-60, 31),     # Point 5 -> 6
    (74, 38),      # Point 6 -> 7
    (42, -24),     # Point 7 -> 8
    (-58, -29),    # Point 8 -> 9
    (-26, 14),     # Point 9 -> 10
    (54, 31)       # Point 10 -> 11
]

print("beginning in 3 seconds")
time.sleep(3)

def getImgLoc(directory, confidence=0.9, grayscale=False):
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    full_directory = Path("./assets") / directory

    if not full_directory.exists():
        print(f"directory not found: {full_directory}")
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
    if(reset == None): input("check state, press enter to continue")
    pyautogui.moveTo(getImgLoc("misc/reset", confidence=0.8))
    time.sleep(0.1)
    pyautogui.click()
    reset = getImgLoc("misc/reset", confidence=0.8)
    if(reset == None): input("check state, press enter to continue")
    pyautogui.moveTo(getImgLoc("misc/reset", confidence=0.8))
    time.sleep(1)
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
                time.sleep(2)
                sycthe = getImgLoc("wheat/scythe", confidence=0.8)
                if(sycthe == None):
                    print("sycthe not found")
                    attemptReset()
                    continue
                
                pyautogui.moveTo(sycthe)

                pyautogui.mouseDown(_pause=False, button='primary')
                for point in relativeHarvestPoints:
                    distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
                    # e.g. 0.005 seconds per pixel, clamp to 0.05 minimum
                    duration = distance * 0.02
                    pyautogui.dragRel(point[0], point[1], duration=duration, mouseDownUp=False, button='left')
                pyautogui.mouseUp(_pause=False, button='primary')

        time.sleep(0.1)

main()

