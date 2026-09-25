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

    loss = mixer.Sound("assets/sounds/player_losing.ogg")
    victory = mixer.Sound("assets/sounds/victory.ogg")
    coin = mixer.Sound("assets/sounds/coin.ogg")
    button = mixer.Sound("assets/sounds/button_sound.ogg")
    chest = mixer.Sound("assets/sounds/chest.ogg")
    hit = mixer.Sound("assets/sounds/hit.ogg")
    hurt = mixer.Sound("assets/sounds/hurt.ogg")
    menu_music = mixer.Sound("assets/sounds/background.ogg")
    heart = mixer.Sound("assets/sounds/heart_sound.ogg")
