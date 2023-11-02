import time
import tkinter as tk
from pygame import mixer
from psutil import process_iter
from pycaw.pycaw import AudioUtilities
import tkinter as tk

class AudioManagement:
    def __init__(self, path_audio_file: str,audio_process_name: str, root: tk.Tk, volume: float = 0.3):
        self.path_audio_file = path_audio_file
        self.root = root        
        self.audio_process_name = audio_process_name
        self.volume = volume
            
    def play_audio(self):
        try:
            self.manager_pid_volume(self.volume)
            time.sleep(1)
            
            mixer.init()  # Initialize the mixer module for audio only

            mixer.music.load(self.path_audio_file)
            mixer.music.play()
            mixer.music.set_volume(1)

            while mixer.music.get_busy() == 1:
                time.sleep(1)
            self.manager_pid_volume(1)
            mixer.music.stop()  # Stop the music
            mixer.quit()  # Quit the mixer module
            
            self.root.deiconify()
        except Exception as e:
            print(f"Error playing audio: {e}")
            
            
    def repeat_audio(self):
        try:               
            self.play_audio()
            self.root.iconify()  # Minimize the window
        except Exception as e:
            print(f"Error playing audio: {e}")
            
            
    def manager_pid_volume(self ,volume_level=1):
        # Find PIDs associated with target and audio processes
        audio_pids = self.find_pids(self.audio_process_name)
        if not audio_pids:
            print(f"No processes found for {self.audio_process_name}.")
            return
        # Adjust the volume for the audio process
        for pid in audio_pids:
            self.set_volume_by_pid(pid, volume_level)        
        
        
    def set_volume_by_pid(self, pid, volume):
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
            
                    
    def find_pids(self, process_name):
        # Function to find PIDs associated with a process name
        pids = []
        for process in process_iter(attrs=['pid', 'name']):
            if process.info['name'] == process_name:
                pids.append(process.info['pid'])

        return pids
    