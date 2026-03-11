import pyautogui
import os
import time
import win32gui
import win32api
import win32con

# Configuration
TARGET_FOLDER = 'targets'
CONFIDENCE = 0.8  # Adjust this (0.1 to 1.0) for better matching
SCAN_DELAY = 0.1  # Delay between scans (seconds)

def background_click(x, y):
    """
    Sends a click to the window at (x, y) without moving the mouse cursor.
    Note: Some games or applications may block this method.
    """
    try:
        # Find the window at the screen coordinates
        hwnd = win32gui.WindowFromPoint((x, y))
        
        # Convert screen coordinates to client (window) coordinates
        client_point = win32gui.ScreenToClient(hwnd, (x, y))
        lparam = win32api.MAKELONG(client_point[0], client_point[1])
        
        # Send Left Button Down and Up messages
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        time.sleep(0.05) # Small delay for reliability
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
        
        print(f"Background click sent to {win32gui.GetWindowText(hwnd)} at ({x}, {y})")
        return True
    except Exception as e:
        print(f"Background click failed: {e}")
        return False

def get_target_images():
    """
    Scans the targets folder for image files.
    """
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        return []
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    return [os.path.join(TARGET_FOLDER, f) for f in os.listdir(TARGET_FOLDER) 
            if f.lower().endswith(valid_extensions)]

def main():
    print("--- Game Target Clicker Bot ---")
    print(f"Place your target images in the '{TARGET_FOLDER}' folder.")
    print("The bot will wait for them to appear and click without moving the mouse.")
    print("Press Ctrl+C to stop the bot.\n")

    while True:
        target_images = get_target_images()
        
        if not target_images:
            print(f"\rNo images found in '{TARGET_FOLDER}'. Waiting...", end="")
            time.sleep(1)
            continue

        found_any = False
        for img_path in target_images:
            try:
                # Search for the image on screen
                # Using grayscale=True for faster matching
                location = pyautogui.locateCenterOnScreen(img_path, confidence=CONFIDENCE, grayscale=True)
                
                if location:
                    x, y = int(location.x), int(location.y)
                    print(f"\nTarget found: {os.path.basename(img_path)} at ({x}, {y})")
                    
                    # Attempt background click
                    background_click(x, y)
                    
                    # Prevent multiple clicks on the same appearance
                    time.sleep(1) 
                    found_any = True
                    break # Skip other images in this scan
            except Exception as e:
                # PyScreeze error if image is not found or other issues
                pass

        if not found_any:
            # Simple indicator that it's scanning
            print(".", end="", flush=True)
            time.sleep(SCAN_DELAY)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
