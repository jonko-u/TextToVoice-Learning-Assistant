
# TextToVoice Learning Assistant: Your Learning Companion


![Screenshot](/screenshots/screenshot1.jpg)



## Introduction

TextToVoice Learning Assistant is a Python application built for students to enhance their learning experience. It offers a unique set of features that streamline the process of capturing text from a tkinter window, converting it to speech in both English and Spanish, and saving this data in a MongoDB database for future use. This README provides an overview of the project, its context, features, technologies, and future developments.

## Context and Problem Statement

Many students today face challenges in comprehending textual content, especially when dealing with multiple languages. There is a need for a tool that can help students capture and understand text content easily. Additionally, having a way to store this text for later reference can be invaluable.

## Solution

TextToVoice Learning Assistant addresses these challenges by offering a comprehensive solution that combines text capture, text-to-speech conversion, and database storage. It simplifies the process of capturing text content from a tkinter window, provides the ability to convert this text into both English and Spanish speech, and saves the captured text in a MongoDB database. This database can serve as a knowledge repository for future use.

## Technologies Used

- Python: The core programming language for building the application.
- Tkinter: Used for creating the graphical user interface for text capture.
- Tesseract OCR: Employed to extract text content from the tkinter window.
- Hugging Face AI Models: Utilized for text-to-speech conversion in both English and Spanish.
- MongoDB: The database system used for storing the captured text content.
- PID sound controller: If the speech is playing it modifies the volume of pid of "firefox.exe".

## Features

TextToVoice Learning Assistant currently offers the following features:

1. **Text Capture**: The application captures text from the tkinter window with the help of Tesseract OCR.

2. **Text-to-Speech Conversion**: It can convert the captured text to speech in both English and Spanish using Hugging Face AI models.

3. **Database Storage**: Captured text can be saved in a MongoDB database for future reference.

## Future Features

Here are some potential features that can be added to enhance the project in the future:

1. **Translation**: Add a feature to translate captured text between various languages, further improving language learning capabilities.

2. **Chatbot Integration**: Implement a chatbot system that can interact with the stored text content in MongoDB, providing a conversational AI experience for students.

3. **User Profiles**: Allow users to create profiles and customize their learning experience, track their progress, and personalize the AI assistant.

4. **Improved User Interface**: Enhance the graphical user interface for a more user-friendly experience.

5. **Text Summarization**: Implement text summarization algorithms to condense long texts for better comprehension.

## How to Use TextToVoice Learning Assistant
```
Download the facebook/mms-tts-eng and facebook/mms-tts-spa from hugging face
```

```
python -m venv venv
```
```
pip install -r requirements.txt
```
```
python run.py
```


## Contributors


- jonko-u - Developer


## License

Free
## Acknowledgments

We would like to extend our gratitude to the following individuals and organizations for their contributions and support to this project:

- [MongoDB](https://www.mongodb.com/): We are thankful for MongoDB's powerful and reliable database system, which enables us to store and manage captured text data efficiently.

- [Python](https://www.python.org/): Python's versatility and ease of use played a crucial role in the development of this project. It served as the foundation for our application.

- [PyTesseract](https://github.com/madmaze/pytesseract): We acknowledge the PyTesseract library for its text recognition capabilities, which allowed us to capture text from tkinter windows effectively.

- [Hugging Face](https://huggingface.co/): The immense efforts of the people at Hugging Face in developing state-of-the-art AI models for text-to-speech conversion have been indispensable. Their models have greatly enhanced the user experience in our project.

---

