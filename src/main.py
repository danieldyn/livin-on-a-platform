"""
Main entry point for the platformer game.
Initialises Pygame, handles menu logic and level transitions.
"""
import pygame
from buttons import Button
from levels import Level, main_menu
from worlds import world_level_01, world_level_02
from settings import screen, instructions, story, play_hint, story_hint, help_hint
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from sounds import SoundAssets

pygame.init()

SoundAssets.menu_music.play()

start_button = Button(300, 600, "Start")
start_button.get_img("button_images_01", 5, "png")

story_button = Button(643, 600, "Story")
story_button.get_img("button_images_01", 5, "png")

help_button = Button(472, 600, "Help")
help_button.get_img("button_images_01", 5, "png")

text_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8.ttf', 20)
alt_bg = pygame.image.load('../backgrounds/story.jpg')
alt_bg = pygame.transform.scale(alt_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

return_button = Button(750, 673, "Back")
return_button.get_img("button_images_01", 5, "png")

# initialise before the main loop
running = True
level_list = []
level_idx = 0
level1 = None
story_mode = False
help_mode = False
world_sequence = [
    ("../backgrounds/sky.jpg", world_level_01, 1),
    ("../backgrounds/sky.jpg", world_level_02, 2)
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if main_menu.running:
        main_menu.display_world()

        # will add idle player (animation) on main menu, on some surface
        # main_menu.display_player()

        # display buttons and hints
        y = 500
        for line in play_hint:
            text = text_font.render(line, True, BLACK)
            screen.blit(text, (80, y))
            y = y + 25
        y = 475
        for line in help_hint:
            text = text_font.render(line, True, BLACK)
            screen.blit(text, (440, y))
            y = y + 25
        y = 500
        for line in story_hint:
            text = text_font.render(line, True, BLACK)
            screen.blit(text, (800, y))
            y = y + 25

        start_button.update()
        help_button.update()
        story_button.update()

        if help_button.was_pressed >= 1:
            main_menu.running = False
            help_mode = True

        if story_button.was_pressed >= 1:
            main_menu.running = False
            story_mode = True

        if start_button.was_pressed >= 1:
            main_menu.running = False
            story_mode = False
            SoundAssets.menu_music.stop()
            # initialise all levels in advance
            level_list = [Level(bg, world, idx) for bg, world, idx in world_sequence]
            level_idx = 0
            level_list[level_idx].reset()

        main_menu.display_update()

    elif help_mode:
        screen.blit(alt_bg, (0, 0))
        # write the paragraphs of text
        y = 140
        for line in instructions:
            text = text_font.render(line, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (200, y))
            screen.blit(text, (200, y))
            y = y + 40

        return_button.update()

        if return_button.was_pressed >= 1:
            help_mode = False
            main_menu.running = True
            return_button.reset()
            help_button.reset()
            start_button.reset()
            level_list = []

        pygame.display.update()

    elif story_mode:
        screen.blit(alt_bg, (0, 0))
        # write the paragraphs of text
        y = 140
        for line in story:
            text = text_font.render(line, True, WHITE)
            text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            text_surf.fill((0, 0, 0, 158)) # partially transparent background
            screen.blit(text_surf, (200, y))
            screen.blit(text, (200, y))
            y = y + 40

        return_button.update()

        if return_button.was_pressed >= 1:
            story_mode = False
            main_menu.running = True
            return_button.reset()
            story_button.reset()
            start_button.reset()
            level_list = []

        pygame.display.update()

    elif level_list:
        current_level = level_list[level_idx]
        if current_level.running:
            current_level.run_level()
        else:
            # the level ended (W or L)
            if current_level.state == "next" and level_idx + 1 < len(level_list):
                # move to the next level
                level_idx += 1
                level_list[level_idx].reset()
            else:
                if level_idx + 1 >= len(level_list):
                    ending_font = pygame.font.Font('../brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 45)
                    bg_surf = pygame.image.load('../backgrounds/ending.jpg')
                    bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    ending_surf = ending_font.render(f'You have finished the game!', True, (64, 64, 64))
                    ending_rect = ending_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
                    screen.blit(bg_surf, (0, 0))
                    screen.blit(ending_surf, ending_rect)
                    pygame.display.update()
                    pygame.time.delay(3000) # stay on the victory screen for 3 seconds
                # return to main menu and reset the level list
                main_menu.running = True
                SoundAssets.menu_music.play()
                start_button.reset()
                level_list = []

pygame.quit()
