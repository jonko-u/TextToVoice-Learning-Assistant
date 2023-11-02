import os
import re
from transformers import VitsModel, AutoTokenizer
import torch
import numpy as np
import soundfile as sf
import tkinter as tk
from PIL import ImageGrab
import pytesseract
from IPython.display import Audio
from playsound import playsound
import pygame
from pygame import mixer
import psutil
from pycaw.pycaw import AudioUtilities
import time
model = VitsModel.from_pretrained("facebook/mms-tts-eng")


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path_directory = r"C:\wav"

audio_process_name = "firefox.exe"

path_audio = f"screen_shot1.wav"
left = 0
top = 0
width = 0
height = 0
path = os.path.join(path_directory, path_audio)

def find_pids(process_name):
    # Function to find PIDs associated with a process name
    pids = []


    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            pids.append(process.info['pid'])

    return pids

def set_volume_by_pid(pid, volume):
    # Function to set the volume for a specific process (by PID)

    audio_sessions = AudioUtilities.GetAllSessions()

    for session in audio_sessions:
        volume_interface = session.SimpleAudioVolume
        if session.Process and session.Process.pid == pid:
            try:
                # mute_status = get_mute_status_by_pid(pid)
                print(session)
                volume_interface.SetMasterVolume(volume, None)
                print(f"Mute status for PID {pid}: ")
            except Exception as e:
                # Handle other exceptions (the 'as' keyword allows you to access the exception object)
                print(f"An error occurred: {e}")

def manager_pid_volume(volume_level=1):
    # Find PIDs associated with target and audio processes
    audio_pids = find_pids(audio_process_name)
    print(audio_pids)
    if not audio_pids:
        print(f"No processes found for {audio_process_name}.")
        return

    # Adjust the volume for the audio process
    for pid in audio_pids:
        set_volume_by_pid(pid, volume_level)

    print(f"Adjusted volume for {audio_process_name} processes.")

def save_audio(output, path_audio, path_directory):
    try:
        # Determine the maximum length of all chunks
        samplerate = model.config.sampling_rate  # Sample rate
        channels = 1  # Mono audio
        subtype = 'PCM_16'  # 16-bit PCM audio
        endian = 'FILE'  # Little-endian
        format = 'WAV'
        print("CHECKPOINT")

        audio_data = np.array(output).copy()

        print(audio_data)
        audio_data = audio_data[0]
        path = os.path.join(path_directory, path_audio)
        # Check if the file "screen_shot.wav" exists and delete it if it does
        print(path)
        try:
            pygame.mixer.music.stop()  # Stop the music
            pygame.mixer.quit()  # Quit the mixer module
        except:
            pass
        with sf.SoundFile(path, 'w', samplerate, channels, subtype, endian, format, closefd=True) as f:
            f.write(audio_data)
        f.close()

    except:
        print("save_audio_function")
def use_model(text):

    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    return output

def repeat_audio():
    try:
        pygame.mixer.music.stop()  # Stop the music
        pygame.mixer.quit()  # Quit the mixer module
        play_audio(path=path)
        root.iconify()  # Minimize the window
    except Exception as e:
        print(f"Error playing audio: {e}")

def update_position():
    global left, top, width, height
    x1 = root.winfo_x()
    y1 = root.winfo_y()
    width = root.winfo_width()
    height = root.winfo_height()
    left = x1
    top = y1
    root.after(100, update_position)  # Update every 100 milliseconds

def capture_screenshot():
    root.iconify()  # Minimize the window
    screenshot = ImageGrab.grab(bbox=(left + 10, top + 20, left + width, top + height))

    try:
        output = read_screenshot(screenshot)
        try:
            print(output)
            save_audio(output=output, path_audio=path_audio, path_directory=path_directory)
        except:
            print("ERROR SAVING")
    except:
        print("ERROR")
    play_audio(path=path)

def read_screenshot(screenshot):
    text = pytesseract.image_to_string(screenshot)
    cleaned_text = text.replace("\n", " \n ")
    output = use_model(cleaned_text)
    return output


def play_audio(path):
    try:
        manager_pid_volume(0.3)
        time.sleep(1)
        pygame.mixer.init()
        mixer.init()  # Initialize the mixer module for audio only

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == 1:
            time.sleep(1)
        manager_pid_volume(1)
        root.deiconify()
    except Exception as e:
        print(f"Error playing audio: {e}")

def replace_newlines(text):
    # Define a regular expression pattern to match the desired pattern
    pattern = r'(\S)\n(\S)'

    # Use re.sub to replace the matched pattern with a space
    modified_text = re.sub(pattern, r'\1 \2', text)

    return modified_text

root = tk.Tk()
root.title("Transparent Window with Blue Borders")
root.attributes('-alpha', 0.5)

border_frame = tk.Frame(root, bg="white", borderwidth=2)
border_frame.pack(fill="both", expand=True)

# Create a "Screenshot" button
screenshot_button = tk.Button(root, text="Capture & Play", command=capture_screenshot)
screenshot_button.pack()

# Create a "Repeat" button
repeat_button = tk.Button(root, text="Repeat", command=repeat_audio)
repeat_button.pack()



# Start the update loop
update_position()

root.mainloop()