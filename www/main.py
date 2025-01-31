import os
import eel
import sys

# Add the parent directory of 'www' (the 'Jarvis' directory) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.features import *
from engine.command import *
from engine.auth import recoganize



from engine.features import *

from engine.command import *
# Initialize the web directory
def start():
    eel.init("www")
    playAssistantSound()
    @eel.expose
    def init():
        subprocess.call(['/Users/nishanthazarika/Desktop/Jarvis/www/device.sh'])
        eel.hideLoader()
        speak("Ready for face authentication")
        flag=recoganize.AuthenticateFace()
        if flag==1:
            eel.hideFaceAuth()
            speak("Face Authentication succesful")
            eel.hideFaceAuthSuccess()
            speak("Welcome to the AI Assistant")
            eel.hideStart()
        else:
            speak("Face Authentication failed")
    # Open Microsoft Edge as an app pointing to your local server (macOS version)
    os.system('open -a "Microsoft Edge" http://localhost:8000/index.html')


    # Start the eel application
    eel.start('index.html', mode=None, host='localhost', block=True)

