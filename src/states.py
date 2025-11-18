"""
A module that contains all states that the game can reach.
These are meant to be used by main.py to control the flow of the game loop.
"""
import pygame
import storage
from abc import ABC, abstractmethod
from buttons import Button
from levels import Level, main_menu
from worlds import world_level_01, world_level_02
from settings import screen, instructions, story, play_hint, story_hint, help_hint, feats_hint
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
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

    def startup(self):
        """
        Entering the main menu.
        """
        # Reset buttons to receive input and start music
        self.start_button.reset()
        self.story_button.reset()
        self.help_button.reset()
        self.feats_button.reset()
        SoundAssets.menu_music.play()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        main_menu.display_world()
        main_menu.display_objects()

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

        # Update buttons and check for input
        self.start_button.update()
        self.help_button.update()
        self.story_button.update()
        self.feats_button.update()

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

        main_menu.display_update()

class HelpScreen(State):
    """
    A class that implements the 'Help' instructions screen.
    Features a Return button and lines of text.
    """
    def __init__(self, game):
        super().__init__(game)

    def startup(self):
        """
        Entering the help menu.
        """
        # Reset return button to receive input
        self.game.return_button.reset()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        # Draw the paragraphs and the background
        screen.blit(self.game.alt_bg, (0, 0))
        y = 140
        for line in instructions:
            text = self.game.text_font.render(line, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (200, y))
            screen.blit(text, (200, y))
            y = y + 40

        # Wait for the user to want to return to the main menu
        self.game.return_button.update()
        if self.game.return_button.was_pressed >= 1:
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

    def startup(self):
        """
        Entering the story menu.
        """
        # Reset the return button to receive input
        self.game.return_button.reset()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        # Draw the paragraphs and the background
        screen.blit(self.game.alt_bg, (0, 0))
        y = 140
        for line in story:
            text = self.game.text_font.render(line, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (200, y))
            screen.blit(text, (200, y))
            y = y + 40

        # Wait for the user to want to return to the main menu
        self.game.return_button.update()
        if self.game.return_button.was_pressed >= 1:
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

    def startup(self):
        """
        Entering the feats menu.
        """
        # Reset the return button to receive input
        self.game.return_button.reset()

    def update(self):
        """
        Updates buttons, draws everything and checks for transition.
        """
        # Draw the paragraphs and the background
        screen.blit(self.game.alt_bg, (0, 0))
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
        self.game.return_button.update()
        if self.game.return_button.was_pressed >= 1:
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
        # Initialise the sequence of worlds, backgrounds and indices once
        self.world_sequence = [
            ("../backgrounds/sky.jpg", world_level_01, 1),
            ("../backgrounds/sky.jpg", world_level_02, 2)
        ]
        self.level_list = []
        self.level_idx = 0
        self.current_level = None

    def startup(self):
        """
        Entering the gameplay state (pressed Start in main menu)
        """
        # Initialise all levels in advance
        self.level_list = [Level(bg, world, idx) for bg, world, idx in self.world_sequence]
        # Determine which level will be run
        if self.game.last_played_level == len(self.level_list):
            self.game.last_played_level = 1

        self.level_idx = self.game.last_played_level - 1
        if self.level_idx < 0:
            self.level_idx = 0

        self.current_level = self.level_list[self.level_idx]
        self.current_level.reset()

    def update(self):
        """
        Runs the current level, checking for clear changes of state.
        If it finishes, transition to the next level or back to the main menu via buttons.
        """
        if self.current_level.running:
            self.current_level.run_level()
        else:
            # The current level ended (Win or Lose)
            if self.current_level.state == "next" and self.level_idx + 1 < len(self.level_list):
                # Move to the next level
                self.level_idx += 1
                self.current_level = self.level_list[self.level_idx]
                self.current_level.reset()
            else:
                # Check if the player finished the game
                if self.level_idx + 1 >= len(self.level_list) and self.current_level.state == "next":
                    ending_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 45)
                    bg_surf = pygame.image.load('../backgrounds/ending.jpg')
                    bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    ending_surf = ending_font.render(f'You have finished the game!', True, (64, 64, 64))
                    ending_rect = ending_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
                    screen.blit(bg_surf, (0, 0))
                    screen.blit(ending_surf, ending_rect)
                    pygame.display.update()
                    pygame.time.delay(3000) # stay on the victory screen for 3 seconds

                # Lost, exited, or finished victory screen
                self.done = True
                self.next_state = "main_menu"
                SoundAssets.menu_music.play()

    def cleanup(self):
        """
        Resets level list when leaving the gameplay state, allowing to restart fresh.
        Overrides the inherited methods from State.
        """
        self.level_list = []
        self.level_idx = 0
        self.current_level = None
        super().cleanup()
