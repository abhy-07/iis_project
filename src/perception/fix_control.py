import requests
import time

BASE_URL = "http://127.0.0.1:54321/furhat"

def make_robot_speak(text):
    print(f"🎤 Telling robot to say: '{text}'...")
    try:
        # STRATEGY CHANGE: Use 'params' to send data in the URL
        # URL becomes: .../say?text=Hello&abort=true
        response = requests.post(
            f"{BASE_URL}/say", 
            params={"text": text, "abort": "true"}, 
            timeout=2
        )
        
        if response.status_code == 200:
            print("✅ SUCCESS: Robot spoke!")
        else:
            print(f"❌ Speak failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"🚫 Network Error: {e}")

def make_robot_attend(x, y, z):
    print(f"👀 Telling robot to look at ({x}, {y}, {z})...")
    try:
        # STRATEGY CHANGE: Use 'params' for location
        # URL becomes: .../attend?location=1,0,1
        response = requests.post(
            f"{BASE_URL}/attend", 
            params={"location": f"{x},{y},{z}"}, 
            timeout=2
        )
        if response.status_code == 200:
            print("✅ SUCCESS: Robot moved head!")
        else:
            print(f"❌ Head move failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"🚫 Network Error: {e}")

# --- EXECUTE ---
print("--- TEST 1: SPEECH (URL PARAMS) ---")
make_robot_speak("I can finally hear you.")

time.sleep(3)

print("\n--- TEST 2: MOVEMENT (URL PARAMS) ---")
make_robot_attend(1, 0, 1)