from src.exception.exception import customexception
from src.logger.logger import logging
from src.components.textprocess import TextProcessor
from src.components.docchat import DocChatProcessor
from src.components.emotionanalyz import EmotionAnalyzer
from src.components.voicesynth import VoiceSynthesizer
import sys

class AvatarConfig:
    def __init__(self):
        self.image_size = 512
        self.voice_sample_rate = 22050
        self.max_text_length = 512

class AvatarSystem:
    def __init__(self, hf_token):
        self.config = AvatarConfig()
        self.text_processor = TextProcessor(hf_token)
        self.emotion_analyzer = EmotionAnalyzer()
        self.voice_synthesiser = VoiceSynthesizer()
        # self.doc_chat_processor = DocChatProcessor(hf_token)
    
    logging.info("Avatar system initiated.")

    def process_input(self, user_input):
        try:
            # Generate response
            response = self.text_processor.generate_response(user_input)
            logging.info("Text response generated.")

            # Analyze emotion
            emotion = self.emotion_analyzer.analyze_emotion(response)
            logging.info("Response sentiment received.")
                    
            # Synthesize voice and saves as mp3 file
            self.voice_synthesiser.synthesize_speech(response)
            logging.info("Generated response saved as audio mp3 format.")
            
            return {
                'response_text': response,
                'emotion': emotion
            }
        
        except Exception as e:
            raise customexception(e,sys)