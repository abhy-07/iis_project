import cv2
import numpy as np
import time
import requests
from tensorflow.keras.models import load_model

# --- CONFIGURATION ---
ROBOT_URL = "http://127.0.0.1:54321/furhat"
MODEL_PATH = 'my_emotion_model_v3.keras'

# 1. TIMING CONTROL (The fix for "Chatty Robot")
# The robot will wait at least this many seconds before speaking again.
INTERACTION_INTERVAL = 8.0  

# 2. LABELS (Confirmed from your check_labels.py)
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

print(f"Loading {MODEL_PATH}...")
model = load_model(MODEL_PATH)
print("✅ Model loaded!")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- HELPERS ---
def robot_say(text):
    try:
        requests.post(f"{ROBOT_URL}/say", params={"text": text, "abort": "true"}, timeout=0.1)
    except: pass

def robot_attend(x, y, z):
    try:
        requests.post(f"{ROBOT_URL}/attend", params={"location": f"{x},{y},{z}"}, timeout=0.1)
    except: pass

# --- STATE VARIABLES ---
cap = cv2.VideoCapture(0)
last_speak_time = 0
last_detected_emotion = "neutral"  # Remember what we saw last time

print("--- STARTING SMOOTH INTERACTION DEMO ---")
print(f"Robot will only react every {INTERACTION_INTERVAL} seconds.")

while True:
    ret, frame = cap.read()
    if not ret: break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Preprocessing
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi_gray, (48, 48))
        
        # Debug View
        cv2.imshow('Brain Input', cv2.resize(roi_resized, (200, 200)))

        # Predict
        img_pixels = roi_resized.astype('float32') / 255.0
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels = np.expand_dims(img_pixels, axis=-1)

        predictions = model.predict(img_pixels, verbose=0)[0]
        max_index = np.argmax(predictions)
        current_emotion = EMOTION_LABELS[max_index]
        confidence = predictions[max_index]

        # Display Text
        label_text = f"{current_emotion} ({int(confidence*100)}%)"
        color = (0, 0, 255) if current_emotion in ['sad', 'angry', 'fear'] else (0, 255, 0)
        cv2.putText(frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # --- SMART ROBOT LOGIC ---
        current_time = time.time()
        time_passed = current_time - last_speak_time

        # Logic Rule 1: Must be confident (>50%)
        # Logic Rule 2: Must wait for the time interval
        if confidence > 0.50 and time_passed > INTERACTION_INTERVAL:
            
            # Logic Rule 3: ONLY speak if the emotion CHANGED, OR if it's been a really long time (e.g. 20s)
            # This prevents "You are happy. You are happy. You are happy."
            if current_emotion != last_detected_emotion or time_passed > 20.0:
                
                print(f"Reacting to: {current_emotion}")
                
                if current_emotion == 'happy':
                    robot_say("I see you are smiling! Let's keep that energy.")
                    robot_attend(1.0, 0.0, 1.0)
                elif current_emotion == 'sad':
                    robot_say("You look a bit down. Should I tell a story to cheer you up?")
                    robot_attend(1.0, 0.0, 1.0)
                elif current_emotion == 'angry':
                    robot_say("I sense some tension. I will speak calmly.")
                elif current_emotion == 'surprise':
                    robot_say("You look surprised!")
                
                # Update State
                last_detected_emotion = current_emotion
                last_speak_time = current_time

    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()