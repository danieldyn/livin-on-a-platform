# Everything about the objects (an object is anything that can be "collected" or interacted with)

import pygame
from settings import screen, OBJECT_IMAGE_INCREMENT

class Object():
    def __init__(self, path_to_sheet, x, y): # x, y -> placement
        self.object_sheet = pygame.image.load(path_to_sheet)
        self.object_img_list = []
        self.object_shown = True
        self.object_can_be_collected = True # some objects (e.g., chests) cannot be collected
        self.can_interact_with_player = False # some objects (e.g., chests) can interact with the player (meaning they have an animation ONLY available when player gives input)
        self.player_is_interacting_with_object = False
        self.sound_was_played = False
        self.object_img_index = 0
        self.obj_width = 16
        self.obj_height = 16
        self.obj_rect = pygame.rect.Rect(x, y, self.obj_width, self.obj_height)
        
    def get_obj_img(self, width, height, scale, color, row_number, number_of_images, list_of_images):
        for i in range(0, number_of_images):
            obj_img = pygame.surface.Surface((width, height)).convert_alpha()
            obj_img.blit(self.object_sheet, (0, 0), (i * width, (row_number - 1) * height, (i + 1) * width, row_number * height))
            obj_img = pygame.transform.scale(obj_img, (scale * width, scale * height))
            obj_img.set_colorkey(color)
            obj_rect = obj_img.get_rect()
            obj_mask = pygame.mask.from_surface(obj_img)
            obj = (obj_img, obj_rect, obj_mask)
            list_of_images.append(obj)
        
    def obj_animation(self):
        if self.can_interact_with_player == False: # if object cannot interact with player, then the animation can be played in a loop
            if self.object_shown == True:
                self.object_img_index += OBJECT_IMAGE_INCREMENT
                if self.object_img_index >= len(self.object_img_list):
                    self.object_img_index = 0
                obj_surface = self.object_img_list[int(self.object_img_index)][0]
                screen.blit(obj_surface, self.obj_rect)
        else: # if object can interact with player, then wait for player input
            if self.player_is_interacting_with_object == False:
                screen.blit(self.object_img_list[0][0], self.obj_rect)
            else:
                self.object_img_index += OBJECT_IMAGE_INCREMENT
                if self.object_img_index >= len(self.object_img_list):
                    self.object_img_index = 0
                    self.player_is_interacting_with_object = False
                obj_surface = self.object_img_list[int(self.object_img_index)][0]
                screen.blit(obj_surface, self.obj_rect)