import pyautogui
import time

print("1. Open your game/app.")
print("2. Move your mouse EXACTLY over the 'open_slot' button.")
print("3. Wait 3 seconds...")
time.sleep(3)

# Get current mouse position
x, y = pyautogui.position()

# We need to capture a small box around the mouse.
# However, on Retina, we need to handle the density carefully.
# We will grab a screenshot of the WHOLE screen, then crop it in memory.
# This ensures the density matches what locateOnScreen uses.

# Move mouse away so it's not in the picture
pyautogui.move(-200, 0)
time.sleep(0.5)

print("Capturing...")
screenshot = pyautogui.screenshot()

# Because of Retina, the screenshot might be 2x larger than the coordinates.
# We need to check the scale factor.
screen_w_pts, screen_h_pts = pyautogui.size()
img_w, img_h = screenshot.size

scale = img_w / screen_w_pts
print(f"Detected Scale Factor: {scale}x")

# Calculate the crop box in PIXELS (not points)
crop_size = 20 # Size of the button image you want (adjust as needed)
crop_x = int(x * scale) - (crop_size // 2)
crop_y = int(y * scale) - (crop_size // 2)

# Ensure we don't crop outside bounds
crop_x = max(0, crop_x)
crop_y = max(0, crop_y)

# Crop and save
button_img = screenshot.crop((crop_x, crop_y, crop_x + crop_size, crop_y + crop_size))
button_img.save('./assets/new.png')

print("Check this image. If it looks correct, use THIS file for your locator.")