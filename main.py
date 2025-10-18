import pygame
from buttons import Button
from levels import Level, main_menu
from worlds import world_level_01, empty_level
from settings import menu_sound, screen, instructions
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

pygame.init()

#class Game():
#        def __init__(self):
#                self.setup()
#                self.running = True
#                self.gameover = False
#                self.run()

menu_sound.play()

start_button = Button(300, 700, "Start") # test coordinates (will change for final main menu)
start_button.get_img(1, "button_images_01", 5, "png")

story_button = Button(500, 700, "Story")
story_button.get_img(1, "button_images_01", 5, "png")
story_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 15)
story_bg = pygame.image.load('backgrounds/story.jpg')
story_bg = pygame.transform.scale(story_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

return_button = Button(750, 670, "Return")
return_button.get_img(1, "button_images_01", 5, "png")

# initialise before the main loop
running = True
level_list = []
current_level = 0
level1 = None
story_mode = False

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        if main_menu.running == True:
                main_menu.display_world()
                
                # will add idle player (animation) on main menu, on some surface
                # main_menu.display_player()
                start_button.update()
                story_button.update()

                if story_button.was_pressed >= 1:
                        main_menu.running = False
                        story_mode = True
                
                ##
                # Warning, this doesn't work, will search for a solution
                if start_button.was_pressed >= 1:
                        main_menu.running = False
                        story_mode = False
                        menu_sound.stop()
                        level1 = Level('backgrounds/sky.jpg', world_level_01)
                        level_list.append(level1)
                        current_level = 0
                        level1.reset()
                # End of disfunctional part
                ##

                main_menu.display_update()

        if story_mode == True:
                screen.blit(story_bg, (0, 0))
                # write the paragraphs of text
                y = 140
                for line in instructions:
                        text = story_font.render(line, True, WHITE)
                        text_surf = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
                        text_surf.fill((0, 0, 0, 128)) # half transparent background
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

        elif level_list and level_list[current_level] and level_list[current_level].running == True:
                level_list[current_level].run_level()

        else:
                # return to main menu and reset the level attempt
                main_menu.running = True
                start_button.reset()
                level_list = []

pygame.quit()
