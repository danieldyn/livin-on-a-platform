"""
A module that handles the objects in the game.
"""
import pygame
from abc import ABC, abstractmethod
from sounds import SoundAssets
from typing import override
from settings import screen, OBJECT_IMAGE_INCREMENT

class Object(ABC):
    """
    A class that implements an object.
    An object is anything that can be collected or interacted with.
    Interactable ones have an animation only available when the player gives input.
    """
    def __init__(self, path_to_sheet, x, y): # x, y -> placement
        self.object_sheet = pygame.image.load(path_to_sheet)
        self.object_img_list = []
        self.object_img_index = 0 
        self.object_is_usable = True
        self.obj_width = 16 
        self.obj_height = 16 
        self.obj_rect = pygame.rect.Rect(x, y, self.obj_width, self.obj_height)

    def get_object_image(self, width, height, scale, color, row_number, number_of_images, list_of_images):
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

    @abstractmethod
    def object_animation(self):
        """
        A method that plays an object's image.
        If the object cannot interact with the player, then the animation can be played in a loop.
        Else, wait for player input.
        """
        pass

class InteractableObject(Object, SoundAssets):
    def __init__(self, path_to_sheet, x, y, value, numeber_of_interactions):
        super().__init__(path_to_sheet, x, y)
        self.value = value
        self.sound = None
        self.number_of_interactions = numeber_of_interactions

    def object_animation(self):
        if not self.object_is_usable and self.number_of_interactions > 0: # if object is not usable, then it is being used
            self.object_img_index += OBJECT_IMAGE_INCREMENT
            if self.object_img_index >= len(self.object_img_list):
                self.object_img_index = 0
                # after an interaction, the number of available interactions is decreased
                self.number_of_interactions -= 1
                self.object_is_usable = True
            obj_surface = self.object_img_list[int(self.object_img_index)][0]
            screen.blit(obj_surface, self.obj_rect)
        elif self.number_of_interactions == 0:
            last = len(self.object_img_list) - 1
            screen.blit(self.object_img_list[last][0], self.obj_rect)
        else:
            screen.blit(self.object_img_list[0][0], self.obj_rect)
        
class CollectableObject(Object, SoundAssets):
    def __init__(self, path_to_sheet, x, y, value):
        super().__init__(path_to_sheet, x, y)
        self.sound = None
        self.value = value
    
    def object_animation(self):
        if self.object_is_usable:
            self.object_img_index += OBJECT_IMAGE_INCREMENT
            if self.object_img_index >= len(self.object_img_list):
                self.object_img_index = 0
            obj_surface = self.object_img_list[int(self.object_img_index)][0]
            screen.blit(obj_surface, self.obj_rect)
        else:
            pass

class DangerousObject(Object, SoundAssets): # could also split this in 2 (Movable vs Imovable)
        def __init__(self, path_to_sheet, x, y):
            super().__init__(path_to_sheet, x, y)
        def object_animation(self):
            # by default a dangerous object imoveable
            self.object_img_index += OBJECT_IMAGE_INCREMENT
            if self.object_img_index >= len(self.object_img_list):
                self.object_img_index = 0
            obj_surface = self.object_img_list[int(self.object_img_index)][0]
            screen.blit(obj_surface, self.obj_rect)    

class DecorationObject(Object): 
    def __init__(self, path_to_sheet, x, y):
        super().__init__(path_to_sheet, x, y)
    
    def object_animation(self):
        self.object_img_index += OBJECT_IMAGE_INCREMENT
        if self.object_img_index >= len(self.object_img_list):
            self.object_img_index = 0
        obj_surface = self.object_img_list[int(self.object_img_index)][0]
        screen.blit(obj_surface, self.obj_rect)

class Coin(CollectableObject):
    def __init__(self, path_to_sheet, x, y, value):
        super().__init__(path_to_sheet, x, y, value)
        self.sound = SoundAssets.coin

class Chest(InteractableObject):
    def __init__(self, path_to_sheet, x, y, value, numeber_of_interactions=1):
        super().__init__(path_to_sheet, x, y, value, numeber_of_interactions)
        self.sound = SoundAssets.chest
    
class EndOfLevelObject(InteractableObject):
    def __init__(self, path_to_sheet, x, y, value, numeber_of_interactions=1):
        super().__init__(path_to_sheet, x, y, value, numeber_of_interactions)
        self.sound = SoundAssets.victory

class Slime(DangerousObject):  
    def __init__(self, path_to_sheet, x, y, dx):
        super().__init__(path_to_sheet, x, y)
        self.slime_width = 64
        self.slime_height = 64
        self.slime_movement_range = (x - dx, x + dx)
        self.direction = 1
    
    @override
    def object_animation(self):
        """
        A method that runs a slime's animation.
        Slimes can move left and right on their designated platform.
        """
        self.object_img_index += 0.1
        if self.object_img_index >= len(self.object_img_list):
            self.object_img_index = 0

        img_surface = self.object_img_list[int(self.object_img_index)][0]

        self.obj_rect.x += 1 * self.direction

        if self.obj_rect.x >= self.slime_movement_range[1]:
            self.direction = -1
        if self.obj_rect.x <= self.slime_movement_range[0]:
            self.direction = 1

        if self.direction == -1: # going left
            img_surface = pygame.transform.flip(img_surface, True, False).convert_alpha()

        screen.blit(img_surface, self.obj_rect)

class Spike(DangerousObject):
    def __init__(self, path_to_sheet, x, y):
        super().__init__(path_to_sheet, x, y)

class Tree(DecorationObject):
    def __init__(self, path_to_sheet, x, y):
        super().__init__(path_to_sheet, x, y)

# class Heart(Object) -> similar to coin (value = 0 / will add health_value)