import cv2
import time
import requests
from deepface import DeepFace

# --- CONFIGURATION ---
ROBOT_IP = "127.0.0.1"
ROBOT_PORT = 54321
BASE_URL = f"http://{ROBOT_IP}:{ROBOT_PORT}/furhat"

def robot_say(text):
    """Makes the robot speak using URL parameters (since JSON failed)."""
    try:
        requests.post(f"{BASE_URL}/say", params={"text": text, "abort": "true"})
    except:
        pass

def robot_gesture(name):
    """Triggers a gesture (using the 'gesture' endpoint if available, or just printing for now)."""
    # Note: If /gesture gave 400 earlier, we might need to debug it later. 
    # For now, we focus on speech which we know works.
    print(f"Robot Gesture: {name}")

# --- MAIN LOOP ---
print("--- STARTING INTERACTIVE DEMO ---")
print("Look at the camera. The robot will comment on your face.")

cap = cv2.VideoCapture(0)
last_emotion = "neutral"
last_speak_time = 0
COOLDOWN = 5.0  # Only speak once every 5 seconds to avoid spam

while True:
    ret, frame = cap.read()
    if not ret: break

    try:
        # 1. Detect Emotion
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        current_emotion = analysis[0]['dominant_emotion']
        
        # Draw on screen
        cv2.putText(frame, f"Detected: {current_emotion}", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 2. Logic: Did the emotion change?
        # We also check the cooldown so the robot doesn't talk over itself.
        if current_emotion != last_emotion and (time.time() - last_speak_time > COOLDOWN):
            
            print(f"New Emotion Detected: {current_emotion}")
            
            # 3. Robot Reaction
            if current_emotion == "happy":
                robot_say("You look so happy today!")
            elif current_emotion == "sad":
                robot_say("Oh no, why are you sad?")
            elif current_emotion == "angry":
                robot_say("Who made you angry?")
            elif current_emotion == "surprise":
                robot_say("Wow, did I surprise you?")
            
            last_emotion = current_emotion
            last_speak_time = time.time()

    except Exception as e:
        pass # Ignore empty frames

    cv2.imshow('Interaction Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()