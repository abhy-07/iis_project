import requests
import json

class FurhatBridge:
    def __init__(self, ip="127.0.0.1", port="54321"):
        # Note: Furhat Remote API uses port 54321, not 8080
        self.base_url = f"http://{ip}:{port}/furhat"

    def send_emotion(self, emotion, confidence):
        """
        Sends the detected emotion to the robot as a generic event.
        """
        url = f"{self.base_url}/event"
        
        # We create a custom event called 'UserEmotion'
        # The Kotlin code on the robot will listen for this specific name
        payload = {
            "event_name": "UserEmotion",
            "data": {
                "emotion": emotion,
                "confidence": float(confidence)
            }
        }

        try:
            # We add timeout=1 so it doesn't hang forever
            response = requests.post(url, json=payload, timeout=1)
            
            # --- DEBUGGING LINES ---
            if response.status_code == 200:
                print(f"[Success] Robot received event! (Status: 200)")
            else:
                print(f"[Error] Robot rejected it. Status: {response.status_code}")
                print(f"Reason: {response.text}")
            # -----------------------
            
            return True
        except Exception as e:
            print(f"[Network Error] Could not connect to Furhat: {e}")
            return False