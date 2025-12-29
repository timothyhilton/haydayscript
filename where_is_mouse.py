import pyautogui
import time
import threading
import sys

saved_points = []

def wait_for_enter():
    # Waits for Enter, saves a point from main thread's global scope
    global waiting
    try:
        while True:
            input()  # blocks until Enter is pressed
            x, y = pyautogui.position()
            saved_points.append((x, y))
            print(f"\nSaved point: ({x}, {y})")
    except EOFError:
        pass  # gracefully exit on EOF

waiting = True
t = threading.Thread(target=wait_for_enter, daemon=True)
t.start()

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})", end='\r', flush=True)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nExiting.")
    if saved_points:
        print("Saved points:")
        for idx, pt in enumerate(saved_points):
            print(f"  {idx+1}: {pt}")
    else:
        print("No points saved.")

