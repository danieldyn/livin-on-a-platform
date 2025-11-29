"""
A module that handles persistent storage of important data.
JSON files will be used to implement this feature.
"""
import json
import os
from datetime import datetime

HIGHSCORES = '../storage/highscores.json'
SAVEFILE = '../storage/last_save.json'

def load_highscores():
    """
    Loads highscores from the path stored in global variable HIGHSCORES.
    """
    try:
        with open(HIGHSCORES, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_highscores(highscores):
    """
    Saves highscores to the path stored in global variable HIGHSCORES.
    """
    with open(HIGHSCORES, 'w', encoding='utf-8') as file:
        json.dump(highscores, file, indent=4)

def update_highscores(level_idx, score, highscores):
    """
    Updates the highscore for level level_idx if score beats the currently existing one.
    """
    level = f"level_{level_idx}"
    if level not in highscores:
        highscores[level] = 0 # initialise level if non-existent

    # Check whether the highscore was beaten
    if score > highscores[level]:
        highscores[level] = score
        save_highscores(highscores)

def get_highscore(level_idx, highscores):
    """
    Returns the highscore stored for level level_idx.
    """
    level = f"level_{level_idx}"
    if level in highscores:
        return highscores[level]
    return 0

def highscores_to_string():
    """
    Returns all stored highscores as a list of strings.
    """
    highscores_data = load_highscores()
    display_list = []

    for level_key, score in highscores_data.items():
        # Extract the level number and reformat the line
        level_idx = level_key.split('_')[-1]
        level_string = f"Level {level_idx}: {score}"
        display_list.append(level_string)

    # Sort the list by level number
    display_list.sort(key=lambda s: int(s.split(':')[0].split(' ')[-1]))

    return display_list

def new_save(level_idx):
    """
    Edits the local savefile at path SAVEFILE, adding the last completed level and a timestamp.
    """
    data = {
        "last_completed_level": level_idx,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    with open(SAVEFILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def load_save():
    """
    Loads the local savefile at path SAVEFILE.
    """
    if not os.path.exists(SAVEFILE):
        return 0

    try:
        with open(SAVEFILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get("last_completed_level", 0)
    except (json.JSONDecodeError, ValueError):
        return 0
