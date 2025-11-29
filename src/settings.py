"""
General usage parameters and settings for the game.
This module is meant to be shared by others, avoiding cross-import errors.
"""
from pygame import display
from pygame import mixer
import storage
# import 'sub'classes

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
COIN_MULTIPLIER = 50
WHITE = (255, 255, 255)
BLACK = (64, 64, 64)

# screen setup
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# mixer setup
mixer.init()

# background music for levels
mixer.music.load('../assets/music/game_level_music.wav')
volume = mixer.music.get_volume()
mixer.music.set_volume(volume - 0.5) # test option

# persistent JSON files
highscores = storage.load_highscores()
savefile = storage.load_save()

# menu texts
instructions = [
    "Game Instructions",
    "",
    "Make your way through the worlds as quickly and",
    "as efficiently as possible. Your performance will",
    "be evaluated based on completion time and the",
    "amount of coins collected on the way. Think your",
    "approach carefully, as some pathways are guarded",
    "by deadly traps and elusive enemies!",
    "",
    "Controls",
    "",
    "Move the player using Right Arrow and Left Arrow.",
    "Press Space to jump and Right Shift to roll.",
    "Press Enter to collect Chests and touch the Flag.",
    "Left click on buttons to interact with them.",
    "",
    "Find out more ------------>"
]

features = [
    "Game Features - What to expect",
    "",
    "You will have a maximum of 3 lives, which carry on",
    "between levels - every mistake counts! Watch out for",
    "hearts you can collect along the way. Being hit will",
    "grant you 2 seconds of invulnerability to bounce back.",
    "",
    "Chests can be a great source of bonus coins, make sure",
    "you interact with them using Enter. It won't always be",
    "easy to get to them. Also, they never award bonus hearts.",
    "",
    "Your progress is automatically saved when completing a",
    "level. By default, the Start button in the main menu will",
    "launch the level after the last completed one, if any. You",
    "can freely reset and start fresh using the Reset button.",
    "",
    "Ready to play now? ------->"
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
    "Press to play!",
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

feats_hint = [
    "                               ^",
    "                               I",
    "                               I",
    "Check out your records!"
]

reset_hint = [
    "                                             ^",
    "                                             |",
    "Want to reset your save? -----"
]
