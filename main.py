import pyautogui
import time
from pathlib import Path

pyautogui.FAILSAFE = True

advertiseButtonOffset = 100

harvestSpeed = 1
relativeHarvestPoints = [
    (63, 11),   # Point 1 -> 2
    (117, 64),  # Point 2 -> 3
    (16, -9),   # Point 3 -> 4
    (-91, -44), # Point 4 -> 5
    (18, -8),   # Point 5 -> 6
    (88, 45),   # Point 6 -> 7
    (12, -9),   # Point 7 -> 8
    (-86, -42), # Point 8 -> 9
    (16, -9),   # Point 9 -> 10
    (88, 43),   # Point 10 -> 11
    (19, -5),   # Point 11 -> 12
    (-95, -46)  # Point 12 -> 13
]

plantSpeed = 1
relativePlantPoints = [
    (-29, 42),    # 1 -> 2
    (116, 61),    # 2 -> 3
    (15, -8),     # 3 -> 4
    (-90, -47),   # 4 -> 5
    (14, -5),     # 5 -> 6
    (91, 45),     # 6 -> 7
    (15, -9),     # 7 -> 8
    (-90, -43),   # 8 -> 9
    (15, -7),     # 9 -> 10
    (91, 46),     # 10 -> 11
    (12, -10),    # 11 -> 12
    (-88, -45)    # 12 -> 13
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

def runHarvest():
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
            return False
        
        pyautogui.moveTo(sycthe)

        pyautogui.mouseDown(_pause=False, button='primary')
        for point in relativeHarvestPoints:
            distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
            duration = distance * 0.01 * harvestSpeed
            pyautogui.dragRel(point[0], point[1], duration=duration, mouseDownUp=False, button='left')
        pyautogui.mouseUp(_pause=False, button='primary')

def runPlant():
    plant = getImgLoc("wheat/plant")

    if(plant == None):
        return False
    
    pyautogui.moveTo(plant)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(2)
    drag = getImgLoc("wheat/drag", confidence=0.8)
    if(drag == None):
        print("wheat to drag not found")
        attemptReset()
        return False

    pyautogui.moveTo(drag)

    pyautogui.mouseDown(_pause=False, button='primary')
    for point in relativePlantPoints:
        distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
        duration = distance * 0.01 * plantSpeed
        pyautogui.dragRel(point[0], point[1], duration=duration, mouseDownUp=False, button='left')
    pyautogui.mouseUp(_pause=False, button='primary')

    attemptReset()

def handleSelling():
    pyautogui.moveTo(getImgLoc("misc/closemenu"))
    pyautogui.click()
    time.sleep(0.7)
    pyautogui.moveTo(getImgLoc("shop/open"))
    pyautogui.click()

    while(getImgLoc("shop/sold")):
        pyautogui.moveTo(getImgLoc("shop/sold"))
        pyautogui.click()
        time.sleep(0.7)
    
    while(getImgLoc("shop/createnew")):
        pyautogui.moveTo(getImgLoc("shop/createnew"))
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.moveTo(getImgLoc("shop/wheattosell"))
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.moveTo(getImgLoc("shop/maxprice"))
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.moveTo(getImgLoc("shop/putonsale"))
        pyautogui.click()
        time.sleep(0.3)

    wheattoadvert = getImgLoc("shop/wheattoadvert")
    if(wheattoadvert):
        pyautogui.moveTo(wheattoadvert)
        pyautogui.click()
        time.sleep(0.3)
        ad = getImgLoc("shop/advertisenow")
        if(ad):
            pyautogui.moveTo(ad[0] + advertiseButtonOffset, ad[1])
            pyautogui.click()
            time.sleep(0.3)
            pyautogui.moveTo(getImgLoc("shop/createad"))
            pyautogui.click()
            time.sleep(0.3)
            
            pyautogui.moveTo(getImgLoc("misc/closemenu"))
            pyautogui.click()
        else:
            pyautogui.moveTo("misc/closemenu")
            pyautogui.click()
    
    time.sleep(0.3)
    
    
    

def main():
    while(1):
        sellingNeeded = getImgLoc("shop/silofull")
        if(sellingNeeded):
            handleSelling()

        if(getImgLoc("misc/homecheck", confidence=0.95) == None):
            print("ruh roh")
            attemptReset()
            continue

        harvest = runHarvest()
        # if(harvest == False):
        #     continue

        plant = runPlant()
        # if(plant == False):
        #     continue
        



main()

