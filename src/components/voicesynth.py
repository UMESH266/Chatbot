# Text to audio convertion
from src.logger.logger import logging
from src.exception.exception import customexception
from gtts import gTTS

class VoiceSynthesizer:
    def __init__(self):
      pass  
              
    def synthesize_speech(self, text):       
        # Text to English 
        language = 'en'

        # Conversion engine
        converter = gTTS(text=text, lang=language, slow=False)

        # Saving the converted audio in a mp3 file named
        converter.save("artifacts/Audio.mp3")
        logging.info("Response text convertion to audio done.")