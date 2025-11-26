"""
Main entry point for the platformer game.
Initialises Pygame, handles menu logic and states using two fundamental classes.
"""
import pygame
import storage
from settings import screen, FPS
from states import MainMenu, HelpScreen, StoryScreen, Gameplay, FeatsScreen

class Game():
    """
    A class that implements the main game controller.
    Manages the game loop, states, and shared resources.
    """
    def __init__(self):
        pygame.init()
        self.screen = screen # Use the screen from settings
        self.clock = pygame.time.Clock()
        self.running = True

        # Load shared assets
        self.load_shared_assets()

        # State setup as a dictionary
        self.states = {
            "main_menu": MainMenu(self),
            "help": HelpScreen(self),
            "story": StoryScreen(self),
            "feats": FeatsScreen(self),
            "gameplay": Gameplay(self),
        }

        # Load save file
        self.last_played_level = storage.load_save()

        # Set initial state to main menu
        self.state_name = "main_menu"
        self.state = self.states["main_menu"]
        self.state.startup()

    def load_shared_assets(self):
        """
        A method that loads assets that are used across multiple states.
        """
        self.text_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8.ttf', 20)

    def handle_events(self):
        """
        A method that lets the current state handle events, unless they are the quit signal.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        A method that updates the current state and checks for transitions.
        """
        self.state.update()
        if self.state.done:
            self.transition_state()

    def transition_state(self):
        """
        A method that changes from the current state to the next.
        """
        self.state.cleanup()
        self.state_name = self.state.next_state
        self.state = self.states[self.state_name]
        self.state.startup()

    def run(self):
        """
        A method that implements the main game loop.
        Will be very simplistic because of other methods.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(FPS)

# Main execution
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
