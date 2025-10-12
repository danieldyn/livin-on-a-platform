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

start_button = Button(400, 400, "Start") # test coordinates (will change for final main menu)
start_button.get_img("button_images_01", 5, "png")

running = True
level1 = None # initialise before loop

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
                        level1.reset()
                main_menu.display_update()

        elif level1 and level1.running == True:
                level1.run_level()

        else:
                # return to main menu and reset the level attempt
                main_menu.running = True
                start_button.reset()
                level1 = None

pygame.quit()
