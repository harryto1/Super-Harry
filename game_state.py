import json


def load_game_state():
    try:
        with open('game_state.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"level_1_completed": False, "level_2_completed": False}

def save_game_state(state):
    with open('game_state.json', 'w') as file:
        json.dump(state, file)

