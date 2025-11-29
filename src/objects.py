"""
A module that handles the objects in the game.
"""
from abc import ABC, abstractmethod
import pygame
from sounds import SoundAssets
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
        self.sound : SoundAssets = None
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

class InteractableObject(Object, SoundAssets):
    """
    A class that implements an object that the player can interact with using Enter.
    The parameter value refers to the equivalent in Coins. Can support multiple interactions.
    """
    def __init__(self, path_to_sheet, x, y, value, number_of_interactions):
        super().__init__(path_to_sheet, x, y)
        self.value = value
        self.sound = None
        self.number_of_interactions = number_of_interactions

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
    """
    A class that implements an object that the player can collect by direct collision.
    The parameter value refers to the equivalent in Coins.
    """
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

class DangerousObject(Object, SoundAssets):
    """
    A class that implements an object that will hurt the player upon collision.
    Unless specified via constructor parameter dx, the object will be immovable.
    """
    def __init__(self, path_to_sheet, x, y, dx=0):
        super().__init__(path_to_sheet, x, y)
        self.object_movement_range = (x - dx, x + dx)
        self.dx = dx
        self.direction = 1
    def object_animation(self):
        self.object_img_index += OBJECT_IMAGE_INCREMENT
        if self.object_img_index >= len(self.object_img_list):
            self.object_img_index = 0

        obj_surface = self.object_img_list[int(self.object_img_index)][0]

        if self.dx == 0:
            # default mode -> imovable
            screen.blit(obj_surface, self.obj_rect)
        else:
            # specific mode -> movable
            self.obj_rect.x += 1 * self.direction
            if self.obj_rect.x >= self.object_movement_range[1]:
                self.direction = -1
            if self.obj_rect.x <= self.object_movement_range[0]:
                self.direction = 1
            if self.direction == -1: # going left
                obj_surface = pygame.transform.flip(obj_surface, True, False).convert_alpha()
            screen.blit(obj_surface, self.obj_rect)

class StaticObject(Object): # it cannot be moved or crossed (i.e. block)
    """
    A class that implements an object that cannot be moved or crossed.
    Player collisions with these objects will not be tested.
    """
    def __init__(self, path_to_sheet, x, y):
        super().__init__(path_to_sheet, x, y)

    def object_animation(self):
        self.object_img_index += OBJECT_IMAGE_INCREMENT
        if self.object_img_index >= len(self.object_img_list):
            self.object_img_index = 0
        obj_surface = self.object_img_list[int(self.object_img_index)][0]
        screen.blit(obj_surface, self.obj_rect)

class DecorationObject(StaticObject):
    """
    A class that implements a static object that is purely decorational.
    """
    def __init__(self, path_to_sheet, x, y):
        super().__init__(path_to_sheet, x, y)

class EndOfLevelObject(InteractableObject):
    """
    A class that implements the end-of-level Flag.
    The player needs to interact with it using Enter to finish the current level.
    """
    def __init__(self, path_to_sheet, x, y, value, numeber_of_interactions=1):
        super().__init__(path_to_sheet, x, y, value, numeber_of_interactions)
        self.sound = SoundAssets.victory

class Coin(CollectableObject):
    """
    A class that implements a coin, worth 1 Coin in the game's economy.
    """
    def __init__(self, path_to_sheet, x, y, value):
        super().__init__(path_to_sheet, x, y, value)
        self.sound = SoundAssets.coin

class Chest(InteractableObject):
    """
    A class that implements a chest.
    It has a variable equivalent in Coins, depending on how nice it looks.
    """
    def __init__(self, path_to_sheet, x, y, value, numeber_of_interactions=1):
        super().__init__(path_to_sheet, x, y, value, numeber_of_interactions)
        self.sound = SoundAssets.chest

class Acorn(InteractableObject):
    def __init__(self, path_to_sheet, x, y, value, numeber_of_interactions=1):
        super().__init__(path_to_sheet, x, y, value, numeber_of_interactions)
        self.sound = None
        


class Slime(DangerousObject):
    """
    A class that implements a slime enemy.
    It's a mobile object that patrols around its own platform by default.
    """
    def __init__(self, path_to_sheet, x, y, dx=5):
        super().__init__(path_to_sheet, x, y, dx)
        self.slime_width = 64
        self.slime_height = 64
        self.sound = SoundAssets.hit

class Spike(DangerousObject, SoundAssets):
    """
    A class that implements a spike obstacle.
    It's an immovable object placed on platforms by default.
    """
    def __init__(self, path_to_sheet, x, y, dx=0):
        super().__init__(path_to_sheet, x, y, dx)
        self.sound = SoundAssets.hurt

class Heart(CollectableObject):
    """
    A class that implement a heart.
    Collecting it will increase the player's maximum lives, if any are missing.
    """
    def __init__(self, path_to_sheet, x, y, value):
        super().__init__(path_to_sheet, x, y, value)
        self.sound = SoundAssets.heart
