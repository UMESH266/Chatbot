# Main driver code of chatbot
import streamlit as st
from streamlit_option_menu import option_menu
from src.components.avatarsys import AvatarSystem
from src.utils.accessory import play_speech, listen, save_output, load_output
import speech_recognition as sr

# Global 
salutation = "Pleasure meeting you. Have a nice day!"

# Page title
st.title("Welcome to Chatbot conversation")
st.markdown("<h3 style='text-align: center;'>Hello, I am your chatbot assistant.</h1>", unsafe_allow_html=True)

mode = option_menu("Choose mode of interaction", ["Text", "Voice", 'Exit'], 
    icons=['house', 'cloud-upload', "list-task"], 
    menu_icon="cast", default_index=0, orientation="horizontal")

st.write("Add your Huggingface Access Token to use the chatbot.")

if "HF_TOKEN" not in st.session_state:
    st.session_state.HF_TOKEN = ''
# Chatbot configuration initiation
st.session_state.HF_TOKEN = st.text_input("Your Access Token: ")
avatar = AvatarSystem(st.session_state.HF_TOKEN)

def response(input_text):
    # Getting response and sentiment of response 
    output = avatar.process_input(input_text)
    # Save output response in txt
    save_output(output)
    response_sentiment = output['emotion']
    ans = load_output()
    st.write(f"You: {input_text}")
    st.write(f"AI Avatar: {ans}\n")
    play_speech(ans)
    st.write(f"Response sentiment: {response_sentiment}")

if mode == "Text":
    # form requires unique key
    with st.form(key='Chat form', clear_on_submit=True):
        user_input = st.text_input("You: ", value="", placeholder="Ask anything or Type 'Exit' to end")
        col1, col2, col3 = st.columns(3)
        save = col3.form_submit_button("Submit")
    if save and user_input != "":
        user_input = user_input.lower() + '?'

        # Exiting the chat
        if 'exit' in user_input:
            st.write(salutation)
            play_speech(salutation)
            st.stop()
            
        # Getting response and sentiment of response 
        response(user_input)
        
elif mode == "Voice":
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
        
elif mode == "Exit":
    st.write(salutation)
    play_speech(salutation)
    st.stop()


def chatbot(mode):
    # while loop to have conversation with bot
    run = True
    while run:
        user_input = 'Hi!' # Initializing user input to be empty
        if mode == "Voice":
            # Voice to text conversion
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Speak: ") # print("Say something!")
                audio = r.listen(source)
                r.adjust_for_ambient_noise(source, duration=0.2)
                text = r.recognize_google(audio)
                user_input = text + '?'
                
                # Exiting the chat
                if 'exit' in user_input:
                    st.write(salutation) # print("Pleasure meeting you. Have a nice day!")
                    play_speech(salutation)
                    break

        elif mode == "Text":
            while user_input != True:    
                user_input = st.text_input("You: ") # input("You: ").lower()
                user_input = user_input.lower() + '?'

                # Exiting the chat
                if 'exit' in user_input:
                    st.write(salutation)
                    play_speech(salutation)
                    break

        elif mode == 'Exit':
            st.write(salutation)
            play_speech(salutation)
            break
        else:
            st.write("Invalid mode. Try again")
            st.write(salutation)
            play_speech(salutation)
            break    
        
        # Getting response and sentiment of response 
        output = avatar.process_input(user_input)

        # Save output response in txt
        save_output(output)
        response_sentiment = output['emotion']
        ans = load_output()
        st.write(f"You: {user_input}")
        st.write(f"AI Avatar: {ans}\n")
        play_speech(ans)
        st.write(f"Response sentiment: {response_sentiment}")

# Calling function
# chatbot(mode)