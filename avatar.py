# Main driver code of chatbot
from src.components.avatarsys import AvatarSystem
from src.utils.accessory import play_speech, listen, save_output, load_output
import speech_recognition as sr

# Chatbot configuration initiation
HF_TOKEN = "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"
avatar = AvatarSystem(HF_TOKEN)

# Chatting bot greetings
welcome_text = "Hello, I am your chatbot assistant. How may I help you? \n Type 'Voice' or 'Text' to choose mode of interaction with me and say or type 'Exit' to end conversation."
print(welcome_text)
play_speech(welcome_text)

# Mode of interaction selection 
mode = input("Select mode of interaction (Voice/ Text/ Exit): ").lower()

# while loop to have conversation with bot
run = True
while run:
    user_input = '' # Initializing user input to be empty
    if mode == "voice":
        # Voice to text conversion
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            r.adjust_for_ambient_noise(source, duration=0.2)
            text = r.recognize_google(audio)
            user_input = text + '?'
            
            # Exiting the chat
            if 'exit' in user_input:
                print("Pleasure meeting you. Have a nice day!")
                play_speech("Pleasure meeting you. Have a nice day!")
                break

    elif mode == "text":
        while user_input != True:    
            user_input = input("You: ").lower()
            user_input = user_input + '?'

            # Exiting the chat
            if 'exit' in user_input:
                print("Thank you, Bye!")
                play_speech("Thank you, Bye!")
                break

    elif mode == 'exit':
        print("Thank you, Bye!")
        play_speech("Thank you, Bye!")
        break
    else:
        print("Invalid mode. Try again")
        print("Thank you, Bye!")
        play_speech("Thank you, Bye!")
        break    
    # Getting response and sentiment of response 
    output = avatar.process_input(user_input)

    # Save output response in txt
    save_output(output)
    response_sentiment = output['emotion']
    ans = load_output()
    print(f"You: {user_input}")
    print(f"AI Avatar: {ans}\n")
    play_speech(ans)
    print(f"Response sentiment: {response_sentiment}")