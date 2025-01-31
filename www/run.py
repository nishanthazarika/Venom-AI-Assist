import multiprocessing
import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def startJarvis():
    """Starts the Jarvis application."""
    print("Starting Jarvis...")
    from main import start
    start()

def listenHotword():
    """Listens for hotwords."""
    print("Listening for hotwords...")
    from engine.features import hotword
    hotword()

if __name__ == '__main__':
    # Create and start processes
    p1 = multiprocessing.Process(target=startJarvis, name="JarvisProcess")
    p2 = multiprocessing.Process(target=listenHotword, name="HotwordProcess")

    p1.start()
    # subprocess.call(['/Users/nishanthazarika/Desktop/Jarvis/www/device.sh'])
    p2.start()

    try:
        # Wait for both processes to complete
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        # Handle manual interruption (Ctrl+C)
        print("\nStopping processes...")
        p1.terminate()
        p2.terminate()
    finally:
        p1.join()
        p2.join()
        print("System stopped.")
