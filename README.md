# Interactive Storyteller

An emotion-adaptive interactive storytelling system built around the Furhat robot.  
Stories adapt in real time based on detected user emotions, intents, and choices.

## Core Capabilities
- Real-time facial emotion recognition (CNN, FER-2013 based)
- Rule-based Finite State Machine (FSM) for dialogue control
- Emotion-aware branching stories stored as JSON
- Optional LLM-based narration constrained by FSM logic
- Speech interaction via Furhat SDK

## Project Structure
IIS_PROJECT/
├─ data/
│ ├─ raw/ # original datasets
│ └─ processed/
│ └─ LLM/ # story JSONs for LLM/FSM
│ ├─ LLM_lk.json # Lantern Keeper
│ ├─ LLM_sa.json # Stardust Arena
│ └─ LLM_as.json # Abandoned Station
│
├─ notebooks/
│ └─ LLM_powered_storyteller.ipynb # Runs the storytelling session; contains all dialogue and handles LLM
│
├─ src/
│ ├─ perception/ # Emotion recognition & Furhat bridge
│ │ ├─ bridge.py
│ │ ├─ integrated_demo.py
│ │ ├─ probe_furhat.py
│ │ ├─ test_emotion.py
│ │ ├─ train_custom_model.py
│ │ └─ my_emotion_model_*.keras # Correct version as of right now is v3
│ │
│ ├─ preprocessing/ # As of right now empty data preprocessing
│ ├─ training/ # As of right now empty model training utilities
│ └─ evaluation/ # As of right now empty evaluation scripts
│
├─ gemini_api_key.env # API key (gitignored)
├─ .gitignore
├─ LICENSE
└─ README.md


## Story Themes
- **Lantern Keeper’s Quiet Night** – calm, comforting
- **Stardust Arena Trials** – energetic, action-oriented
- **Abandoned Train Station** – neutral, exploratory

## Tech Stack
- Python
- TensorFlow / Keras
- OpenCV
- Furhat SDK
- Gemini API (as of right now)

## Setup
1. Clone the repository  
2. Install Python dependencies  
3. Add your API key to `gemini_api_key.env`  
4. Run emotion detection (`src/perception/`)  
5. Start the Furhat dialogue system
6. Run the entire notebook

## Usage
- Speak to the robot
- Emotion is detected via webcam
- FSM selects and adapts story scenes in real time

## Contributors
- Abhishek Yadav  
- Karin Haglund  
- Molly Börjes  
- Sparsh Paliya  

## License
Educational / academic use only.
