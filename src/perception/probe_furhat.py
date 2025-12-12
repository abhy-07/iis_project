import requests

# The port you enabled in Settings
PORT = 54321
BASE_IP = "127.0.0.1"

# List of common paths Furhat has used over the years
possible_paths = [
    "/furhat/event",   # Standard Legacy
    "/event",          # Simplified
    "/api/event",      # Alternative
    "/furhat/say",     # Test: Can we make it speak?
    "/say"             # Test: Simplified speak
]

print(f"--- Probing Furhat on Port {PORT} ---")

for path in possible_paths:
    url = f"http://{BASE_IP}:{PORT}{path}"
    try:
        # We send a dummy event just to see if we get a 200 OK or 404
        # If testing 'say', we send text. If 'event', we send a dummy event.
        if "say" in path:
            payload = {"text": "Can you hear me?"}
        else:
            payload = {"event_name": "TestEvent", "data": {}}

        response = requests.post(url, json=payload, timeout=2)
        
        if response.status_code == 200:
            print(f"✅ SUCCESS! Found correct path: {path}")
            print(f"   (Robot might have said something or accepted the event)")
            break # Stop looking, we found it
        elif response.status_code == 404:
             print(f"❌ 404 Not Found: {path}")
        else:
             print(f"⚠️  Connected but got status {response.status_code}: {path}")

    except Exception as e:
        print(f"🚫 Connection Failed to {url}: {e}")

print("---------------------------------------")