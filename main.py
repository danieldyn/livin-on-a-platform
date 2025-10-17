import pygame
from buttons import Button
from levels import Level, main_menu
from worlds import world_level_01


pygame.init()

#class Game():
#        def __init__(self):
#                self.setup()
#                self.running = True
#                self.gameover = False
#                self.run()

start_button = Button(400, 700, "Start") # test coordinates (will change for final main menu)
start_button.get_img(1, "button_images_01", 5, "png")

# initialise before the main loop
running = True
level_list = []
current_level = None
level1 = None

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        if main_menu.running == True:
                main_menu.display_world()
                
                # will add idle player (animation) on main menu, on some surface
                # main_menu.display_player()
                start_button.update()
                if start_button.was_pressed >= 1:
                        main_menu.running = False
                        level1 = Level('backgrounds/sky.jpg', world_level_01)
                        level_list.append(level1)
                        current_level = 0
                        level1.reset()
                main_menu.display_update()

        elif level_list[current_level] and level_list[current_level].running == True:
                level_list[current_level].run_level()

        else:
                # return to main menu and reset the level attempt
                main_menu.running = True
                start_button.reset()
                level_list = []

pygame.quit()
