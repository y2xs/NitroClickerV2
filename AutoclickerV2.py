import os
import sys
import tkinter as tk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import customtkinter as ctk
import threading
import time
import random
import winsound
from pynput.mouse import Button, Controller
from pynput import keyboard

# --- Configuration for the Modern UI ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AutoClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("NITRO CLICKER v2.0")
        self.geometry("420x650") # Increased height for new panel
        self.resizable(False, False)
        
        try:
            self.icon_path = resource_path("AutoClickerPicture.png")
            self.icon_image = tk.PhotoImage(file=self.icon_path)
            self.iconphoto(False, self.icon_image)
        except Exception as e:
            print(f"Icon could not be loaded: {e}")

        # --- State Variables ---
        self.running = False
        self.mouse = Controller()
        self.click_thread = None
        
        # --- Hotkey State ---
        self.start_stop_key = keyboard.Key.f6 # Default hotkey
        self.listening_for_hotkey = False
        
        # --- Default Settings ---
        self.delay = 0.1 
        self.random_range = 0.01 
        self.button_target = Button.left
        self.double_click = False

        # --- UI Layout ---
        self.setup_ui()

        # --- Hotkey Listener ---
        # We start the listener in a non-blocking way
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def setup_ui(self):
        """Constructs the Gamer Aesthetic UI"""
        
        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="NITRO CLICKER", 
            font=("Orbitron", 26, "bold"),
            text_color="#00E5FF" # Cyberpunk Cyan
        )
        self.title_label.pack()

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="STATUS: STOPPED",
            font=("Roboto Medium", 14),
            text_color="#FF3333" # Red
        )
        self.status_label.pack(pady=(5, 0))

        # 2. Settings Container
        self.settings_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.settings_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # -- Interval Settings --
        self.create_label(self.settings_frame, "Click Interval (ms):")
        self.entry_interval = ctk.CTkEntry(self.settings_frame, placeholder_text="100")
        self.entry_interval.insert(0, "100")
        self.entry_interval.pack(pady=5)

        self.create_label(self.settings_frame, "Random Delay (ms):")
        self.entry_random = ctk.CTkEntry(self.settings_frame, placeholder_text="10")
        self.entry_random.insert(0, "10")
        self.entry_random.pack(pady=5)

        # -- Mouse Options --
        self.create_label(self.settings_frame, "Mouse Button:")
        self.btn_selection = ctk.CTkSegmentedButton(
            self.settings_frame, 
            values=["Left", "Right"],
            selected_color="#00E5FF",
            text_color_disabled="#666"
        )
        self.btn_selection.set("Left")
        self.btn_selection.pack(pady=5)

        self.create_label(self.settings_frame, "Click Type:")
        self.type_selection = ctk.CTkSegmentedButton(
            self.settings_frame, 
            values=["Single", "Double"],
            selected_color="#00E5FF"
        )
        self.type_selection.set("Single")
        self.type_selection.pack(pady=5)

        # -- Hotkey Configuration Panel --
        self.create_label(self.settings_frame, "Start/Stop Hotkey:")
        
        self.hotkey_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.hotkey_frame.pack(pady=5)

        # Label showing current key
        self.hotkey_display = ctk.CTkLabel(
            self.hotkey_frame,
            text="[ F6 ]",
            font=("Roboto Mono", 14, "bold"),
            text_color="#00E5FF"
        )
        self.hotkey_display.pack(side="left", padx=10)

        # Button to change key
        self.change_hotkey_btn = ctk.CTkButton(
            self.hotkey_frame,
            text="CHANGE KEY",
            command=self.start_hotkey_recording,
            fg_color="#444444",
            hover_color="#555555",
            width=100,
            height=25,
            font=("Roboto", 10)
        )
        self.change_hotkey_btn.pack(side="left")

        # 3. Footer / Main Control
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(pady=20)
        
        self.toggle_btn = ctk.CTkButton(
            self.footer_frame,
            text="START",
            command=self.manual_toggle,
            fg_color="#00E5FF",
            text_color="#000000",
            hover_color="#00B2CC",
            font=("Roboto", 16, "bold"),
            width=200,
            height=40
        )
        self.toggle_btn.pack(pady=10)

    def create_label(self, parent, text):
        """Helper to create consistent labels"""
        label = ctk.CTkLabel(parent, text=text, text_color="#dce4ee", font=("Roboto", 12))
        label.pack(pady=(12, 2))

    # --- Hotkey Management ---

    def start_hotkey_recording(self):
        """Enables 'listening' mode to capture the next key press"""
        self.listening_for_hotkey = True
        self.change_hotkey_btn.configure(text="PRESS KEY...", fg_color="#FFAA00", text_color="black")
        self.hotkey_display.configure(text_color="#FFAA00")

    def format_key_name(self, key):
        """Cleans up the key name for display (e.g., 'Key.f6' -> 'F6')"""
        raw_name = str(key)
        # Remove 'Key.' prefix if present
        clean_name = raw_name.replace("Key.", "")
        # Remove single quotes if present (e.g., 'a' -> a)
        clean_name = clean_name.replace("'", "")
        return clean_name.upper()

    def on_key_press(self, key):
        """Global Keyboard Listener"""
        
        # MODE A: Recording a new hotkey
        if self.listening_for_hotkey:
            self.start_stop_key = key
            self.listening_for_hotkey = False
            
            # Update UI via .after() to keep it thread-safe
            display_text = f"[ {self.format_key_name(key)} ]"
            
            def update_hotkey_ui():
                self.hotkey_display.configure(text=display_text, text_color="#00E5FF")
                self.change_hotkey_btn.configure(text="CHANGE KEY", fg_color="#444444", text_color="white")
            
            self.after(0, update_hotkey_ui)
            return

        # MODE B: Normal Operation (Check for Start/Stop)
        if key == self.start_stop_key:
            self.after(0, self.toggle_clicking)

    # --- Core Logic ---

    def manual_toggle(self):
        """Button trigger"""
        self.toggle_clicking()

    def toggle_clicking(self):
        """Switches state between Running and Stopped"""
        if self.running:
            self.stop_clicker()
        else:
            self.start_clicker()

    def start_clicker(self):
        # 1. Update State
        self.running = True
        
        # 2. Update UI
        self.status_label.configure(text="STATUS: ACTIVE", text_color="#00FF00") # Green
        self.toggle_btn.configure(text="STOP", fg_color="#FF3333", hover_color="#CC0000")
        
        # 3. Parse Inputs
        try:
            self.delay = int(self.entry_interval.get()) / 1000.0
            self.random_range = int(self.entry_random.get()) / 1000.0
        except ValueError:
            self.delay = 0.03
            self.random_range = 0.001
        
        # Set Mouse Button
        if self.btn_selection.get() == "Left":
            self.button_target = Button.left
        else:
            self.button_target = Button.right

        # Set Click Type
        self.double_click = (self.type_selection.get() == "Double")

        # 4. Audio Feedback
        winsound.PlaySound("Switch.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # High pitch

        # 5. Start Thread
        self.click_thread = threading.Thread(target=self.click_loop)
        self.click_thread.daemon = True 
        self.click_thread.start()

    def stop_clicker(self):
        # 1. Update State
        self.running = False
        
        # 2. Update UI
        self.status_label.configure(text="STATUS: STOPPED", text_color="#FF3333")
        self.toggle_btn.configure(text="START", fg_color="#00E5FF", hover_color="#00B2CC")
        
        # 3. Audio Feedback
        winsound.PlaySound("SwitchLow.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) # Low pitch

    def click_loop(self):
        """The threaded engine that performs the clicking"""
        while self.running:
            # Perform Click
            self.mouse.click(self.button_target, 2 if self.double_click else 1)
            
            # Calculate Wait Time (Base + Random)
            actual_delay = self.delay + random.uniform(0, self.random_range)
            
            time.sleep(actual_delay)

# --- Application Entry Point ---
if __name__ == "__main__":
    app = AutoClickerApp()
    
    # Handle clean exit
    def on_close():
        app.running = False
        app.destroy()
        import sys
        sys.exit(0)
        
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
