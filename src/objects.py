"""
A module that handles the objects in the game.
"""
import pygame
from settings import screen, OBJECT_IMAGE_INCREMENT

class Object():
    """
    A class that implements an object.
    An object is anything that can be collected or interacted with.
    Interactable ones have an animation only available when the player gives input
    """
    def __init__(self, path_to_sheet, x, y): # x, y -> placement
        self.object_sheet = pygame.image.load(path_to_sheet)
        self.object_img_list = []
        self.object_shown = True
        self.object_can_be_collected = True
        self.can_interact_with_player = False
        self.player_is_interacting_with_object = False
        self.sound_was_played = False
        self.object_img_index = 0
        self.obj_width = 16
        self.obj_height = 16
        self.obj_rect = pygame.rect.Rect(x, y, self.obj_width, self.obj_height)

    def get_obj_img(self, width, height, scale, color, row_number, number_of_images, list_of_images):
        """
        A method that completes an object's image list.
        """
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
        """
        A method that plays an object's image.
        If the object cannot interact with the player, then the animation can be played in a loop.
        Else, wait for player input.
        """
        if not self.can_interact_with_player:
            if self.object_shown:
                self.object_img_index += OBJECT_IMAGE_INCREMENT
                if self.object_img_index >= len(self.object_img_list):
                    self.object_img_index = 0
                obj_surface = self.object_img_list[int(self.object_img_index)][0]
                screen.blit(obj_surface, self.obj_rect)
        else:
            if not self.player_is_interacting_with_object:
                screen.blit(self.object_img_list[0][0], self.obj_rect)
            else:
                self.object_img_index += OBJECT_IMAGE_INCREMENT
                if self.object_img_index >= len(self.object_img_list):
                    self.object_img_index = 0
                    self.player_is_interacting_with_object = False
                obj_surface = self.object_img_list[int(self.object_img_index)][0]
                screen.blit(obj_surface, self.obj_rect)
