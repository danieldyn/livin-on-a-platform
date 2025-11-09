"""
General usage parameters and settings for the game.
This module is meant to be shared by others, avoiding cross-import errors.
"""
from pygame import display
from pygame import mixer

# constants
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
WHITE = (255, 255, 255)
BLACK = (64, 64, 64)

# screen setup
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# mixer setup
mixer.init()

# initialise sound effects
loss_sound = mixer.Sound('../brackeys_platformer_assets/sounds/player_losing.wav')
victory_sound = mixer.Sound('../brackeys_platformer_assets/sounds/victory.wav')
coin_sound = mixer.Sound('../brackeys_platformer_assets/sounds/coin.wav')
button_sound = mixer.Sound('../brackeys_platformer_assets/sounds/button_sound.mp3')
chest_sound = mixer.Sound('../brackeys_platformer_assets/sounds/chest.wav')
hit_sound = mixer.Sound('../brackeys_platformer_assets/sounds/hit.mp3')
menu_sound = mixer.Sound('../brackeys_platformer_assets/sounds/background.mp3')

# background music for levels
mixer.music.load('../brackeys_platformer_assets/music/game_level_music.wav')
volume = mixer.music.get_volume()
mixer.music.set_volume(volume - 0.5) # test option

# menu texts
instructions = [
    "Game Instructions",
    "Make your way through the worlds as quickly and",
    "as efficiently as possible. Your performance will",
    "be evaluated based on completion time and the",
    "amount of coins collected on the way. Think your",
    "approach carefully, as some treasures are guarded",
    "by deadly traps and elusive enemies!",
    "",
    "Controls",
    "Move the player using Right Arrow and Left Arrow.",
    "Press Space to jump and Right Shift to roll.",
    "Press Enter to collect Chests and touch the Flag.",
    "Left click on buttons to interact with them.",
    "",
    "Ready to play now? --------------->"
]

story = [
    "Game Story",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit,",
    "sed do eiusmod tempor incididunt ut labore et dolore magna",
    "aliqua. Ut enim ad minim veniam, quis nostrud exercitation",
    "ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "Duis aute irure dolor in reprehenderit in voluptate velit",
    "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint",
    "occaecat cupidatat non proident, sunt in culpa qui officia",
    "deserunt mollit anim id est laborum."
    "",
    "Lorem",
    "ipsum",
    "dolor",
    "sit",
    "",
    "Ready to play now? --------------->"
]

play_hint = [
    "Press to begin!",
    "          I",
    "          I",
    "          I",
    "          I",
    "          ------->",
]

help_hint = [
    "Need any help?",
    "          I",
    "          I",
    "          I",
    "          V"
]

story_hint = [
    "Check out the story!",
    "              I",
    "              I",
    "              I",
    "              I",
    "<---------",
]
