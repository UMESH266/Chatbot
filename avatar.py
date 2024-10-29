# Main driver code of chatbot
import streamlit as st
from streamlit_option_menu import option_menu
from src.components.avatarsys import AvatarSystem
from src.utils.accessory import play_speech, listen, save_output, load_output
import speech_recognition as sr

# Global 
salutation = "Pleasure meeting you. Have a nice day!"

# Page title
st.title("Hi, Chatmate here!")
st.markdown("<h3 style='text-align: center;'>Hello, I am your chatbot assistant.</h1>", unsafe_allow_html=True)

mode = option_menu("Choose mode of interaction", ["RoboDoc", "Text", "Voice"], 
    icons=['chat-text', 'mic'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if "HF_TOKEN" not in st.session_state:
    st.session_state.HF_TOKEN = ''
st.write("Add your Huggingface Access Token to use the chatbot.")
st.session_state.HF_TOKEN = st.text_input("Your Access Token: ")

# Chatbot configuration initiation
if st.session_state.HF_TOKEN != '':
    avatar = AvatarSystem(st.session_state.HF_TOKEN)

def chat_history(input, response, sentiment):
    if 'history' not in st.session_state:
        st.session_state.history = dict()
    st.session_state.history[input] = [response, sentiment]
    return st.session_state.history

def response(input_text):
    # Getting response and sentiment of response 
    output = avatar.process_input(input_text)
    # Save output response in txt
    save_output(output)
    response_sentiment = output['emotion']
    ans = load_output()
    # st.write(f"You: {input_text}")
    # st.write(f"AI Avatar: {ans}\n")
    # st.write(f"Response sentiment: {response_sentiment}")
    
    return ans, response_sentiment

if mode == "Text" and st.session_state.HF_TOKEN != '':    
    if 'chathist' not in st.session_state:
        st.session_state.chathist = dict()
    
    # Form requires unique key
    with st.form(key=f'Chat form', clear_on_submit=True):
        user_input = st.text_input("You: ", value="", placeholder="Ask anything or Type 'Exit'")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        save = col6.form_submit_button("Click here")
        
    if save and user_input != "":
        user_input = user_input.lower() + '?'

        # Exiting the chat
        if 'exit' in user_input:
            st.write(salutation)
            play_speech(salutation)
           
        # Getting response and sentiment of response 
        ans, senti = response(user_input)
        # st.button("Audio", on_click=play_speech(ans))
        
        # Chat history 
        st.session_state.chathist = chat_history(user_input, ans, senti)
    
    # Chat history display
    st.markdown("### Chat History: ")
    with st.container(border=True):
        for key in st.session_state.chathist.keys():
            user_col1, user_col2, user_col3 = st.columns(3, vertical_alignment="center")
            user = user_col3.container(border=True)
            user.write(key)
            bot_col1, bot_col2, bot_col3 = st.columns([4, 1, 1], vertical_alignment='center')
            bot = bot_col1.container(border=True)
            bot.write(st.session_state.chathist[key][0])
                            
elif mode == "Voice" and st.session_state.HF_TOKEN != '':
    # Voice to text conversion
    r = sr.Recognizer()
    while 1:
        with sr.Microphone() as source:
            st.write("Speak: ") # print("Say something!")
            st.write("Please wait, response under process...")
            audio = r.listen(source)
            r.adjust_for_ambient_noise(source, duration=0.2)
            text = r.recognize_google(audio)
            user_input = text + '?'
            if text == '':
                user_input='exit?'
                st.write("Start again please. Failed to recognise the voice.")
                
            # Exiting the chat
            if 'exit' in user_input:
                st.write(salutation) # print("Pleasure meeting you. Have a nice day!")
                play_speech(salutation)
                st.stop()
                break
        
            #Getting response and sentiment of response 
            response(user_input)# output = avatar.process_input(user_input)