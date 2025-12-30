import pyautogui
import time
from pathlib import Path

print("1. Open your game/app.")
print("2. Move your mouse EXACTLY over the target button.")
subdir = input("Enter subfolder under assets (ex: wheat/ready), blank for root: ").strip().strip("/")
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

crop_size = 50
crop_x = int(x * scale) - (crop_size // 2)
crop_y = int(y * scale) - (crop_size // 2)
crop_x = max(0, crop_x)
crop_y = max(0, crop_y)

button_img = screenshot.crop((crop_x, crop_y, crop_x + crop_size, crop_y + crop_size))
assets_dir = Path(__file__).resolve().parent / "assets"
target_dir = assets_dir / subdir if subdir else assets_dir
target_dir.mkdir(parents=True, exist_ok=True)
out_path = target_dir / f"{image_name}.png"
button_img.save(str(out_path))

print(f"Image saved as '{out_path}'. Check this image before using it as a locator.")