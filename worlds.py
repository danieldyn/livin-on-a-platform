# Everything about the worlds in the game

import pygame
from settings import BLOCK_SIZE, screen
import objects

class World():
        def __init__(self):
                # every world has an object list and block list
                self.block_list = []
                self.obj_list = []

                self.world_data = []

        def get_world_data(self, file_path):
                with open(file_path) as file:
                        for line in file:
                                self.world_data.append([int(c) for c in line.strip()])

        def get_block_list(self, grid):
                grass_img = pygame.image.load('ClassicPlatformerAssets/GrassBlockBuildable/grassblocksetBuildable1.png')
                dirt_img = pygame.image.load('ClassicPlatformerAssets/GrassBlockBuildable/grassblocksetBuildable4.png')
                water_img = pygame.image.load('ClassicPlatformerAssets/Water/water.png')

                row_count = 0
                for row in grid:
                        col_count = 0
                        for block in row:
                                if block == 1:
                                        # dirt block
                                        image = pygame.transform.scale(dirt_img, (BLOCK_SIZE, BLOCK_SIZE))
                                        dirt_rect = image.get_rect()
                                        dirt_rect.x = BLOCK_SIZE * col_count
                                        dirt_rect.y = BLOCK_SIZE * row_count
                                        block_mask = pygame.mask.from_surface(image)
                                        block_var = (image, dirt_rect, block_mask)
                                        self.block_list.append(block_var)
                                if block == 2:
                                        # grass block
                                        image = pygame.transform.scale(grass_img, (BLOCK_SIZE, BLOCK_SIZE))
                                        grass_rect = image.get_rect()
                                        grass_rect.x = BLOCK_SIZE * col_count
                                        grass_rect.y = BLOCK_SIZE * row_count
                                        block_mask = pygame.mask.from_surface(image)
                                        block_var = (image, grass_rect, block_mask)
                                        self.block_list.append(block_var)
                                if block == 3:
                                        # water block
                                        image = pygame.transform.scale(water_img, (BLOCK_SIZE, BLOCK_SIZE))
                                        water_rect = image.get_rect()
                                        water_rect.x = BLOCK_SIZE * col_count
                                        water_rect.y = BLOCK_SIZE * row_count
                                        block_mask = pygame.mask.from_surface(image)
                                        block_var = (image, water_rect, block_mask)
                                        self.block_list.append(block_var)
                                if block == 4:
                                        # coin block
                                        coin_x = BLOCK_SIZE * col_count
                                        coin_y = BLOCK_SIZE * row_count
                                        coin = objects.Object('brackeys_platformer_assets/sprites/coin.png', coin_x, coin_y)
                                        coin.get_obj_img(16, 16, (0, 0, 0), 1, 12, coin.object_img_list)
                                        self.obj_list.append(coin)
                                col_count += 1
                        row_count += 1

        def draw(self):
                for block in self.block_list:
                        screen.blit(block[0], block[1])
                        # Keep this commented unless you want to debug the screen layout
                        # pygame.draw.rect(screen, (255, 255, 255), block[1], 1)

# Keep this commented unless you want to debug the screen layout
        # def draw_grid():
        #         for line in range(0, 73):
        #                 pygame.draw.line(screen, (0, 0, 0), (0, line * block_size), (screen_width, line * block_size))
        #                 pygame.draw.line(screen, (0, 0, 0), (line * block_size, 0), (line * block_size, screen_height))
        #draw_grid()

def create_world(path_to_world_data):
        world = World() # new world
        world.get_world_data(path_to_world_data) # get data
        world.get_block_list(world.world_data) # get blocks (and objects)
        return world

# main menu
world_main_menu = create_world("worlds/main_menu.txt")

# level 01
world_level_01 = create_world("worlds/world1.txt")