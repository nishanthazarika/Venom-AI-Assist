import os
from shlex import quote
import sys
import time
import struct
import sqlite3
import subprocess
import webbrowser
from hugchat import hugchat
import openai
import pywhatkit as kit
import pyautogui as autogui
import pyaudio
import pvporcupine
from playsound import playsound
import eel
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words
# from dotenv import load_dotenv
# # # Load environment variables
# load_dotenv()


con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Play assistant sound
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)

import os
import subprocess
import webbrowser
def openCommand(query):
    # Process the query by removing assistant name and "open" keyword
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().title().lower()  # Using title() for better handling of app names
    print(f"Processed query: {query}")
    
    try:
        # Check database for the app path
        cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (query,))
        results = cursor.fetchall()
        print(f"Database results: {results}")
        
        # If found in the database
        if results:
            speak("Opening " + query)
            print(f"Opening path from database: {results[0][0]}")
            subprocess.call(["open", results[0][0]])
        else:
            # Check if it's a valid app in /Applications folder (macOS specific)
            #app_path = f"/Sytem/Applications/{query}.app"  # Check in the common /Applications directory first
            app_path = f"/System/Applications/{query}.app"
            app_path1 = f"/Applications/{query}.app"
            print(f"Checking for app in /Applications: {app_path}")
            if os.path.exists(app_path):
                speak(f"Opening {query}")
                print(f"Opening app directly from /Applications: {app_path}")
                subprocess.call(["open", app_path])
            elif os.path.exists(app_path1):
                speak(f"Opening {query}")
                print(f"Opening app directly from /Applications: {app_path1}")
                subprocess.call(["open", app_path1])
            else:
                # Check for web commands
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (query,))
                results = cursor.fetchall()
                print(f"Web command results: {results}")
                
                if results:
                    speak("Opening " + query)
                    print(f"Opening URL: {results[0][0]}")
                    webbrowser.open(results[0][0])
                else:
                    # Fallback to opening query directly if nothing else is found
                    speak(f"Opening {query}, attempting fallback.")
                    print(f"Trying to open directly: {query}")
                    try:
                        subprocess.call(["open", query])  # No fallback to Desktop/Jarvis folder
                    except Exception as e:
                        speak("Not found")
                        print(f"Error: {e}")
    except Exception as e:
        speak("Something went wrong")
        print(f"Error: {e}")


# Play YouTube videos
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        try:
            kit.playonyt(search_term)
        except Exception as e:
            speak(f"Sorry, I encountered an error: {e}")
            print(f"Error: {e}")
    else:
        speak("I couldn't understand what you want to play on YouTube.")

# Hotword detection
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        access_key = "zfpzW7GRPsaNXxukXDAgk2U7m8L3XoS844kp+qqzSXcjiiDacYISkQ=="
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"], access_key=access_key)
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length * 2
        )
        
        # Loop for hotword detection
        while True:
            try:
                keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            except IOError:
                print("Audio input overflowed. Skipping this frame.")
                continue

            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("Hotword detected")
                # trigger_action()  # Trigger the action when hotword is detected
    except KeyboardInterrupt:
        print("\nExiting on user request...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    # Remove unnecessary words from the query
    words_to_remove = [
        ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call',
        'send', 'message', 'whatsapp', 'video'
    ]
    query = remove_words(query, words_to_remove)
    query = query.strip().lower()  # Normalize to lowercase for comparison

    # Debugging log for query transformation
    print(f"Processed query for findContact: '{query}'")

    try:
        # Search for an exact case-insensitive match in the database
        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) = ?",
            (query,)
        )
        exact_results = cursor.fetchall()

        # Debugging log for exact match results
        print(f"Exact match results: {exact_results}")

        # If an exact match is found, return it
        if exact_results:
            mobile_number_str = str(exact_results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query

        # If no exact match, log and return failure
        print("No exact match found in the database.")
        return 0, 0

    except Exception as e:
        print(f"Error in findContact: {e}")
        speak("I couldn't find the contact. Please try again.")
        return 0, 0



#### 9. Create Whatsapp Function in features.py

import pyautogui as autogui
import time
import subprocess
import platform

import time
import pyautogui
import webbrowser
import subprocess

def whatsApp(contact_no, message, flag, name):
    try:
        # Open WhatsApp Web in the browser
        webbrowser.open('https://web.whatsapp.com/')
        print("Opening WhatsApp Web...")
        time.sleep(10)  # Wait for WhatsApp Web to load completely

        # Move to the search bar (index 10)
        for _ in range(1, 11):
            pyautogui.hotkey('tab')
        time.sleep(1)

        # Type the contact name and press Enter to search
        pyautogui.typewrite(name)
        pyautogui.press('enter')
        time.sleep(2)  # Wait for the contact to load

        # Type the message
        pyautogui.typewrite(message)
        time.sleep(1)

        # Send the message by pressing Enter
        pyautogui.press('enter')
        print(f"Message sent successfully to {name}")
    
    except Exception as e:
        print(f"Error: {e}")


# def chatBot(query):
#     # Set the Gemini API endpoint URL
#     api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
#     # Print environment variables for debugging
#     print("All Environment Variables:")
#     for key, value in os.environ.items():
#         print(f"{key}: {value}")
    
#     # Retrieve the Gemini API key from the environment variable
#     api_key = os.getenv("GEMINI_API_KEY")

#     # Detailed logging
#     print(f"API Key retrieved: {api_key}")
#     if not api_key:
#         print("Error: GEMINI_API_KEY not set in environment variables.")
#         return "Sorry, API key is missing."

#     # Prepare the request payload and headers
#     payload = {
#         "contents": [{"parts": [{"text": query}]}]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     params = {"key": api_key}

#     try:
#         # Make the POST request to the Gemini API endpoint
#         response = requests.post(
#             api_url, 
#             json=payload, 
#             headers=headers, 
#             params=params
#         )
        
#         # Detailed logging
#         print(f"API Response Status: {response.status_code}")
#         print(f"API Response Content: {response.text}")

#         # Check if the request was successful
#         if response.status_code == 200:
#             response_data = response.json()
#             generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
#             speak(generated_text)
#             return generated_text
#         else:
#             # Prepare and speak error message
#             error_message = f"Sorry, API request failed. Status: {response.status_code}"
#             speak(error_message)
#             print(f"API Error: {response.text}")
#             return error_message
    
#     except Exception as e:
#         # Prepare and speak exception message
#         error_message = f"An unexpected error occurred: {e}"
#         speak(error_message)
#         print(f"Exception in API call: {e}")
#         return error_message

def clean_text(text):
    """
    Clean the text by removing extra newline characters and excessive whitespace.
    
    Args:
        text (str): The input text to be cleaned.
    
    Returns:
        str: Cleaned text with newlines replaced and extra whitespace removed.
    """
    # Replace multiple newlines with a single space
    cleaned_text = text.replace('\n', ' ')
    
    # Remove leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # Reduce multiple spaces to a single space
    import re
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text

def chatBot(query):
    # Set the Gemini API endpoint URL
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    # Retrieve the Gemini API key from the environment variable
    api_key = os.getenv("GEMINI_API_KEY")

    # Check if the API key is set
    if not api_key:
        error_message = "Sorry, I couldn't process your request due to an API configuration issue."
        cleaned_error = clean_text(error_message)
        
        # Speak the error
        speak(cleaned_error)
        
        # Print in terminal
        print(cleaned_error)
        
        # Display in UI
        eel.DisplayMessage(cleaned_error)
        
        return cleaned_error

    # Prepare the request payload and headers
    payload = {
        "contents": [{"parts": [{"text": query}]}]
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {"key": api_key}

    try:
        # Make the POST request to the Gemini API endpoint
        response = requests.post(
            api_url, 
            json=payload, 
            headers=headers, 
            params=params
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
            
            # Clean the generated text
            cleaned_text = clean_text(generated_text)
            
            # Speak the response
            speak(cleaned_text)
            
            # Print in terminal
            print("Gemini Response:")
            print(cleaned_text)
            
            # Display in UI
            eel.DisplayMessage(cleaned_text)
            
            return cleaned_text
        else:
            # Prepare and handle error message
            error_message = f"Sorry, API request failed. Status: {response.status_code}"
            cleaned_error = clean_text(error_message)
            
            # Speak the error
            speak(cleaned_error)
            
            # Print error in terminal
            print("API Error:")
            print(f"Status Code: {response.status_code}")
            print(f"Error Details: {response.text}")
            
            # Display error in UI
            eel.DisplayMessage(cleaned_error)
            
            return cleaned_error
    
    except Exception as e:
        # Prepare and handle exception message
        error_message = f"An unexpected error occurred: {e}"
        cleaned_error = clean_text(error_message)
        
        # Speak the error
        speak(cleaned_error)
        
        # Print exception details in terminal
        print("Exception in API Call:")
        print(error_message)
        print(f"Full Exception Details: {e}")
        
        # Display error in UI
        eel.DisplayMessage(cleaned_error)
        
        return cleaned_error
    
# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)

def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    import time

    # Replace spaces in the message and mobile number for ADB input
    message = replace_spaces_with_percent_s(message)  # Ensures spaces are replaced with %20 or appropriate format
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    
    speak("Sending message to " + name)
    
    # Go back to the home screen
    goback(4)  # Navigate back multiple times to ensure starting from the home screen
    time.sleep(1)
    keyEvent(3)  # KeyEvent 3 simulates the home button press
    
    # Open the SMS app (Adjust coordinates based on your screen resolution)
    tapEvents(136, 2220)  # Tap on the SMS app icon
    time.sleep(2)  # Wait for the app to open
    
    # Start a new chat
    tapEvents(819, 2192)  # Tap on the "Start Chat" button
    time.sleep(1)
    
    # Input the mobile number in the "To" field
    adbInput(mobileNo)  # Type the mobile number
    time.sleep(1)
    
    # Tap on the contact result (Adjust the coordinates to the first search result on your screen)
    tapEvents(355, 664)  # Select the first contact result
    time.sleep(1)
    
    # Focus on the message input field (Adjust coordinates based on the input field location)
    tapEvents(347, 2193)
    time.sleep(3)
    
    # Type the message in the input field
    adbInput(message)
    time.sleep(1)
    
    # Send the message (Adjust coordinates for the send button)
    tapEvents(957, 1397)  # Tap the send button
    time.sleep(1)
    
    speak("Message sent successfully to " + name)
