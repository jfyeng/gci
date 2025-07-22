# https://core-electronics.com.au/guides/face-identify-raspberry-pi/

import face_recognition
import cv2
import numpy as np
import time
import pickle

import time

#import distance
import ttsArshvir
#import vibrator

# Load pre-trained face encodings
print("[INFO] loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize our variables
cv_scaler = 4 # this has to be a whole number

face_locations = []
face_encodings = []
face_names = []
frame_count = 0
start_time = time.time()
fps = 0

utrasonic_distance=0

cooldown_max = 50
current_cooldown = 0

def process_frame(frame, distance):
    
    global cooldown_max, current_cooldown
    
    if current_cooldown != 0:
        current_cooldown+=1
    global face_locations, face_encodings, face_names
    
    # Resize the frame using cv_scaler to increase performance (less pixels processed, less time spent)
    resized_frame = cv2.resize(frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))
    
    # Convert the image from BGR to RGB colour space, the facial recognition library uses RGB, OpenCV uses BGR
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
    
    face_names = []
    if current_cooldown==cooldown_max:
        current_cooldown=0
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
            
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
                
        face_names.append(name)
  
        if current_cooldown==0:
            current_cooldown+=1
            ttsArshvir.speech(name, "bro", distance)
        
    
    return frame

def draw_results(frame):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler
        
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    
    return frame

def calculate_fps():
    global frame_count, start_time, fps
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    return fps

while True:
    # Capture a frame from camera
    ret, frame = cap.read()
    
    #vibrator.vibrate(ultrasonic_distance)
    

    processed_frame = process_frame(frame, "one point five")
    display_frame = draw_results(processed_frame)
    
    current_fps = calculate_fps()
    cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Video', display_frame)
    if cv2.waitKey(1) == ord("q"):
        break

# By breaking the loop we run this code here which closes everything
cv2.destroyAllWindows()
