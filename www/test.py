# import struct
# import time
# import pyaudio
# import pvporcupine
# import pyautogui as autogui
# import time

# def hotword():
#     porcupine = None
#     paud = None
#     audio_stream = None
#     try:
#         access_key = "zfpzW7GRPsaNXxukXDAgk2U7m8L3XoS844kp+qqzSXcjiiDacYISkQ=="  # Replace with your actual access key
#         porcupine = pvporcupine.create(keywords=["jarvis", "alexa"], access_key=access_key)
#         paud = pyaudio.PyAudio()
#         audio_stream = paud.open(
#             # rate=porcupine.sample_rate
#             channels=1,
#             format=pyaudio.paInt16,
#             input=True,
#             frames_per_buffer=porcupine.frame_length * 2  # Increased buffer size
#         )
        
#         # Loop for streaming
#         while True:
#             try:
#                 keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
#                 keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
#             except IOError:
#                 print("Audio input overflowed. Skipping this frame.")
#                 continue

#             # Process keyword from mic input
#             keyword_index = porcupine.process(keyword)

#             # Check if hotword is detected
#             if keyword_index >= 0:
#                 print("Hotword detected")
#                 autogui.hotkey("win", "j")  # Simulates pressing Win + J
#                 time.sleep(2)  # Delay to prevent multiple triggers

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()
# hotword()


# import pyautogui as autogui

# # Attempt to locate the search result image on the screen
# result = autogui.locateCenterOnScreen('/full/path/to/search_result_marker.png', confidence=0.8)


# # Print the result
# if result:
#     print(f"Image found at {result}")
# else:
#     print("Image not found.")

#api integrate gemini

# (envjarvis) (base) nishanthazarika@MacBookAir Jarvis % echo $GEMINI_API_KEY


# (envjarvis) (base) nishanthazarika@MacBookAir Jarvis % sudo nano ~/.zshrc

# Password:
# (envjarvis) (base) nishanthazarika@MacBookAir Jarvis % source ~/.zshrc

# (base) (envjarvis) nishanthazarika@MacBookAir Jarvis % echo $GEMINI_API_KEY

# AIzaSyD4FQ-wjY0ZvnPWBaltln195cuHno0zGpA
# (base) (envjarvis) nishanthazarika@MacBookAir Jarvis % 



# import cv2

# cam = cv2.VideoCapture(0)
# if not cam.isOpened():
#     print("Error: Unable to access the camera.")
# else:
#     print("Camera is accessible. Close the permission prompt and re-run the script.")
# cam.release()
# import cv2

# try:
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     print("LBPH Face Recognizer created successfully!")
# except AttributeError as e:
#     print(f"Error: {e}")
# import cv2
# print(cv2.__version__)
# print(dir(cv2.face))  # This should list available methods like LBPHFaceRecognizer_create


# import cv2
# print(cv2.__file__)  # This should print the path to the cv2 module
# import cv2

# try:
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     print("LBPH Face Recognizer created successfully!")
# except AttributeError as e:
#     print(f"Error: {e}")
# import cv2

# #cam = cv2.VideoCapture(0)  # Try using 0 or 1, depending on your setup
# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# if not cam.isOpened():
#     print("Error: Could not access the camera.")
# else:
#     print("Camera is working correctly.")

#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             print("Failed to grab frame")
#             break

#         cv2.imshow("Camera", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cam.release()
#     cv2.destroyAllWindows()
import cv2
import numpy as np
import glob

# Define checkerboard dimensions
CHECKERBOARD = (9, 6)  # Number of inner corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points (3D coordinates in real world)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Load images from folder
images = glob.glob('calibration_images/*.jpg')  # Update path accordingly

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    
    if ret:
        objpoints.append(objp)
        refined_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(refined_corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, CHECKERBOARD, refined_corners, ret)
        cv2.imshow('Checkerboard', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()