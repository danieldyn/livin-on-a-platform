import pygame
from settings import FPS, MAIN_MENU
from buttons import Button
from levels import main_menu, level1


pygame.init()

#class Game():
#        def __init__(self):
#                self.setup()
#                self.running = True
#                self.gameover = False
#                self.run()

running = True

start_button = Button(400, 400, "Start") # test coordinates (will change for final main menu)
start_button.get_img("button_images_01", 5, "png")


while running:
        level1.clock.tick(FPS)

        # for clarity 
        # def draw_grid():
        #         for line in range(0, 73):
        #                 pygame.draw.line(screen, (0, 0, 0), (0, line * block_size), (screen_width, line * block_size))
        #                 pygame.draw.line(screen, (0, 0, 0), (line * block_size, 0), (line * block_size, screen_height))
        # Keep this commented unless you want to debug the screen layout
        #draw_grid()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        if MAIN_MENU == True:
                main_menu.display_world()
                
                # will add idle player (animation) on main menu, on some surface
                # main_menu.display_player()
                start_button.update()
                if start_button.was_pressed >= 1:
                        MAIN_MENU = False
                main_menu.display_update()
        elif level1.running == True:
                level1.start_level()
        else:
                running = False

pygame.quit()
