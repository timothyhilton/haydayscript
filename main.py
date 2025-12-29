import pyautogui
import time
import os
from pathlib import Path

pyautogui.FAILSAFE = True

scytheDragOffset = (450, 210)
scytheDragDuration = 1

wheatDragOffset = (450, 260)
wheatDragDuration = 1

print("beginning in 3 seconds")
time.sleep(3)

def checkSiloFull():
    try:
        pyautogui.locateOnScreen("./assets/shop/silofull.png", confidence=0.9)
        return True
    except:
        return False

def checkPlantingNeeded():
    if(locateInDir("./assets/wheat/plant") != None):
        return True
    else:
        return False

def checkHarvestingNeeded():
    try:
        locateInDir("./assets/wheat/ready/", confidence=0.9)
        return True
    except:
        return False

def locateInDir(directory, confidence=0.9, grayscale=False):
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    directory_path = Path(directory)
    
    if not directory_path.exists():
        return None
    
    image_files = [f for f in directory_path.iterdir()
                   if f.is_file() and f.suffix.lower() in image_extensions]
    
    for image_file in image_files:
        try:
            location = pyautogui.locateCenterOnScreen(str(image_file), confidence=confidence, grayscale=grayscale)
            if location:
                return location
        except:
            pass
    
    return None

def moveTo(image, confidence=0.8, grayscale=False):
    try:
        location = locateInDir(image, confidence=confidence, grayscale=grayscale)
        
        if location:
            x, y = location

            target_x = x / 2
            target_y = y / 2

            print(f"Corrected target: {target_x}, {target_y}")
            
            pyautogui.moveTo(target_x, target_y)
            return True
            
        else:
            print("Image still not found.")
            return False

    except Exception as e:
        print(f"Error finding image {e}")
        return False

def plant_wheat():
    if(moveTo("./assets/wheat/plant", confidence=0.7, grayscale=True) == False): return
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(1)
    moveTo("./assets/wheat/drag")
    pyautogui.dragRel(wheatDragOffset, duration=wheatDragDuration, button="left")

def harvest_wheat():
    if(moveTo("./assets/wheat/ready", confidence=0.9) == False): return
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.3)
    moveTo("./assets/wheat/scythe/", confidence=0.7)
    pyautogui.dragRel(scytheDragOffset, duration=scytheDragDuration, button="left")

def main():
    while 1:
        if(checkHarvestingNeeded()):
            harvest_wheat()
        if(checkPlantingNeeded()):
            plant_wheat()
        print("finished loop, waiting")
        time.sleep(0.1)

main()