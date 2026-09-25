"""
A module that handles persistent storage of important data.
Uses browser localStorage in Pygbag/WASM, and local JSON files on desktop.
"""

import datetime
import json
import os
import sys

# Detect WebAssembly environment
IS_WASM = sys.platform == "emscripten"

if IS_WASM:
    import platform

    window = platform.window
else:
    # Use paths relative to project root or script location
    STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")
    HIGHSCORES = os.path.join(STORAGE_DIR, "highscores.json")
    SAVEFILE = os.path.join(STORAGE_DIR, "last_save.json")


def load_highscores():
    """
    Loads highscores from localStorage (web) or JSON file (desktop).
    """
    if IS_WASM:
        raw = window.localStorage.getItem("game_highscores")
        if raw:
            try:
                return json.loads(str(raw))
            except json.JSONDecodeError:
                return {}
        return {}

    try:
        with open(HIGHSCORES, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_highscores(highscores):
    """
    Saves highscores to localStorage (web) or JSON file (desktop).
    """
    data_str = json.dumps(highscores, indent=4)
    if IS_WASM:
        window.localStorage.setItem("game_highscores", data_str)
        return

    os.makedirs(os.path.dirname(HIGHSCORES), exist_ok=True)
    with open(HIGHSCORES, "w", encoding="utf-8") as file:
        file.write(data_str)


def update_highscores(level_idx, score, highscores):
    """
    Updates the highscore for level level_idx if score beats the currently existing one.
    """
    level = f"level_{level_idx}"
    if level not in highscores:
        highscores[level] = 0

    if score > highscores[level]:
        highscores[level] = score
        save_highscores(highscores)


def get_highscore(level_idx, highscores):
    """
    Returns the highscore stored for level level_idx.
    """
    level = f"level_{level_idx}"
    return highscores.get(level, 0)


def highscores_to_string():
    """
    Returns all stored highscores as a list of strings.
    """
    highscores_data = load_highscores()
    display_list = []

    for level_key, score in highscores_data.items():
        level_idx = level_key.split("_")[-1]
        display_list.append(f"Level {level_idx}: {score}")

    display_list.sort(key=lambda s: int(s.split(":")[0].split(" ")[-1]))
    return display_list


def new_save(level_idx):
    """
    Saves last completed level and timestamp.
    """
    data = {
        "last_completed_level": level_idx,
        "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    data_str = json.dumps(data, indent=4)

    if IS_WASM:
        window.localStorage.setItem("game_savefile", data_str)
        return

    os.makedirs(os.path.dirname(SAVEFILE), exist_ok=True)
    with open(SAVEFILE, "w", encoding="utf-8") as file:
        file.write(data_str)


def load_save():
    """
    Loads last completed level.
    """
    if IS_WASM:
        raw = window.localStorage.getItem("game_savefile")
        if raw:
            try:
                data = json.loads(str(raw))
                return data.get("last_completed_level", 0)
            except json.JSONDecodeError:
                return 0
        return 0

    if not os.path.exists(SAVEFILE):
        return 0

    try:
        with open(SAVEFILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("last_completed_level", 0)
    except (json.JSONDecodeError, ValueError):
        return 0
