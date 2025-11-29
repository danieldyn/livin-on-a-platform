"""
A module that handles the collection of sounds used in the game.
"""
from abc import ABC
from pygame import mixer

# initialise sound effects
class SoundAssets(ABC, mixer.Sound):
    """
    A class that contains all sounds and music used in the game.
    """
    loss = mixer.Sound('../assets/sounds/player_losing.wav')
    victory = mixer.Sound('../assets/sounds/victory.wav')
    coin = mixer.Sound('../assets/sounds/coin.wav')
    button = mixer.Sound('../assets/sounds/button_sound.mp3')
    chest = mixer.Sound('../assets/sounds/chest.wav')
    hit = mixer.Sound('../assets/sounds/hit.mp3')
    hurt = mixer.Sound('../assets/sounds/hurt.mp3')
    menu_music = mixer.Sound('../assets/sounds/background.mp3')
    heart = mixer.Sound('../assets/sounds/heart_sound.wav')
