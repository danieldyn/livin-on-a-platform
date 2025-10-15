import pygame
from settings import screen
from settings import BUTTON_IMAGE_INCREMENT

class Button():
    def __init__(self, x, y, text_on_button):
        self.button_img_list = [] # for now all Button objects have the same "animation" 
        self.button_width = 144 # same dimensions as the unscaled picture (for now)
        self.button_height = 72
        self.button_rect = pygame.rect.Rect(x, y, self.button_width, self.button_height)
        self.can_press_button = True
        self.button_image_index = 0
        self.was_pressed = 0
        self.text_on_button = text_on_button

    def reset(self):
        self.was_pressed = 0
        self.can_press_button = 1
        self.button_image_index = 0

    def get_img(self, scale, directory, number_of_image_files, image_file_type):
        for i in range(1, number_of_image_files + 1):
            img_surf = pygame.image.load(f"buttons/{directory}/img{i:02}.{image_file_type}").convert_alpha()
            # scale
            # img_surf = pygame.transform.scale(img_surf, (self.button_width * scale, self.button_height * scale))
            # self.button_width = self.button_width * scale
            # self.button_height = self.button_height * scale
            img_mask = pygame.mask.from_surface(img_surf)
            img_rect = img_surf.get_rect()

            # add text to button 
            text_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
            text_surf = text_font.render(self.text_on_button, True, (20, 20, 20))
            text_rect = text_surf.get_rect(center=img_rect.center) # for positioning

            img_surf.blit(text_surf, text_rect)

            img = (img_surf, img_mask)
            self.button_img_list.append(img)

    def update(self):
        mouse_coordinates = (mouse_x, mouse_y) = pygame.mouse.get_pos()

        first_button_img = self.button_img_list[0][1] # the mask

        if self.button_rect.collidepoint(mouse_coordinates) and first_button_img.get_at((mouse_x - self.button_rect.x, mouse_y - self.button_rect.y)) == 1: # collision
                if pygame.mouse.get_pressed()[0] == True: # left click
                     self.can_press_button = False # can't press twice (before the animation cycle is complete)

        if self.can_press_button == False: # it is currently being pressed
            self.button_image_index += BUTTON_IMAGE_INCREMENT
            if self.button_image_index >= len(self.button_img_list):
                self.button_image_index = 0
                self.can_press_button = True # it can be pressed again
                self.was_pressed += 1
            screen.blit(self.button_img_list[int(self.button_image_index)][0], self.button_rect)
        else:
            screen.blit(self.button_img_list[0][0], self.button_rect)