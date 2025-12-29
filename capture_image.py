import pyautogui
import time

print("1. Open your game/app.")
print("2. Move your mouse EXACTLY over the target button.")
image_name = input("Enter a name for the image (without extension): ").strip()
if not image_name:
    image_name = "new"
print("3. Wait 3 seconds...")
time.sleep(3)

x, y = pyautogui.position()
pyautogui.move(-200, 0)
time.sleep(0.5)

print("Capturing...")
screenshot = pyautogui.screenshot()

screen_w_pts, screen_h_pts = pyautogui.size()
img_w, img_h = screenshot.size
scale = img_w / screen_w_pts
print(f"Detected Scale Factor: {scale}x")

crop_size = 40
crop_x = int(x * scale) - (crop_size // 2)
crop_y = int(y * scale) - (crop_size // 2)
crop_x = max(0, crop_x)
crop_y = max(0, crop_y)

button_img = screenshot.crop((crop_x, crop_y, crop_x + crop_size, crop_y + crop_size))
button_img.save(f'./assets/{image_name}.png')

print(f"Image saved as './assets/{image_name}.png'. Check this image before using it as a locator.")