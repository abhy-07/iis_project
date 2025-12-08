import requests
import time

BASE_URL = "http://127.0.0.1:54321/furhat"

def make_robot_speak(text):
    print(f"🎤 Telling robot to say: '{text}'...")
    try:
        # FIX: The error told us to use 'utterance' instead of 'text'
        response = requests.post(
            f"{BASE_URL}/say", 
            json={"utterance": text, "abort": True}, 
            timeout=2
        )
        
        if response.status_code == 200:
            print("✅ SUCCESS: Robot spoke!")
        else:
            print(f"❌ Speak failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"🚫 Network Error: {e}")

def make_robot_attend(x, y, z):
    # Instead of gestures (which are giving parsing errors), 
    # let's try moving the head. It's a great visual test.
    print(f"👀 Telling robot to look at ({x}, {y}, {z})...")
    try:
        response = requests.post(
            f"{BASE_URL}/attend", 
            json={"location": f"{x},{y},{z}"}, 
            timeout=2
        )
        if response.status_code == 200:
            print("✅ SUCCESS: Robot moved head!")
        else:
            print(f"❌ Head move failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"🚫 Network Error: {e}")

# --- EXECUTE ---
print("--- TEST 1: SPEECH ---")
make_robot_speak("System connected. I can hear you.")

time.sleep(3)

print("\n--- TEST 2: MOVEMENT ---")
make_robot_attend(1, 0, 1) # Look right