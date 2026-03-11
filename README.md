# zenumama click

A cross-platform GUI automation bot for Windows and Android.

## Features
- **Floating Bubble UI**: Control the bot from anywhere.
- **Background Click**: Clicks without moving your mouse cursor (Windows).
- **Image Recognition**: Automatically finds and clicks targets from the `targets` folder.
- **Cross-Platform**: Support for Windows (.exe) and Android (.apk).

## Setup
1. Place your target images in the `targets/` folder.
2. Run the application.
3. Click **START** to begin automation.

## Build
- Windows: Use `build_win.py` to generate EXE.
- Android: Use `buildozer` with `android_main.py` and `buildozer.spec`.
