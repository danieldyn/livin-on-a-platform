from pygame import mixer
from abc import ABC

# initialise sound effects
class SoundAssets(ABC):
    loss = mixer.Sound('../brackeys_platformer_assets/sounds/player_losing.wav')
    victory = mixer.Sound('../brackeys_platformer_assets/sounds/victory.wav')
    coin = mixer.Sound('../brackeys_platformer_assets/sounds/coin.wav')
    button = mixer.Sound('../brackeys_platformer_assets/sounds/button_sound.mp3')
    chest = mixer.Sound('../brackeys_platformer_assets/sounds/chest.wav')
    hit = mixer.Sound('../brackeys_platformer_assets/sounds/hit.mp3')
    menu_music = mixer.Sound('../brackeys_platformer_assets/sounds/background.mp3')