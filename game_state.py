from pathlib import Path
import json

def ensure_folder_exists(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)

def load_game_state():
    ensure_folder_exists('data')
    try:
        with open('data/game_state.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"level_1_completed": False, "level_2_unlocked": False}

def save_game_state(state):
    ensure_folder_exists('data')
    with open('data/game_state.json', 'w') as file:
        json.dump(state, file)

