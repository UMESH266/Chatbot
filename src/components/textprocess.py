# Text generation
from src.logger.logger import logging
from src.exception.exception import customexception
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import HuggingFaceEndpoint

# Text generation model
repo_id="mistralai/Mistral-7B-Instruct-v0.3"
# repo_id='openai-community/gpt2'

class TextProcessor:
    def __init__(self, hf_token):
        self.llm = HuggingFaceEndpoint( 
                                    repo_id=repo_id,  
                                    max_new_tokens=250,
                                    top_k=10,  
                                    top_p=0.95,  
                                    typical_p=0.95,  
                                    temperature=0.01,  
                                    repetition_penalty=1.03,  
                                    streaming=False,  
                                    huggingfacehub_api_token= hf_token,
                                    stop_sequences=['?', '</s>', '.\n\n']  
                                ) 
        
    logging.info("LLM model for text generation created.")

    def generate_response(self, input_text):
        logging.info("Text response generated.")
        return self.llm.invoke(input_text)