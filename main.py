import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3
import google.generativeai as genai

chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Jarvis: {query}\n Prime : "
    
    # Configure Gemini API
    genai.configure(api_key="key")
    
    # Set up the model
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }
    
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
      },
    ]
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                            generation_config=generation_config,
                            safety_settings=safety_settings)
    
    convo = model.start_chat(history=[])
    
    convo.send_message(query)
    print(convo.last.text)

    response = convo.last.text
    
    say(response)
    chatStr += f"{response}\n"
    
    return response




def ai(prompt):
    # openai.api_key = api_key
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    client = OpenAI() 
    response = client.chat.completions.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    
    # todo: Wrap this inside of a try-except block
    # print(response.choices[0].text)
    text += response.choices[0].text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Prime "

if __name__ == '__main__':
    print('Welcome to Prime  A.I')
    say("Prime  A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            musicPath = "/Users/Jarvis/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "the time" in query:
            musicPath = "/Users/Jarvis/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif " chatgpt ".lower() in query.lower():
            ai(prompt=query)

        elif "Prime  Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)

def say(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech

    # Say the provided text
    engine.say(text)

    # Block while processing all currently queued commands
    engine.runAndWait()
