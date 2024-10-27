# Emotion analysis
from src.exception.exception import customexception
from src.logger.logger import logging
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# Pretrained model
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(MODEL)

class EmotionAnalyzer:
    def __init__(self):
        self.emotion_classifier = sentiment_model
        self.emotion = ''
    
    #  Roberta model
    def analyze_emotion(self, text):
        encoded_text = tokenizer(text, return_tensors='pt')
        output = self.emotion_classifier(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2],
        }
        self.emotion = max(scores_dict)
        logging.info("Sentiment of response generated.")

        return self.emotion