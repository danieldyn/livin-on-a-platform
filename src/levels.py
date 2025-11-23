"""
A method that handles the game's levels.
"""
import pygame
import storage
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COIN_MULTIPLIER
from settings import screen, mixer, highscores
from character import player
from worlds import world_main_menu, reset_world
from buttons import Button
from objects import Object
from sounds import SoundAssets

restart_button = Button(400, 600, "Retry")
restart_button.get_img("button_images_01", 5, "png")

main_menu_button = Button(600, 600, "Quit")
main_menu_button.get_img("button_images_01", 5, "png")

next_button = Button(500, 700, "Next")
next_button.get_img("button_images_01", 5, "png")

class Level(SoundAssets):
    """
    A class that implements a level.
    The level contains a world and the player.
    The level has its own clock and score, based on performance.
    """
    def __init__(self, bg_img, world, idx):
        self.running = True
        self.idx = idx
        bg_surf = pygame.image.load(bg_img)
        self.bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.world = world
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.state = "playing"
        self.ending_time = 0
        self.fallen_buttons = False
        self.main_menu_button = None
        self.restart_button = None

    def reset(self):
        """
        A method resets a level.
        This will usually be used when restarting a level.
        Also, it is very useful when switching between levels.
        """
        self.start_time = pygame.time.get_ticks()
        self.state = "playing"
        player.player_is_alive = True
        player.reset()
        mixer.music.rewind()
        mixer.music.play()
        restart_button.reset()
        main_menu_button.reset()
        self.world = reset_world(self.world.file_path)
        next_button.reset()
        for obj in self.world.obj_list:
            obj.object_shown = True

    def display_world(self):
        """
        A method that draws the level's world.
        """
        screen.blit(self.bg_surf, (0, 0))
        # self.world.draw()

    def display_player(self):
        """
        A wrapper method that simply updates the player.
        """
        player.update(self.world)

    def display_objects(self):
        """
        A method that draws the level's objects.
        """
        for obj in self.world.obj_list:
            obj : Object
            obj.object_animation()

    def display_update(self):
        """
        A wrapper method that simply updates the game's display.
        """
        pygame.display.update()

    def display_score(self):
        """
        A method that displays the score in the top right corner.
        """
        score_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
        score = player.coins_collected * 10
        score_surf = score_font.render(f'Score: {score}', True, (64, 64, 64))
        score_rect = score_surf.get_rect(center = (SCREEN_WIDTH - 150, 50))
        screen.blit(score_surf, score_rect)

    def display_time(self):
        """
        A method that displays the time in the top right corner.
        """
        time_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
        time = pygame.time.get_ticks() - self.start_time
        time = (int)(time / 1000) # transform to seconds
        minutes = (int)(time / 60)
        seconds = (int)(time % 60)

        time_surf = time_font.render(f'Time: {minutes:02}:{seconds:02}', True, (64, 64, 64))
        time_rect = time_surf.get_rect(center = (SCREEN_WIDTH - 150, 100))
        screen.blit(time_surf, time_rect)

    def display_lives(self):
        """
        A method that displays the total amount of lives in the top left corner.
        """
        original_heart = pygame.image.load('../ClassicPlatformerAssets/Heart/heartanim1.png')
        heart_full = pygame.transform.scale(original_heart, (40, 40))
        heart_empty = heart_full.copy()
        heart_empty.set_alpha(150) # make the heart greyed out

        (x, y) = (30, 30)
        for i in range(3):
            if i < player.lives:
                screen.blit(heart_full, (x, y))
            else:
                screen.blit(heart_empty, (x, y))
            x += 50

    def display_ending(self):
        """
        A method that displays the ending menu on the entire screen.
        Depending on the states "fallen" and "completed", a different menu is displayed.
        """
        ending_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 45)
        score = player.coins_collected * COIN_MULTIPLIER
        time = (int)(self.ending_time / 1000) # transform to seconds
        minutes = time // 60
        seconds = time % 60
        score = score - minutes // 60 - seconds # adjust score depending on the time taken
        if score < 0:
            score = 0 # we don't accept negative scores here 

        bg_surf = pygame.image.load('../backgrounds/ending.jpg')
        bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.state == "fallen":
            ending_surf = ending_font.render(f'You have lost!', True, (64, 64, 64))

        else:
            ending_surf = ending_font.render(f'You have won!', True, (64, 64, 64))

        ending_rect = ending_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))

        score_surf = ending_font.render(f'Score: {score}', True, (64, 64, 64))
        score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        time_surf = ending_font.render(f'Time: {minutes:02}:{seconds:02}', True, (64, 64, 64))
        time_rect = time_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

        screen.blit(bg_surf, (0, 0))
        screen.blit(ending_surf, ending_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(time_surf, time_rect)

        restart_button.update()
        main_menu_button.update()
        if self.state == "completed":
            next_button.update() # only show next button when the level was won

        if restart_button.was_pressed >= 1:
            self.reset()
            self.state = "playing"

        if next_button.was_pressed >= 1:
            self.state = "next"
            self.running = False

        elif main_menu_button.was_pressed >= 1:
            self.running = False

        self.display_update()

    def display_death(self):
        """
        A method that displays the player's death image.
        Following this, the function hands over the control to display_ending.
        """
        player.death_img_index += 0.1
        if player.death_img_index >= len(player.death_img_list):
            player.death_img_index = 0
            self.state = "fallen" # after the death animation, treat the rest as the fallen case
            self.ending_time = pygame.time.get_ticks() - self.start_time
            pygame.time.delay(200) # avoid making the transition very sudden
            mixer.music.stop()
            SoundAssets.loss.play()
            return

        img_frame = player.death_img_list[int(player.death_img_index)][0] # the surface
        screen.blit(img_frame, player.player_rect)

    def display_victory(self):
        """
        A method that hands over the control to display_ending after playing a victory sound".
        Also handles highscore updating and autosaving.
        """
        self.ending_time = pygame.time.get_ticks() - self.start_time
        # update highscore if necessary
        storage.update_highscores(self.idx, player.coins_collected * COIN_MULTIPLIER, highscores)
        storage.new_save(self.idx)
        mixer.music.stop()
        SoundAssets.victory.play()
        self.state = "completed"

    def run_level(self):
        """
        A method that controls a level's outcomes and constantly updates it while playing.
        """
        self.clock.tick(FPS)

        if self.state == "playing":
            self.display_world() # layer 1
            self.display_objects() # layer 2
            self.display_player() # layer 3

            if not player.player_is_alive:
                self.state = "dead"

            else:
                self.display_score() # layer 5
                self.display_time() # layer 6
                self.display_lives() # layer 7

        if player.completed_current_level and self.state != "completed":
            self.display_victory()

        if self.state == "dead":
            # call all of these to have a fluid death animation
            self.display_world()
            self.display_objects()
            self.display_death()

        if self.state in ("completed", "fallen"):
            self.display_ending()

        self.display_update() # go back to layer 1

main_menu = Level('../backgrounds/sky.jpg', world_main_menu, 0)
