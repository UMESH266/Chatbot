import os
import sys
from pathlib import Path
import speech_recognition as sr
import pyttsx3 
import pygame
from src.components.voicesynth import VoiceSynthesizer
from src.logger.logger import logging
from src.exception.exception import customexception

# Initialize the voice recognizer
r = sr.Recognizer()

def play_speech(text):
    try:
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

    except Exception as e:
        raise customexception(e,sys)

# Function to convert text to
# speech
def SpeakText(command):
    try:
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command) 
        engine.runAndWait()
    except Exception as e:
        raise customexception(e,sys)
    
def listen():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + text)

        return text
    
    except sr.UnknownValueError:
        raise ("Google Speech Recognition could not understand audio", sys)
    except sr.RequestError as e:
        raise customexception("Could not request results from Google Speech Recognition service; {0}".format(e), sys)
    except Exception as e:
        raise customexception(e, sys)

def save_output(output_data, output_dir="artifacts"):
    try:
        Path(output_dir).mkdir(exist_ok=True)
        
        # Save text response
        with open(f"{output_dir}/response.txt", "w") as f:
            f.write(output_data['response_text'])
        logging.info("Generated response stored in response.txt file in artifacts folder.")
    except Exception as e:
        raise customexception(e,sys)

def load_output(output_dir="artifacts"): 
    try:  
        # Load text response
        with open(f"{output_dir}/response.txt", "r") as f:
            answer = f.read()
        logging.info("Stored text loaded.")

        return answer
    except Exception as e:
        raise customexception(e,sys)