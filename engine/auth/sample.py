import cv2
import os

# Create a video capture object to access the webcam
cam = cv2.VideoCapture(0)  # Remove cv2.CAP_DSHOW for macOS compatibility
cam.set(3, 640)  # Set video FrameWidth
cam.set(4, 480)  # Set video FrameHeight

# Load the Haar Cascade classifier
detector = cv2.CascadeClassifier('engine/auth/haarcascade_frontalface_default.xml')

# Check if the Haar Cascade XML file exists
if not os.path.exists('engine/auth/haarcascade_frontalface_default.xml'):
    print("Error: Haar Cascade XML file not found!")
    exit()

# Input face ID
face_id = input("Enter a Numeric user ID here: ")

print("Taking samples, look at the camera .......")
count = 0  # Initializing sampling face count

while True:
    # Read the frames using the created object
    ret, img = cam.read()
    if not ret:
        print("Error: Unable to capture video. Is the camera connected and accessible?")
        break

    # Convert the image to grayscale
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = detector.detectMultiScale(converted_image, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        # Save the captured image into the datasets folder
        if not os.path.exists("engine/auth/samples"):
            os.makedirs("engine/auth/samples")  # Create the directory if it doesn't exist
        cv2.imwrite(f"engine/auth/samples/face.{face_id}.{count}.jpg", converted_image[y:y + h, x:x + w])

        # Display the image in a window
        cv2.imshow('image', img)

    # Wait for a pressed key
    k = cv2.waitKey(100) & 0xff
    if k == 27:  # Press 'ESC' to stop
        break
    elif count >= 100:  # Take 100 samples for better accuracy
        break

print("Samples taken. Now closing the program....")
cam.release()
cv2.destroyAllWindows()
1