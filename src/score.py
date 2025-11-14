"""
A module that handles persistent storage of highscores.
JSON files will be used to implement this features.
"""
import json

HIGHSCORES = 'storage/highscores.json'

def load_highscores():
    with open(HIGHSCORES, 'r') as file:
        return json.load(file)

def save_highscores(highscores):
    with open(HIGHSCORES, 'w') as file:
        json.dump(highscores, file, indent=4)

def update_highscores(level_idx, score, highscores):
    level = f"level_{level_idx}"
    if level not in highscores:
        highscores[level] = 0 # initialise level if non-existent

    # Check whether the highscore was beaten
    if score > highscores[level]:
        highscores[level] = score
        save_highscores(highscores)
