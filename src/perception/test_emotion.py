import cv2
from deepface import DeepFace
from bridge import FurhatBridge  # <--- IMPORT THE BRIDGE
import time                      # <--- IMPORT TIME

print("Initializing Camera...")
cap = cv2.VideoCapture(0)
bridge = FurhatBridge()          # <--- CONNECT TO ROBOT

# We don't want to spam the robot 30 times a second.
# Let's send an update every 2 seconds.
last_sent_time = 0
SEND_INTERVAL = 2.0 

while True:
    ret, frame = cap.read()
    if not ret: break

    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dom_emotion = analysis[0]['dominant_emotion']
        confidence = analysis[0]['face_confidence']

        # --- NEW CODE START ---
        # Check if 2 seconds have passed
        current_time = time.time()
        if current_time - last_sent_time > SEND_INTERVAL:
            print(f"Sending to Robot: {dom_emotion}")
            bridge.send_emotion(dom_emotion, confidence)
            last_sent_time = current_time
        # --- NEW CODE END ---

        text = f"{dom_emotion} ({int(confidence*100)}%)"
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        pass

    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()