import pytesseract
from transformers import VitsModel, AutoTokenizer, AutoConfig
import torch
import numpy as np
import soundfile as sf

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# model_local_path = 'j:\\huggingface\\hub\\facebook\\mms-tts-eng'
# config = 'j:\\huggingface\\hub\\facebook\\mms-tts-eng\\config.json'


class ModelingLocal:
    
    def __init__(self, model_local_path, config):
        self.model_local_path = model_local_path
        self.config = config
        self.model = VitsModel.from_pretrained(self.model_local_path)     

    def use_model(self, text):                
        tokenizer = AutoTokenizer.from_pretrained(self.model_local_path)
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**inputs).waveform   
        return output


    def read_screenshot(self, screenshot):
        text = pytesseract.image_to_string(screenshot)
        cleaned_text = text.replace("\n", " \n ")
        tensor_audio = self.use_model(cleaned_text)
        return tensor_audio
    
    def save_audio(self, tensor_audio, path_output_file):
        try:
            # Determine the maximum length of all chunks
            samplerate = self.model.config.sampling_rate  # Sample rate
            channels = 1  # Mono audio
            subtype = 'PCM_16'  # 16-bit PCM audio
            endian = 'FILE'  # Little-endian
            format = 'WAV'
            audio_data = np.array(tensor_audio)
            audio_data = audio_data[0]        
            with sf.SoundFile(path_output_file, 'w', samplerate, channels, subtype, endian, format, closefd=True) as f:
                f.write(audio_data)
            f.close()

        except:
            print("save_audio_function")
            