import threading
import tkinter as tk
from gui.app_gui import FuturisticAssistantApp
from commands.reminder_manager import check_due_reminders
from commands.alarm_manager import check_alarms_loop
from commands.battery_status import monitor_battery_status  # ✅ added
import pygame
import os
import sys
from gui.app_gui import clean_exit
from gui.message_router import set_gui_instance

# Initialize Pygame mixer
pygame.mixer.init()

# Flag to manage global listening thread
listening_active = False

if __name__ == "__main__":
    # Start reminder checker thread
    reminder_thread = threading.Thread(target=check_due_reminders, daemon=True)
    reminder_thread.start()

    # Start alarm checker thread
    alarm_thread = threading.Thread(target=check_alarms_loop, daemon=True)
    alarm_thread.start()

    # ✅ Start battery monitoring thread
    battery_thread = threading.Thread(target=monitor_battery_status, daemon=True)
    battery_thread.start()

    # Launch GUI
    root = tk.Tk()
    app = FuturisticAssistantApp(root)
    set_gui_instance(app)  # ✅ set the GUI instance
    root.protocol("WM_DELETE_WINDOW", clean_exit)  # Ensure clean shutdown
    root.mainloop()
