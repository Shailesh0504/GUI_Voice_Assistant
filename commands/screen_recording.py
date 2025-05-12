# commands/screen_recording.py

import threading
import pyautogui
import cv2
import numpy as np
import datetime
import os
from core.registry import register_command
from core.voice_output import speak

recording = False
writer = None
filename = None
record_thread = None

@register_command("start screen recording")
def start_screen_recording(params=None):
    global recording, writer, filename, record_thread

    if recording:
        return "🟥 A screen recording is already in progress. Say 'stop screen recording' first."

    screen_size = pyautogui.size()
    frame_width = screen_size[0]
    frame_height = screen_size[1]

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    recordings_dir = "recordings"
    os.makedirs(recordings_dir, exist_ok=True)
    filename = os.path.join(recordings_dir, f"screen_recording_{now}.avi")

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(filename, fourcc, 8.0, (frame_width, frame_height))

    recording = True

    def record():
        global recording, writer
        try:
            while recording:
                img = pyautogui.screenshot()
                frame = np.array(img)

                # OpenCV expects BGR, not RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if writer is not None:
                    try:
                        writer.write(frame)
                    except Exception as e:
                        print(f"⚠️ Error writing frame: {e}")
                        break
        except Exception as e:
            print(f"🚨 Screen recording thread crashed: {e}")

    record_thread = threading.Thread(target=record, daemon=True)
    record_thread.start()

    speak("🎥 Started screen recording.")
    return "🎥 Started screen recording."

@register_command("stop screen recording")
def stop_screen_recording(params=None):
    global recording, writer, filename

    if not recording:
        return "⛔ No screen recording is currently active."

    recording = False
    if writer is not None:
        writer.release()
        writer = None

    speak(f"🛑 Screen recording stopped. Saved as {filename}")
    return f"🛑 Screen recording stopped. Saved as {filename}"
