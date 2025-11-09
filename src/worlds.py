"""
A module that handles the worlds in the game.
"""
import pygame
from settings import BLOCK_SIZE, screen
import objects
import enemies

class World():
    """
    A class that implements an in-game world.
    Every world has a grid of blocks, objects, obstacles (dangerous objects) and enemies.
    """
    def __init__(self):
        self.block_list = []
        self.obj_list = []
        self.world_data = []
        self.dangerous_blocks_list = []
        self.enemy_list = []

    def get_world_data(self, file_path):
        """
        A method that completes a world's codified block grid.
        """
        with open(file_path, encoding='utf-8') as file:
            for line in file:
                self.world_data.append([c for c in line.strip()])

    def get_block_list(self, grid):
        """
        A method that populates a world's block list according to the grid.
        """
        grass_img = pygame.image.load('../ClassicPlatformerAssets/GrassBlockBuildable/grassblocksetBuildable1.png')
        dirt_img = pygame.image.load('../ClassicPlatformerAssets/GrassBlockBuildable/grassblocksetBuildable4.png')
        water_img = pygame.image.load('../ClassicPlatformerAssets/Water/water.png')
        spike_img = pygame.image.load('../ClassicPlatformerAssets/Props/spikes.png')

        row_count = 0
        for row in grid:
            col_count = 0
            for block in row:
                if block == '-':
                    # ignore block
                    # some objects are inserted into the text file as 1 block, but they occupy more space
                    # adding an ignore block lets us signal that some adjacent blocks are occupied
                    pass
                if block == '1':
                    # dirt block
                    image = pygame.transform.scale(dirt_img, (BLOCK_SIZE, BLOCK_SIZE))
                    dirt_rect = image.get_rect()
                    dirt_rect.x = BLOCK_SIZE * col_count
                    dirt_rect.y = BLOCK_SIZE * row_count
                    block_mask = pygame.mask.from_surface(image)
                    block_var = (image, dirt_rect, block_mask)
                    self.block_list.append(block_var)
                if block == '2':
                    # grass block
                    image = pygame.transform.scale(grass_img, (BLOCK_SIZE, BLOCK_SIZE))
                    grass_rect = image.get_rect()
                    grass_rect.x = BLOCK_SIZE * col_count
                    grass_rect.y = BLOCK_SIZE * row_count
                    block_mask = pygame.mask.from_surface(image)
                    block_var = (image, grass_rect, block_mask)
                    self.block_list.append(block_var)
                if block == '3':
                    # water block
                    image = pygame.transform.scale(water_img, (BLOCK_SIZE, BLOCK_SIZE))
                    water_rect = image.get_rect()
                    water_rect.x = BLOCK_SIZE * col_count
                    water_rect.y = BLOCK_SIZE * row_count
                    block_mask = pygame.mask.from_surface(image)
                    block_var = (image, water_rect, block_mask)
                    self.block_list.append(block_var)
                if block == '4':
                    # coin block
                    coin_x = BLOCK_SIZE * col_count
                    coin_y = BLOCK_SIZE * row_count
                    coin = objects.Object('../brackeys_platformer_assets/sprites/coin.png', coin_x, coin_y)
                    coin.get_obj_img(16, 16, 1, (0, 0, 0), 1, 12, coin.object_img_list)
                    self.obj_list.append(coin)
                if block == '5':
                    # spike block
                    image = pygame.transform.scale(spike_img, (BLOCK_SIZE, BLOCK_SIZE))
                    spike_rect = image.get_rect()
                    spike_rect.x = BLOCK_SIZE * col_count
                    spike_rect.y = BLOCK_SIZE * row_count
                    spike_mask = pygame.mask.from_surface(image)
                    img = (image, spike_rect, spike_mask)
                    self.dangerous_blocks_list.append(img)
                # chests will be increasingly nicer as the number is higer
                if block == '6':
                    # tier 1 chest (least nice)
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest_obj = objects.Object('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y)
                    chest_obj.get_obj_img(48, 32, 1,(0, 0, 0), 1, 5, chest_obj.object_img_list)
                    chest_obj.get_obj_img(48, 32, 1, (0, 0, 0), 2, 5, chest_obj.object_img_list)
                    chest_obj.object_can_be_collected = False # a chest cannot be collected
                    chest_obj.can_interact_with_player = True
                    self.obj_list.append(chest_obj)
                if block == '7':
                    # tier 2 chest
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest_obj = objects.Object('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y)
                    chest_obj.get_obj_img(48, 32, 1,(0, 0, 0), 3, 5, chest_obj.object_img_list)
                    chest_obj.get_obj_img(48, 32, 1, (0, 0, 0), 4, 5, chest_obj.object_img_list)
                    chest_obj.object_can_be_collected = False # a chest cannot be collected
                    chest_obj.can_interact_with_player = True
                    self.obj_list.append(chest_obj)
                if block == '8':
                    # tier 3 chest
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest_obj = objects.Object('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y)
                    chest_obj.get_obj_img(48, 32, 1,(0, 0, 0), 5, 5, chest_obj.object_img_list)
                    chest_obj.get_obj_img(48, 32, 1, (0, 0, 0), 6, 5, chest_obj.object_img_list)
                    chest_obj.object_can_be_collected = False # a chest cannot be collected
                    chest_obj.can_interact_with_player = True
                    self.obj_list.append(chest_obj)
                if block == '9':
                    # tier 4 chest (nicest)
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest_obj = objects.Object('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y)
                    chest_obj.get_obj_img(48, 32, 1,(0, 0, 0), 7, 5, chest_obj.object_img_list)
                    chest_obj.get_obj_img(48, 32, 1, (0, 0, 0), 8, 5, chest_obj.object_img_list)
                    chest_obj.object_can_be_collected = False # a chest cannot be collected
                    chest_obj.can_interact_with_player = True
                    self.obj_list.append(chest_obj)
                if block == 'a':
                    # tree
                    tree_x = BLOCK_SIZE * col_count
                    tree_y = BLOCK_SIZE * row_count
                    tree_obj = objects.Object('../ClassicPlatformerAssets/Tree/tree.png', tree_x, tree_y)
                    tree_obj.get_obj_img(48, 80, 1.2, (0, 0, 0), 1, 1, tree_obj.object_img_list)
                    tree_obj.object_can_be_collected = False # a tree cannot be collected
                    self.obj_list.append(tree_obj)
                if block == 'b':
                    # end of level flag
                    flag_x = BLOCK_SIZE * col_count
                    flag_y = BLOCK_SIZE * row_count
                    flag_obj = objects.Object('../ClassicPlatformerAssets/Checkpoint/checkpoint.png', flag_x, flag_y)
                    flag_obj.get_obj_img(48, 32, 1, (0, 0, 0), 1, 1, flag_obj.object_img_list)
                    flag_obj.object_can_be_collected = False # the end of level flag cannot be collected
                    flag_obj.can_interact_with_player = True
                    self.obj_list.append(flag_obj)
                if block == 'c':
                    # enemy (slime)
                    enemy_x = BLOCK_SIZE * col_count
                    enemy_y = BLOCK_SIZE * row_count
                    enemy = enemies.Enemy('../brackeys_platformer_assets/sprites/slime_purple.png', enemy_x, enemy_y, 20)
                    # 20 is a test value (hardcoded for now - will change later)
                    enemy.get_image(24, 24, 1.35, (0, 0, 0), 2, 4, enemy.animation_img_list)
                    # 1.35 hardcoded value (gives the impression that the slime is touching the ground)
                    self.enemy_list.append(enemy)
                col_count += 1
            row_count += 1

    def draw(self):
        """
        A method that draws a world..
        """
        for block in self.block_list:
            screen.blit(block[0], block[1])
            # Keep this commented unless you want to debug the screen layout
            # pygame.draw.rect(screen, (255, 255, 255), block[1], 1)
        for dangerous_blocks in self.dangerous_blocks_list:
            screen.blit(dangerous_blocks[0], dangerous_blocks[1])


# Keep this commented unless you want to debug the screen layout
# def draw_grid():
#         for line in range(0, 73):
#                 pygame.draw.line(screen, (0, 0, 0), (0, line * block_size), (screen_width, line * block_size))
#                 pygame.draw.line(screen, (0, 0, 0), (line * block_size, 0), (line * block_size, screen_height))
#draw_grid()

def create_world(path_to_world_data):
    """
    A method that creates a world based on the Object's methods for the grid and the blocks.
    """
    world = World() # new world
    world.get_world_data(path_to_world_data) # get data
    world.get_block_list(world.world_data) # get blocks (and objects)
    return world

# main menu
world_main_menu = create_world("../worlds/main_menu.txt")

# level worlds
world_level_01 = create_world("../worlds/world1.txt")
world_level_02 = create_world("../worlds/world2.txt")

# empty world (good for menus)
empty_level = create_world("../worlds/empty_world.txt")
