"""
A module that handles the enemies in the game.
"""
import pygame
from settings import screen

class Enemy():
    """
    A class that implements an enemy.
    Colliding with one will reduce the player's number of hearts.
    """
    def __init__(self, path_to_sheet, x, y, dx):
        self.enemy_sheet = pygame.image.load(path_to_sheet)
        self.enemy_width = 64
        self.enemy_height = 64
        self.enemy_rect = pygame.rect.Rect(x, y, self.enemy_width, self.enemy_height)
        self.animation_img_list = [] # every enemy will have a predetermined path and animation
        self.enemy_img_index = 0
        self.enemy_movement_range = (x - dx, x + dx)
        self.direction = 1

    def get_image(self, width, height, scale, color, row_number, number_of_images, list_of_images):
        """
        A method that completes an enemy's image list.
        """
        for i in range(0, number_of_images):
            enemy_img = pygame.surface.Surface((width, height)).convert_alpha()
            enemy_img.blit(self.enemy_sheet, (0, 0), (i * width, (row_number - 1) * height, (i + 1) * width, row_number * height))
            enemy_img = pygame.transform.scale(enemy_img, (scale * width, scale * height))
            enemy_img.set_colorkey(color)
            enemy_mask = pygame.mask.from_surface(enemy_img)
            enemy = (enemy_img, enemy_mask)
            list_of_images.append(enemy)

    def enemy_animation(self):
        """
        A method that runs an enemy's animation.
        Enemies can move left and right on their designated platform.
        """
        self.enemy_img_index += 0.1
        if self.enemy_img_index >= len(self.animation_img_list):
            self.enemy_img_index = 0

        img_surface = self.animation_img_list[int(self.enemy_img_index)][0]

        self.enemy_rect.x += 1 * self.direction

        if self.enemy_rect.x >= self.enemy_movement_range[1]:
            self.direction = -1
        if self.enemy_rect.x <= self.enemy_movement_range[0]:
            self.direction = 1

        if self.direction == -1: # going left
            img_surface = pygame.transform.flip(img_surface, True, False).convert_alpha()

        screen.blit(img_surface, self.enemy_rect)
