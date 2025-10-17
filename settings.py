# General usage parameters and game settings

BLOCK_SIZE = 16 # px
SCREEN_WIDTH = 72 * BLOCK_SIZE
SCREEN_HEIGHT = 54 * BLOCK_SIZE
FPS = 60
RUNNING_IMAGE_INCREMENT = 0.1
ROLLING_IMAGE_INCREMENT = 0.15 # faster rolling animation
IDLE_IMAGE_INCREMENT = 0.1
OBJECT_IMAGE_INCREMENT = 0.1
BUTTON_IMAGE_INCREMENT = 0.35
COIN_MULTIPLIER = 10

# screen setup
from pygame import display
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# mixer setup
from pygame import mixer
mixer.init()

# initialise sound effects
loss_sound = mixer.Sound('brackeys_platformer_assets/sounds/player_losing.wav')
victory_sound = mixer.Sound('brackeys_platformer_assets/sounds/victory.wav')
coin_sound = mixer.Sound('brackeys_platformer_assets/sounds/coin.wav') # two options here, also coin_collected.wav
button_sound = mixer.Sound('brackeys_platformer_assets/sounds/button_sound.mp3')
chest_sound = mixer.Sound('brackeys_platformer_assets/sounds/chest.wav')
hit_sound = mixer.Sound('brackeys_platformer_assets/sounds/hit.mp3')
menu_sound = mixer.Sound('brackeys_platformer_assets/sounds/background.mp3')

# background music for levels
mixer.music.load('brackeys_platformer_assets/music/game_level_music.wav')
volume = mixer.music.get_volume()
mixer.music.set_volume(volume - 0.5) # test option
