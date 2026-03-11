from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import os
import sys

# For interacting with Android Java API
try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from android import activity
except ImportError:
    # Fallback for PC testing
    autoclass = None

class AndroidBubbleBot(App):
    def build(self):
        self.title = "zenumama click"
        self.running = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.status_label = Label(text="Status: Stopped", font_size='22sp', bold=True)
        layout.add_widget(self.status_label)
        
        # Start/Stop Button
        self.btn_toggle = Button(text="START BOT", background_color=(0, 0.7, 0, 1), font_size='25sp')
        self.btn_toggle.bind(on_press=self.toggle_bot)
        layout.add_widget(self.btn_toggle)
        
        # Accessibility Permission Button
        self.btn_acc = Button(text="OPEN ACCESSIBILITY SETTINGS", background_color=(0.2, 0.2, 0.8, 1), font_size='14sp')
        self.btn_acc.bind(on_press=self.open_accessibility_settings)
        layout.add_widget(self.btn_acc)
        
        # Exit Button
        self.btn_exit = Button(text="EXIT APP", background_color=(0.7, 0, 0, 1), font_size='18sp')
        self.btn_exit.bind(on_press=self.exit_app)
        layout.add_widget(self.btn_exit)
        
        self.info_label = Label(text="1. Open Settings -> 2. Enable BubbleBot Service\n3. Put images in 'targets' -> 4. Click START", 
                               font_size='12sp', color=(0.8, 0.8, 0.8, 1), halign='center')
        layout.add_widget(self.info_label)
        
        return layout

    def open_accessibility_settings(self, instance):
        if autoclass:
            try:
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                activity.start_activity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
                print("Opened Accessibility Settings")
            except Exception as e:
                print(f"Failed to open settings: {e}")
        else:
            print("Running on PC: Accessibility settings not available.")

    def exit_app(self, instance):
        print("Exiting App...")
        App.get_running_app().stop()
        sys.exit(0)

    def toggle_bot(self, instance):
        if not self.running:
            self.start_bot()
        else:
            self.stop_bot()

    def start_bot(self):
        self.running = True
        self.status_label.text = "Status: RUNNING"
        self.btn_toggle.text = "STOP BOT"
        self.btn_toggle.background_color = (0.7, 0, 0, 1) # Change to Red
        print("Bot Started")

    def stop_bot(self):
        self.running = False
        self.status_label.text = "Status: Stopped"
        self.btn_toggle.text = "START BOT"
        self.btn_toggle.background_color = (0, 0.7, 0, 1) # Change to Green
        print("Bot Stopped")

if __name__ == '__main__':
    AndroidBubbleBot().run()
