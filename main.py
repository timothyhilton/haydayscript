import pyautogui
import time
from pathlib import Path

pyautogui.FAILSAFE = True

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
_img_file_cache = {}

advertiseButtonOffset = 100

harvestSpeed = 0.4
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
    (-25, -4)
]

plantSpeed = 0.4
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

def get_scale_factor():
    try:
        screenshot = pyautogui.screenshot()
        screen_w_pts, _ = pyautogui.size()
        img_w, _ = screenshot.size
        if screen_w_pts <= 0:
            return 1.0
        scale = img_w / screen_w_pts
        if scale <= 0:
            return 1.0
        return scale
    except Exception:
        return 1.0

SCALE_FACTOR = get_scale_factor()

def _get_image_files(directory):
    cached = _img_file_cache.get(directory)
    if cached is not None:
        return cached

    full_directory = ASSETS_DIR / directory

    if not full_directory.exists():
        print(f"directory not found: {full_directory}")
        _img_file_cache[directory] = []
        return []

    image_files = [
        f for f in sorted(full_directory.iterdir())
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    _img_file_cache[directory] = image_files
    return image_files

def getImgLoc(directory, confidence=0.9, grayscale=False):
    image_files = _get_image_files(directory)

    for image_file in image_files:
        try:
            location = pyautogui.locateCenterOnScreen(str(image_file), confidence=confidence, grayscale=grayscale)
            if location:
                x, y = location
                return (x / SCALE_FACTOR, y / SCALE_FACTOR)
        except Exception:
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

def performDrag(start_pos, relative_points, speed):
    pyautogui.moveTo(start_pos)
    pyautogui.mouseDown(_pause=False, button="left")
    for point in relative_points:
        distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
        duration = distance * 0.01 * speed
        pyautogui.dragRel(point[0], point[1], duration=duration, mouseDownUp=False, button="left", _pause=False)
    pyautogui.mouseUp(_pause=False, button="left")

def attemptReset():
    print("resetting view")
    for i in range(2):
        reset = getImgLoc("misc/reset", confidence=0.8)
        if reset is None: 
            print(f"reset button not found (attempt {i+1}), manual help needed")
            input("check state, press enter to continue")
            reset = getImgLoc("misc/reset", confidence=0.8)
        if reset:
            print(f"clicking reset ({i+1}/2)")
            pyautogui.click(reset)
            time.sleep(0.5)
    print("reset done")

def runHarvest():
    print("checking for ready wheat")
    ready = getImgLoc("wheat/ready")
    if ready:
        print("found wheat, clicking")
        pyautogui.click(ready)
        time.sleep(1)
        scythe = getImgLoc("wheat/scythe", confidence=0.8)
        if scythe is None:
            print("scythe not found, resetting")
            attemptReset()
            return False

        print("harvesting")
        performDrag(scythe, relativeHarvestPoints, harvestSpeed)
        print("harvest done")
        return True
    else:
        print("no wheat ready")
        return False

def runPlant():
    print("checking for empty plots")
    plant = getImgLoc("wheat/plant")

    if plant is None:
        print("no empty plots found")
        return False

    print("found empty plot, clicking")
    pyautogui.click(plant)
    time.sleep(1)
    drag = getImgLoc("wheat/drag", confidence=0.8)
    if drag is None:
        print("wheat to drag not found, resetting")
        attemptReset()
        return False

    print("planting wheat")
    performDrag(drag, relativePlantPoints, plantSpeed)

    print("planting done, resetting")
    attemptReset()
    return True

def handleSelling():
    print("handling sales")
    closemenu = getImgLoc("misc/closemenu")
    if closemenu:
        pyautogui.click(closemenu)
    
    print("opening shop")
    shop = getImgLoc("shop/open")
    if shop:
        pyautogui.click(shop)
    time.sleep(0.5)

    soldItems = []
    try:
        sold_path = str(ASSETS_DIR / "shop/sold/sold.png")
        for box in pyautogui.locateAllOnScreen(sold_path, confidence=0.9):
            x, y = pyautogui.center(box)
            pos = (x / SCALE_FACTOR, y / SCALE_FACTOR)
            if not any(abs(pos[0] - p[0]) < 30 and abs(pos[1] - p[1]) < 30 for p in soldItems):
                soldItems.append(pos)
    except Exception:
        pass
    
    if soldItems:
        print(f"collecting {len(soldItems)} sold items")
        for sold in soldItems:
            pyautogui.click(sold)
        time.sleep(1)

    cachedClicks = None
    pass_num = 0
    max_passes = 4
    while True:
        pass_num += 1
        if pass_num > max_passes:
            print("max passes reached")
            break

        emptySlots = []
        try:
            createnew_path = str(ASSETS_DIR / "shop/createnew/createnew.png")
            for box in pyautogui.locateAllOnScreen(createnew_path, confidence=0.9):
                x, y = pyautogui.center(box)
                pos = (x / SCALE_FACTOR, y / SCALE_FACTOR)
                if any(abs(pos[0] - p[0]) < 30 and abs(pos[1] - p[1]) < 30 for p in emptySlots):
                    continue
                emptySlots.append(pos)
        except Exception:
            pass

        if not emptySlots:
            print("no empty slots found")
            break

        print(f"found {len(emptySlots)} empty slots (pass {pass_num}/{max_passes})")
        filled = 0

        for i, slot in enumerate(emptySlots):
            print(f"filling slot {i+1}/{len(emptySlots)}")
            pyautogui.click(slot)
            time.sleep(0.15)

            if cachedClicks:
                time.sleep(0.08)
                pyautogui.click(cachedClicks["wheat"])
                
                time.sleep(0.08)
                pyautogui.click(cachedClicks["maxprice"])

                time.sleep(0.12)
                pyautogui.click(cachedClicks["sale"])
                
                print("sale created")
                filled += 1
                continue

            wheat = getImgLoc("shop/wheattosell")
            if not wheat:
                print("wheat not found, skipping slot")
                continue
            pyautogui.click(wheat)

            maxprice = getImgLoc("shop/maxprice")
            if maxprice:
                pyautogui.click(maxprice)

            sale = getImgLoc("shop/putonsale")
            if not sale:
                print("sale button not found, skipping slot")
                continue
            pyautogui.click(sale)

            cachedClicks = {
                "wheat": wheat,
                "maxprice": maxprice,
                "sale": sale
            }
            print("cached button positions for remaining slots")
            print("sale created")
            filled += 1

        if filled == 0:
            print("no sales created this pass")
            break

    wheattoadvert = getImgLoc("shop/wheattoadvert")
    if wheattoadvert:
        print("advertising wheat sale")
        pyautogui.click(wheattoadvert)
        ad = getImgLoc("shop/advertisenow")
        if ad:
            pyautogui.click(ad[0] + advertiseButtonOffset, ad[1])
            createad = getImgLoc("shop/createad")
            if createad:
                pyautogui.click(createad)
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

def main():
    loop_count = 0
    try:
        while True:
            loop_count += 1
            print(f"loop {loop_count} at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            silofull = getImgLoc("shop/silofull")
            if silofull:
                print("silo full, selling")
                handleSelling()

            closeAllMenus()
            runHarvest()
            runPlant()

            print("loop done, waiting 1s")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nstopping script")


if __name__ == "__main__":
    main()
