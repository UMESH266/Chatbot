# Text generation
from src.logger.logger import logging
from src.exception.exception import customexception
import sys
from langchain_huggingface import HuggingFaceEndpoint

# Text generation model
# repo_id="Laim/Llama-3.1-MedPalm2-imitate-8B-Instruct"
# repo_id="Joycean0301/Llama-3.2-3B-Instruct-Medical-Conversational"
# repo_id = "TheBloke/medalpaca-13B-GGML"
repo_id="mistralai/Mistral-7B-Instruct-v0.3"

class DocChatProcessor:
    def __init__(self, hf_token):
        self.llm = HuggingFaceEndpoint( 
                                    repo_id=repo_id,  
                                    max_new_tokens=512,
                                    top_k=10,  
                                    top_p=0.95,  
                                    typical_p=0.95,  
                                    temperature=0.01,  
                                    repetition_penalty=1.03,  
                                    streaming=False,  
                                    huggingfacehub_api_token= hf_token,
                                    stop_sequences=['?', '</s>', '.\n\n']  
                                ) 
        
    logging.info("LLM model for medical text generation created.")

    def generate_response(self, input_text):
        try:
            logging.info("Text response generated.")
            return self.llm.invoke(input_text)
        except Exception as e:
            raise customexception(e,sys)