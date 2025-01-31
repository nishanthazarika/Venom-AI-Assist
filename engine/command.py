import pyttsx3
import speech_recognition as sr

import time
import os




import eel
os.environ["FLAC_CONVERTER"] = "/opt/homebrew/bin/flac"

def speak(text):
    text = str(text)
    engine = pyttsx3.init()  # Default to 'nsss' on macOS
    voices = engine.getProperty('voices')
    # Uncomment this to see available voices
    #englis(uk):119,USA:120,Reed UK:105,superstar:102,18->eddy(uk,1->alice)
    # for index, voice in enumerate(voices):
    #     print(f"Voice {index}: {voice.name}")
    engine.setProperty('voice', voices[119].id)  # Change index as needed
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
            print('Recognizing...')
            eel.DisplayMessage('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            eel.DisplayMessage(query)
            # speak(query)
            time.sleep(2)
            # eel.ShowHood()
        except Exception as e:
            print(f"Error: {e}")
            return ""
        return query.lower()

# text = takecommand()
# if text:
#     speak(text)
# else:
#     print("No input detected.")
@eel.expose
def allCommands(message=1):
    if message==1:
        query = takecommand()
        print(f"Query received: {query}")
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)
    from engine.features import PlayYoutube, findContact, whatsApp
    try:
        

        if "open" in query.lower():
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query.lower():
            print("Matched YouTube command")
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
        elif "send a message to" in query.lower():
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send a message to" in query or "send a sms to" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send a message to" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot
            response = chatBot(query)
            eel.DisplayMessage(response)  # Display the response on the screen
            speak(response)
    except Exception as e:
        print(f"Error: {e}")

    eel.ShowHood()


