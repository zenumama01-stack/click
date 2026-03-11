[app]
title = zenumama click
package.name = zenumamaclick
package.domain = org.zia
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ico
version = 1.0
requirements = python3,kivy,pillow,numpy,opencv-python
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
# Entry point for Android
android.entrypoint = android_main.py
# Icon for Android
icon.filename = zia/icon256.ico
