import os
from pathlib import Path
import speech_recognition as sr
import pyttsx3 
import pygame
from src.components.voicesynth import VoiceSynthesizer
from src.logger.logger import logging
from src.exception.exception import customexception
import tkinter as tk

# Initialize the voice recognizer
r = sr.Recognizer()

def play_speech(text):
    # Voice syntesizer initiation
    converter = VoiceSynthesizer()
    converter.synthesize_speech(text)

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load("artifacts/Audio.mp3")
    logging.info("Generated audio file loaded")

    # Play the loaded mp3 file
    pygame.mixer.music.play()
    pygame.mixer.music.get_endevent()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.load("artifacts/Audio_copy.mp3")
    os.remove("artifacts/Audio.mp3")
    logging.info("Created audio file removed for entry of new file.")

# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()

def listen():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # # recognize speech using Sphinx
    # try:
    #     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    # except sr.UnknownValueError:
    #     print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + text)

        return text
    
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def save_output(output_data, output_dir="artifacts"):
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save text response
    with open(f"{output_dir}/response.txt", "w") as f:
        f.write(output_data['response_text'])
    logging.info("Generated response stored in response.txt file in artifacts folder.")

def load_output(output_dir="artifacts"):   
    # Load text response
    with open(f"{output_dir}/response.txt", "r") as f:
        answer = f.read()
    logging.info("Stored text loaded.")

    return answer