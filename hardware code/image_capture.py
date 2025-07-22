# https://core-electronics.com.au/guides/face-identify-raspberry-pi/

import cv2 as cv
import os
from datetime import datetime
import time

# Change this to the name of the person you're photographing
PERSON_NAME = "Isaac"  

def create_folder(name):
    dataset_folder = "dataset"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    person_folder = os.path.join(dataset_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def capture_photos(name):
    folder = create_folder(name)

    # Allow camera to warm up
    time.sleep(2)

    photo_count = 0
    
    print(f"Taking photos for {name}. Press SPACE to capture, 'q' to quit.")
    cap = cv.VideoCapture(0 )
    
    while True:
        

        ret, frame = cap.read()
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) 
        # Display the frame
        cv.imshow('Capture', frame)
        
        key = cv.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space key
            photo_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)
            cv.imwrite(filepath, frame)
            print(f"Photo {photo_count} saved: {filepath}")
        
        elif key == ord('q'):  # Q key
            break
    
    # Clean up
    cv.destroyAllWindows()

    cap.release()
    print(f"Photo capture completed. {photo_count} photos saved for {name}.")

if __name__ == "__main__":
    capture_photos(PERSON_NAME)
