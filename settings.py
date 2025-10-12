# General usage parameters and game settings

BLOCK_SIZE = 16 # px
SCREEN_WIDTH = 1152 # 16px * 72 blocks
SCREEN_HEIGHT = 864 # 16px * 54 blocks
LOSS_SCREEN_DURATION = 5000 # miliseconds
FPS = 60
RUNNING_IMAGE_INCREMENT = 0.1
ROLLING_IMAGE_INCREMENT = 0.15 # faster rolling animation
IDLE_IMAGE_INCREMENT = 0.1
OBJECT_IMAGE_INCREMENT = 0.1
BUTTON_IMAGE_INCREMENT = 0.35

# Level and main menu settings

MAIN_MENU = True



# screen setup
from pygame import display
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# mixer setup
from pygame import mixer
mixer.init()

# initialise sound effects
loss_sound = mixer.Sound('brackeys_platformer_assets/sounds/player_losing.wav')
coin_sound = mixer.Sound('brackeys_platformer_assets/sounds/coin.wav') # two options here, also coin_collected.wav

# background music for levels
mixer.music.load('brackeys_platformer_assets/music/game_level_music.wav')
mixer.music.play()
volume = mixer.music.get_volume()
mixer.music.set_volume(volume - 0.5) # test option
mixer.music.play(-1) # loop forever
