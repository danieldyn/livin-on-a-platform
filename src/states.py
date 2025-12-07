"""
A module that contains all states that the game can reach.
These are meant to be used by main.py to control the flow of the game loop.
"""
from abc import ABC, abstractmethod
import pygame
import storage
from buttons import Button
from levels import Level
from worlds import create_world
from settings import screen, instructions, features, story, play_hint, story_hint, help_hint, feats_hint, reset_hint
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLOCK_SIZE
from sounds import SoundAssets

class State(ABC):
    """
    An abstract base class for a game state.
    It defines the common interface for all states, which will implement their own methods.
    """
    def __init__(self, game):
        self.game = game
        self.done = False
        self.next_state = None
        # IDEA: self.persistent_data = {} # Data to pass to the next state

    @abstractmethod
    def startup(self):
        """
        A method that is called when the state is first entered.
        """

    @abstractmethod
    def update(self):
        """
        A method that updates state logic, updating the screen.
        """

    def cleanup(self):
        """
        A method that is called when the state is exited.
        """
        self.done = False # Reset for next time

class MainMenu(State):
    """
    A class that implements the main menu state of the game.
    Features buttons, messages, music and a simple background.
    """
    def __init__(self, game):
        super().__init__(game)
        # Load the buttons once to reuse
        self.start_button = Button(300, 600, "Start")
        self.start_button.get_img("button_images_01", 5, "png")

        self.story_button = Button(643, 600, "Story")
        self.story_button.get_img("button_images_01", 5, "png")

        self.help_button = Button(472, 600, "Help")
        self.help_button.get_img("button_images_01", 5, "png")

        self.feats_button = Button(SCREEN_WIDTH - 150, 5, "Feats")
        self.feats_button.get_img("button_images_01", 5, "png")

        self.quit_button = Button(5, 5, "Quit")
        self.quit_button.get_img("button_images_01", 5, "png")

        self.reset_button = Button(472, 710, "Reset")
        self.reset_button.get_img("button_images_01", 5, "png")

        # Play music once, upon instantiation
        SoundAssets.menu_music.play(loops=-1)

        # Store main menu world inside a Level object
        world_main_menu = create_world("../assets/worlds/main_menu.txt")
        self.level_instance = Level('../assets/backgrounds/sky.jpg', world_main_menu, 0, 900, SCREEN_HEIGHT / 2)


    def startup(self):
        """
        Entering the main menu.
        """
        # Reset buttons to receive input and start music
        self.start_button.reset()
        self.story_button.reset()
        self.help_button.reset()
        self.feats_button.reset()
        self.quit_button.reset()
        self.reset_button.reset()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        self.level_instance.display_world()
        self.level_instance.display_objects()
        self.level_instance.display_player(False, False)

        # Display game name (fancy)
        msg = "Livin' on a Platform"
        font = self.game.title_font
        x, y = 270, 300
        # Shadow
        screen.blit(font.render(msg, True, (50, 50, 50)), (x + 3, y + 3))
        # Outline (4 directions)
        for ox, oy in [(-2,0), (2,0), (0,-2), (0,2)]:
            screen.blit(font.render(msg, True, (255, 255, 255)), (x + ox, y + oy))
        # Main text
        screen.blit(font.render(msg, True, BLACK), (x, y))

        # Display hints using hardcoded values to fit well in the chosen background
        y = 500
        for line in play_hint:
            text = self.game.text_font.render(line, True, BLACK)
            screen.blit(text, (80, y))
            y = y + 25
        y = 475
        for line in help_hint:
            text = self.game.text_font.render(line, True, BLACK)
            screen.blit(text, (440, y))
            y = y + 25
        y = 500
        for line in story_hint:
            text = self.game.text_font.render(line, True, BLACK)
            screen.blit(text, (800, y))
            y = y + 25
        y = 90
        for line in feats_hint:
            text = self.game.text_font.render(line, True, BLACK)
            screen.blit(text, (750, y))
            y = y + 25
        y = 785
        for line in reset_hint:
            text = self.game.text_font.render(line, True, BLACK)
            screen.blit(text, (80, y))
            y = y + 25

        # Update buttons and check for input
        self.start_button.update()
        self.help_button.update()
        self.story_button.update()
        self.feats_button.update()
        self.quit_button.update()
        self.reset_button.update()

        if self.help_button.was_pressed >= 1:
            self.done = True
            self.next_state = "help"

        if self.story_button.was_pressed >= 1:
            self.done = True
            self.next_state = "story"

        if self.feats_button.was_pressed >= 1:
            self.done = True
            self.next_state = "feats"

        if self.start_button.was_pressed >= 1:
            self.done = True
            self.next_state = "gameplay"
            SoundAssets.menu_music.stop() # levels have a different soundtrack

        if self.quit_button.was_pressed >= 1:
            self.game.running = False

        if self.reset_button.was_pressed >= 1:
            storage.new_save(0) # overwrite save file
            reset_hint[2] = "Successfully reset save! -----"

        self.level_instance.display_update()

class HelpScreen(State):
    """
    A class that implements the 'Help' instructions screen.
    Features a Return button and lines of text.
    """
    def __init__(self, game):
        super().__init__(game)
        self.bg = pygame.image.load('../assets/backgrounds/help.jpg')
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.return_button = Button(620, 670, "Menu")
        self.return_button.get_img("button_images_01", 5, "png")
        self.next_button = Button(620, 670, "Next")
        self.next_button.get_img("button_images_01", 5, "png")
        self.page = None

    def startup(self):
        """
        Entering the help menu.
        """
        self.page = 1 # Enter the menu on the first page
        # Reset the buttons to receive input
        self.return_button.reset()
        self.next_button.reset()

    def draw_text(self, source):
        """
        Draws the lines of text from source with proper alignment and partially transparent background.
        """
        y = 60
        for line in source:
            text = self.game.text_font.render(line, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (200, y))
            screen.blit(text, (200, y))
            y = y + 40

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        # Draw the background and choose paragraph depending on page number
        screen.blit(self.bg, (0, 0))
        if self.page == 1:
            self.draw_text(instructions)
            # Wait for the user to want to go to the next page
            self.next_button.update()
            if self.next_button.was_pressed >= 1:
                self.page = 2

        elif self.page == 2:
            self.draw_text(features)
            # Wait for the user to want to return to the main menu or the other page
            self.return_button.update()
            if self.return_button.was_pressed >= 1:
                self.done = True
                self.next_state = "main_menu"

        pygame.display.update()

class StoryScreen(State):
    """
    A class that implements the 'Story' screen.
    Features a Return button and lines of text.
    """
    def __init__(self, game):
        super().__init__(game)
        self.bg = pygame.image.load('../assets/backgrounds/story.jpg')
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.return_button = Button(750, 673, "Back")
        self.return_button.get_img("button_images_01", 5, "png")

    def startup(self):
        """
        Entering the story menu.
        """
        # Reset the return button to receive input
        self.return_button.reset()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        # Draw the paragraphs and the background
        screen.blit(self.bg, (0, 0))
        y = 140
        for line in story:
            text = self.game.text_font.render(line, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (200, y))
            screen.blit(text, (200, y))
            y = y + 40

        # Wait for the user to want to return to the main menu
        self.return_button.update()
        if self.return_button.was_pressed >= 1:
            self.done = True
            self.next_state = "main_menu"

        pygame.display.update()

class FeatsScreen(State):
    """
    A class that implements the 'Feats' screen.
    Features a Return button and information about the player's achievements.
    """
    def __init__(self, game):
        super().__init__(game)
        self.bg = pygame.image.load('../assets/backgrounds/feats.jpg')
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.return_button = Button(750, 673, "Back")
        self.return_button.get_img("button_images_01", 5, "png")

    def startup(self):
        """
        Entering the feats menu.
        """
        # Reset the return button to receive input
        self.return_button.reset()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        # Draw the paragraphs and the background
        screen.blit(self.bg, (0, 0))
        y = 140
        text = self.game.text_font.render("Level Highscores", True, WHITE)
        text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 158)) # partially transparent background
        screen.blit(text_surf, (200, y))
        screen.blit(text, (200, y))
        y = y + 80

        x = 200
        highscores = storage.highscores_to_string()
        for score in highscores:
            text = self.game.text_font.render(score, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (x, y))
            screen.blit(text, (x, y))
            y = y + 40
            if y == 620:
                y = 220
                x = 600

        # Display final hint
        text = self.game.text_font.render("Ready to play now? --------------->", True, WHITE)
        text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 158)) # partially transparent background
        screen.blit(text_surf, (200, 700))
        screen.blit(text, (200, 700))

        # Wait for the user to want to return to the main menu
        self.return_button.update()
        if self.return_button.was_pressed >= 1:
            self.done = True
            self.next_state = "main_menu"

        pygame.display.update()

class Gameplay(State):
    """
    A class that implements the main gameplay state, managing the sequence of levels.
    Features a list of levels, worlds, state checks for the current level and relies on levels to run their own logic.
    """
    def __init__(self, game):
        super().__init__(game)
        # Create worlds once
        world_level_01 = create_world("../assets/worlds/world1.txt")
        world_level_02 = create_world("../assets/worlds/world2.txt")
        world_level_03 = create_world("../assets/worlds/world3.txt")
        world_level_04 = create_world("../assets/worlds/world4.txt")
        world_level_05 = create_world("../assets/worlds/world5.txt")
        world_level_06 = create_world("../assets/worlds/world6.txt") # contains secret level entry point
        world_level_07 = create_world("../assets/worlds/world7.txt")
        world_level_08 = create_world("../assets/worlds/world8.txt")
        world_level_09 = create_world("../assets/worlds/world9.txt")
        world_level_10 = create_world("../assets/worlds/world10.txt")
        world_level_11 = create_world("../assets/worlds/world11.txt")
        final_world = create_world("../assets/worlds/final_world.txt")
        secret_world = create_world("../assets/worlds/secret.txt")
        secret_world1 = create_world("../assets/worlds/secret1.txt")

        # Initialise the sequence of worlds, backgrounds and indices once
        self.world_sequence = [
            ("../assets/backgrounds/sky.jpg", world_level_01, 1, 10 * BLOCK_SIZE, SCREEN_HEIGHT - 7 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_02, 2, 9 * BLOCK_SIZE, SCREEN_HEIGHT - 7 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_03, 3, 5 * BLOCK_SIZE, 19 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_04, 4, 5 * BLOCK_SIZE, SCREEN_HEIGHT - 3 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_05, 5, 5 * BLOCK_SIZE, SCREEN_HEIGHT - 11 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_06, 6, SCREEN_WIDTH - 3 * BLOCK_SIZE, SCREEN_HEIGHT - 8 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_07, 7, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            ("../assets/backgrounds/sky.jpg", world_level_08, 8, 3 * BLOCK_SIZE, SCREEN_HEIGHT - 9 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_09, 8, 2 * BLOCK_SIZE, SCREEN_HEIGHT - 27 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_10, 9, 15 * BLOCK_SIZE, SCREEN_HEIGHT - 8 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", world_level_11, 10, 3 * BLOCK_SIZE, SCREEN_HEIGHT - 13 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", final_world, 10, 2 * BLOCK_SIZE, SCREEN_HEIGHT - 6 * BLOCK_SIZE)
        ]
        self.secret_world_sequence = [
            # The last level is only accesible by interacting with the All Powerful Acorn
            ("../assets/backgrounds/sky.jpg", secret_world, 2, 70, SCREEN_HEIGHT - 7 * BLOCK_SIZE),
            ("../assets/backgrounds/sky.jpg", secret_world1, 2, 6 * BLOCK_SIZE, SCREEN_HEIGHT - 11 * BLOCK_SIZE)
        ]
        self.level_list = []
        self.secret_level_list = []
        self.level_idx = 0
        self.secret_level_idx = 0
        self.current_level = None
        self.start_secret = False

    def startup(self):
        """
        Entering the gameplay state (pressed Start in main menu)
        """
        # Initialise all levels in advance
        self.level_list = [Level(bg, world, idx, start_x, start_y)
                            for bg, world, idx, start_x, start_y in self.world_sequence]
        # Initialise all (secret) levels in advance
        self.secret_level_list = [Level(bg, world, idx, start_x, start_y)
                            for bg, world, idx, start_x, start_y in self.secret_world_sequence]
        # Determine which level will be run
        self.game.last_played_level = storage.load_save() # sync save file
        if self.game.last_played_level >= len(self.level_list):
            self.game.last_played_level = 0

        self.level_idx = self.game.last_played_level
        self.level_idx = max(self.level_idx, 0)

        self.current_level = self.level_list[self.level_idx]
        self.current_level.reset()

    def update(self):
        """
        Runs the current level, checking for clear changes of state.
        If it finishes, transition to the next level or back to the main menu via buttons.
        """
        if self.current_level.running:
            if self.level_idx == len(self.level_list) - 1: # last level
                self.current_level.run_level(True)
            else:
                self.current_level.run_level()
            if self.current_level.player.touched_acorn == True:
                self.start_secret = True
        else:
            if self.start_secret:
                if self.secret_level_idx == 0 and self.secret_level_list:
                    current_lives = self.current_level.player.lives
                    self.current_level = self.secret_level_list[self.secret_level_idx]
                    self.secret_level_idx += 1
                    # self.current_level.player.touched_acorn = True
                    self.current_level.reset()
                    self.current_level.player.lives = current_lives
                elif self.current_level.state == "next" and self.secret_level_idx < len(self.secret_level_list):
                    current_lives = self.current_level.player.lives
                    self.current_level = self.secret_level_list[self.secret_level_idx]
                    self.secret_level_idx += 1
                    # self.current_level.player.touched_acorn = True
                    self.current_level.reset()
                    self.current_level.player.lives = current_lives
                else:
                    # after all the secret levels are over, the player is sent back to the normal level he came from
                    self.current_level.reset()
                    self.current_level = self.level_list[self.level_idx]
                    self.current_level.player.touched_acorn = False
                    self.current_level.running = True
                    
                    self.current_level.state = "playing"
                    
                    # self.level_idx -= 1
                    # print(self.level_idx)
                    self.start_secret = False
            # The current level ended (Win or Lose)
            elif self.current_level.state == "next" and self.level_idx + 1 < len(self.level_list):
                # Move to the next level
                current_lives = self.current_level.player.lives
                self.level_idx += 1
                self.current_level = self.level_list[self.level_idx]
                self.current_level.reset()
                self.current_level.player.lives = current_lives
            else:
                # Check if the player finished the game
                if self.level_idx + 1 >= len(self.level_list) and self.current_level.state == "next":
                    ending_font = pygame.font.Font('../assets/fonts/PixelOperator8-Bold.ttf', 45)
                    bg_surf = pygame.image.load('../assets/backgrounds/ending.jpg')
                    bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    ending_surf = ending_font.render('You have finished the game!', True, (64, 64, 64))
                    ending_rect = ending_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
                    screen.blit(bg_surf, (0, 0))
                    screen.blit(ending_surf, ending_rect)
                    pygame.display.update()
                    pygame.time.delay(3000) # stay on the victory screen for 3 seconds

                # Lost, exited, or finished victory screen
                self.done = True
                self.next_state = "main_menu"
                SoundAssets.menu_music.play(loops=-1)

    def cleanup(self):
        """
        Resets level list when leaving the gameplay state, allowing to restart fresh.
        Overrides the inherited methods from State.
        """
        self.level_list = []
        self.level_idx = 0
        self.current_level = None
        super().cleanup()
