import os
import subprocess
import shutil

def build():
    script_name = "bubble_bot.py"
    app_name = "zenumama click"
    icon_path = os.path.join("zia", "icon256.ico")
    
    print("--- Starting Build Process ---")
    
    # 1. Build Single File EXE
    print("\nBuilding Single-File EXE...")
    subprocess.run([
        "py", "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--icon", icon_path,
        "--name", f"{app_name}_Standalone",
        "--add-data", f"zia;zia",
        script_name
    ])
    
    # 2. Build Directory (for Installer)
    print("\nBuilding Directory-based App (Installer Ready)...")
    subprocess.run([
        "py", "-m", "PyInstaller",
        "--noconsole",
        "--icon", icon_path,
        "--name", f"{app_name}_Package",
        "--add-data", f"zia;zia",
        script_name
    ])
    
    print("\n--- Build Complete! ---")
    print(f"Check the 'dist' folder for your files:")
    print(f"1. {app_name}_SingleFile.exe (Standalone)")
    print(f"2. {app_name}_InstallerReady/ (Folder for installer)")

if __name__ == "__main__":
    build()
