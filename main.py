import pyautogui
import time
from pathlib import Path

pyautogui.FAILSAFE = True

advertiseButtonOffset = 100

harvestSpeed = 0.3
relativeHarvestPoints = [
    (63, -19),
    (51, 31),
    (-40, 21),
    (118, 62),
    (12, -8),
    (-119, -63),
    (10, -6),
    (110, 63),
    (8, -5),
    (-118, -62),
    (8, -6),
    (114, 67),
    (5, -6),
    (-115, -66),
    (12, -4),
    (116, 68),
    (9, -4),
    (-125, -67),
    (8, -5),
    (121, 66),
    (11, -2),
    (-133, -74),
    (12, -4),
    (129, 74),
    (12, -4),
    (-136, -73),
    (7, -6),
    (133, 70),
    (-240, -15),
    (32, -20),
    (12, 16),
    (-29, -4)
]

plantSpeed = 0.3
relativePlantPoints = [
    (-22, 45),
    (136, 69),
    (3, -3),
    (-133, -70),
    (5, -9),
    (138, 74),
    (6, -5),
    (-98, -53),
    (7, -9),
    (101, 59),
    (18, -6),
    (-122, -65),
    (9, -3),
    (122, 61),
    (11, -6),
    (-131, -62),
    (11, -6),
    (126, 73),
    (11, -4),
    (-136, -74),
    (9, -5),
    (131, 74),
    (8, -5),
    (-129, -64),
    (8, -9),
    (124, 63),
    (-96, 55),
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
                return (x / 2, y / 2)
        except Exception as e:
            pass
    return None

def closeAllMenus():
    while True:
        closemenu = getImgLoc("misc/closemenu")
        if closemenu:
            print("closing menu")
            pyautogui.click(closemenu)
            time.sleep(0.3)
        else:
            break

def attemptReset():
    print("resetting view")
    reset = getImgLoc("misc/reset", confidence=0.8)
    if reset == None: 
        print("reset button not found, manual help needed")
        input("check state, press enter to continue")
        reset = getImgLoc("misc/reset", confidence=0.8)
    print("clicking first reset")
    pyautogui.click(reset)
    time.sleep(0.5)
    reset = getImgLoc("misc/reset", confidence=0.8)
    if reset == None: 
        print("reset button not found after first click")
        input("check state, press enter to continue")
        reset = getImgLoc("misc/reset", confidence=0.8)
    print("clicking second reset")
    time.sleep(0.5)
    pyautogui.click(reset)
    print("reset done")

def runHarvest():
    print("checking for ready wheat")
    ready = getImgLoc("wheat/ready")
    if ready:
        print("found wheat, clicking")
        pyautogui.click(ready)
        time.sleep(1)
        scythe = getImgLoc("wheat/scythe", confidence=0.8)
        if scythe == None:
            print("scythe not found, resetting")
            attemptReset()
            return False

        print("harvesting")
        pyautogui.moveTo(scythe)
        pyautogui.mouseDown(_pause=False, button='primary')
        for point in relativeHarvestPoints:
            distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
            duration = distance * 0.01 * harvestSpeed
            pyautogui.dragRel(point[0], point[1], duration=duration, mouseDownUp=False, button='left', _pause=False)
        pyautogui.mouseUp(_pause=False, button='primary')
        print("harvest done")
        return True
    else:
        print("no wheat ready")
        return False

def runPlant():
    print("checking for empty plots")
    plant = getImgLoc("wheat/plant")

    if plant == None:
        print("no empty plots found")
        return False

    print("found empty plot, clicking")
    pyautogui.click(plant)
    time.sleep(1)
    drag = getImgLoc("wheat/drag", confidence=0.8)
    if drag == None:
        print("wheat to drag not found, resetting")
        attemptReset()
        return False

    print("planting wheat")
    pyautogui.moveTo(drag)

    pyautogui.mouseDown(_pause=False, button='primary')
    for point in relativePlantPoints:
        distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
        duration = distance * 0.01 * plantSpeed
        pyautogui.dragRel(point[0], point[1], duration=duration, mouseDownUp=False, button='left')
    pyautogui.mouseUp(_pause=False, button='primary')

    print("planting done, resetting")
    attemptReset()
    return True

def handleSelling():
    print("handling sales")
    closemenu = getImgLoc("misc/closemenu")
    if closemenu:
        pyautogui.click(closemenu)
        time.sleep(0.4)
    
    print("opening shop")
    shop = getImgLoc("shop/open")
    if shop:
        pyautogui.click(shop)
        time.sleep(0.4)

    soldItems = []
    try:
        found = pyautogui.locateAllOnScreen("./assets/shop/sold/sold.png", confidence=0.9)
        for box in found:
            x, y = pyautogui.center(box)
            pos = (x / 2, y / 2)
            if not any(abs(pos[0] - p[0]) < 30 and abs(pos[1] - p[1]) < 30 for p in soldItems):
                soldItems.append(pos)
    except Exception as e:
        pass
    
    if soldItems:
        print(f"collecting {len(soldItems)} sold items")
        for sold in soldItems:
            pyautogui.click(sold)
            time.sleep(0.05)

    while getImgLoc("shop/createnew"):
        createnew = getImgLoc("shop/createnew")
        print("creating new sale")
        pyautogui.click(createnew)
        time.sleep(0.3)
        wheat = getImgLoc("shop/wheattosell")
        if not wheat:
            break
        pyautogui.click(wheat)
        time.sleep(0.1)
        maxprice = getImgLoc("shop/maxprice")
        if maxprice:
            pyautogui.click(maxprice)
            time.sleep(0.1)
        sale = getImgLoc("shop/putonsale")
        if sale:
            pyautogui.click(sale)
            time.sleep(0.1)
        print("sale created")

    wheattoadvert = getImgLoc("shop/wheattoadvert")
    if wheattoadvert:
        print("advertising wheat sale")
        pyautogui.click(wheattoadvert)
        time.sleep(0.1)
        ad = getImgLoc("shop/advertisenow")
        if ad:
            pyautogui.click(ad[0] + advertiseButtonOffset, ad[1])
            time.sleep(0.2)
            createad = getImgLoc("shop/createad")
            if createad:
                pyautogui.click(createad)
                time.sleep(0.2)
            print("ad placed, closing shop")
            closemenu = getImgLoc("misc/closemenu")
            if closemenu:
                pyautogui.click(closemenu)
        else:
            print("advertise button not found, closing")
            closemenu = getImgLoc("misc/closemenu")
            if closemenu:
                pyautogui.click(closemenu)
    else:
        print("no wheat to advertise")

    time.sleep(0.2)

def main():
    loop_count = 0
    while 1:
        loop_count += 1
        print(f"loop {loop_count} at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        silofull = getImgLoc("shop/silofull")
        if silofull:
            print("silo full, selling")
            handleSelling()

        closeAllMenus()
        runHarvest()
        runPlant()

        print("loop done, waiting")
        time.sleep(0.5)


main()
