import tkinter as tk
import os
from utils.model_settings import ModelingLocal
from utils.audio import AudioManagement
from PIL import ImageGrab
import logging
import pytesseract
from utils.mongo_db import DbManagement

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



class AppInterface:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("Transparent Window with Blue Borders")
        self.root.attributes('-alpha', 0.5)
        self.top = 0
        self.left = 0
        self.width = 0
        self.heigth = 0
        self.audio_process_name = "firefox.exe"
        self.path_windows_directory = r'j:\\PycharmProjects\\screenshot-text\\wav\\'
        self.create_language_buttons()
        self.update_position()
        self.capture_count = 0  # Initialize the capture counter
        
    def create_language_buttons(self):
        languages = {
            "English": {
                "audio_file": "english.wav",
                "model_local_path": 'j:/huggingface/hub/facebook/mms-tts-eng',
                "config": 'j:/huggingface/hub/facebook/mms-tts-eng/config.json',
            },
            "Spanish": {
                "audio_file": "spanish.wav",
                "model_local_path": 'j:/huggingface/hub/facebook/mms-tts-spa',
                "config": 'j:/huggingface/hub/facebook/mms-tts-spa/config.json',
            }
        }
        lang_frame = tk.Frame(self.root, bg="blue", borderwidth=2, height=10)
        lang_frame.pack(side='bottom', fill='x')
        # Set a maximum height of 20 pixels for the button bar
        # Divide the button bar into two halves with a right_frame
        right_frame = tk.Frame(lang_frame)
        right_frame.pack(side="right", fill="y", padx=10)  # Adjust padx as needed

        # Create a green button in the right half
        green_button = tk.Button(right_frame, text="Green Button", bg="green", command= self.capture_screenshot_to_db)
        green_button.pack(side="right")
        
        for lang, lang_data in languages.items():
            
            audio_management, modeling_local = self.load_audio_model_template(lang_data)
            path_audio_file = os.path.join(self.path_windows_directory, lang_data["audio_file"])

            # Create "Capture & Play" button and align it to the bottom of lang_frame
            screenshot_button = tk.Button(lang_frame, text=f"Capture & Play ({lang})", command=lambda path=path_audio_file, audio_management=audio_management, modeling_local=modeling_local: self.capture_screenshot(audio_management=audio_management, modeling_local=modeling_local, path_audio_file=path))
            screenshot_button.pack(side="left")

            # Create "Repeat" button and align it to the bottom of lang_frame
            repeat_button = tk.Button(lang_frame, text=f"Repeat ({lang})", command=lambda: audio_management.repeat_audio())
            repeat_button.pack(side="left")


    
    def load_audio_model_template(self, lang_data):
        
        path_audio_file = os.path.join(self.path_windows_directory, lang_data["audio_file"])
        logging.warning(path_audio_file)
        model_local_path = lang_data["model_local_path"]
        logging.warning(model_local_path)
        config = lang_data["config"]
        
        # Add your logic to load audio models here
        audio_management = AudioManagement(path_audio_file=path_audio_file, audio_process_name=self.audio_process_name, root=self.root)

        modeling_local = ModelingLocal(model_local_path=model_local_path, config=config)
        
        return audio_management, modeling_local
    
    def update_position(self):        
        self.width = 500
        self.height = 500
        x1 = self.root.winfo_x()
        y1 = self.root.winfo_y()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.left = x1
        self.top = y1
        self.root.after(100, self.update_position)  # Update every 100 milliseconds
    
    def capture_screenshot(self, audio_management, modeling_local, path_audio_file):
        self.root.iconify()  # Minimize the window
        screenshot = ImageGrab.grab(bbox=(self.left + 10, self.top + 20, self.left + self.width, self.top + self.height))

        try:        
            tensor_audio = modeling_local.read_screenshot(screenshot)
            modeling_local.save_audio(tensor_audio=tensor_audio, path_output_file=path_audio_file)        
        except Exception as e:
            print(e)
        audio_management.play_audio()
        
    def capture_screenshot_to_db(self):
        screenshot = ImageGrab.grab(bbox=(self.left + 10, self.top + 20, self.left + self.width, self.top + self.height))
        print(screenshot)
        text = pytesseract.image_to_string(screenshot)
        cleaned_text = text.replace("\n", " \n ")
        print(cleaned_text)
        n_subjects = 15
        name_module = 'Empresa e iniciativa emprendedora'
        subject = 'La Iniciativa Emprendedora'
        self.capture_count += 1
        db_management = DbManagement(n_subjects=n_subjects, text=cleaned_text, name_module=name_module, subject=subject)
        db_management.add_text_to_db(page_iterator=self.capture_count)
        