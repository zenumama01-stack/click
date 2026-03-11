import tkinter as tk
import threading
import time
import os
import sys
import pyautogui
import win32gui
import win32api
import win32con
import ctypes

# Enable DPI awareness for Windows (Critical for accurate coordinates)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# Configuration
# Determine the base path (where the .exe or script is located)
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

TARGET_FOLDER = os.path.join(BASE_PATH, 'targets')
DEFAULT_CONFIDENCE = 0.7
SCAN_DELAY = 0.1

class BubbleBot:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.click_mode = "background"
        self.confidence = DEFAULT_CONFIDENCE
        self.bot_thread = None
        
        # Ensure targets folder exists immediately
        if not os.path.exists(TARGET_FOLDER):
            os.makedirs(TARGET_FOLDER)
            print(f"Created folder: {TARGET_FOLDER}")
        
        # Setup window
        self.root.title("zenumama click")
        
        # Set Icon if exists
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zia", "icon256.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass
                
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("100x120+100+100")
        self.root.configure(bg="#1e1e1e")
        
        # UI Elements...
        self.btn_toggle = tk.Button(self.root, text="START", bg="#ff4444", fg="white", 
                               command=self.toggle_bot, font=("Arial", 9, "bold"), height=2)
        self.btn_toggle.pack(fill="x", padx=5, pady=5)
        
        # Click Mode Toggle Button
        self.btn_mode = tk.Button(self.root, text="MODE: BACK", bg="#4444ff", fg="white", 
                                 command=self.toggle_mode, font=("Arial", 8))
        self.btn_mode.pack(fill="x", padx=5, pady=2)

        # Confidence Label
        self.lbl_conf = tk.Label(self.root, text=f"CONF: {self.confidence}", bg="#1e1e1e", fg="gray", font=("Arial", 7))
        self.lbl_conf.pack(fill="x")
        
        # Spacer
        tk.Label(self.root, bg="#1e1e1e", height=1).pack()

        # Exit/Close Button (Clearer Exit Option)
        self.btn_exit = tk.Button(self.root, text="EXIT APP", bg="#444444", fg="#ff4444", 
                                 command=self.exit_app, font=("Arial", 8, "bold"), bd=0)
        self.btn_exit.pack(fill="x", side="bottom", padx=5, pady=5)
        
        # Draggable feature on window background
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        
        self.drag_start_x = 0
        self.drag_start_y = 0

    def exit_app(self):
        print("Exiting Windows App...")
        self.running = False
        self.root.destroy()
        sys.exit(0)

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_start_x)
        y = self.root.winfo_y() + (event.y - self.drag_start_y)
        self.root.geometry(f"+{x}+{y}")

    def toggle_mode(self):
        if self.click_mode == "background":
            self.click_mode = "standard"
            self.btn_mode.config(text="MODE: STD", bg="#ffa500")
            print("Switched to Standard Click Mode (Cursor will move)")
        else:
            self.click_mode = "background"
            self.btn_mode.config(text="MODE: BACK", bg="#4444ff")
            print("Switched to Background Click Mode (Cursor won't move)")

    def toggle_bot(self):
        if not self.running:
            self.start_bot()
        else:
            self.stop_bot()

    def start_bot(self):
        self.running = True
        self.btn_toggle.config(text="STOP", bg="#00c851")
        self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
        self.bot_thread.start()
        print(f"Bot Started | Mode: {self.click_mode} | Conf: {self.confidence}")

    def stop_bot(self):
        self.running = False
        self.btn_toggle.config(text="START", bg="#ff4444")
        print("Bot Stopped")

    def perform_click(self, x, y):
        if self.click_mode == "background":
            try:
                hwnd = win32gui.WindowFromPoint((x, y))
                # Check if window is not the bot itself
                if hwnd == self.root.winfo_id():
                    return False
                    
                client_point = win32gui.ScreenToClient(hwnd, (x, y))
                lparam = win32api.MAKELONG(client_point[0], client_point[1])
                win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
                time.sleep(0.05)
                win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
                print(f"Background Click @ ({x}, {y})")
                return True
            except Exception as e:
                print(f"Background Click Error: {e}")
                return False
        else:
            # Standard click (more reliable but moves mouse)
            pyautogui.click(x, y)
            print(f"Standard Click @ ({x}, {y})")
            return True

    def get_target_images(self):
        if not os.path.exists(TARGET_FOLDER):
            os.makedirs(TARGET_FOLDER)
            return []
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        return [os.path.join(TARGET_FOLDER, f) for f in os.listdir(TARGET_FOLDER) 
                if f.lower().endswith(valid_extensions)]

    def bot_loop(self):
        while self.running:
            target_images = self.get_target_images()
            if not target_images:
                time.sleep(1)
                continue

            found_any = False
            for img_path in target_images:
                try:
                    # Search with slightly lower confidence and WITHOUT grayscale for better precision if color matters
                    location = pyautogui.locateCenterOnScreen(img_path, confidence=self.confidence)
                    
                    if location:
                        self.perform_click(int(location.x), int(location.y))
                        time.sleep(1) # Delay after click
                        found_any = True
                        break
                except Exception:
                    pass
            
            if not found_any:
                time.sleep(SCAN_DELAY)

if __name__ == "__main__":
    root = tk.Tk()
    app = BubbleBot(root)
    root.mainloop()
