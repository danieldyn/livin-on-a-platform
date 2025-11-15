"""
A module that handles the worlds in the game.
"""
import pygame
from settings import BLOCK_SIZE, screen
from objects import Coin, Chest, Tree, EndOfLevelObject, Slime, Spike

class World():
    """
    A class that implements an in-game world.
    Every world has a grid of blocks, objects, obstacles (dangerous objects) and enemies.
    """
    def __init__(self, file_path):
        self.block_list = []
        self.obj_list = []
        self.world_data = []
        self.file_path = file_path

    def get_world_data(self):
        """
        A method that completes a world's codified block grid.
        """
        with open(self.file_path, encoding='utf-8') as file:
            for line in file:
                self.world_data.append([c for c in line.strip()])

    def get_block_list(self, grid):
        """
        A method that populates a world's block list according to the grid.
        """
        grass_img = pygame.image.load('../ClassicPlatformerAssets/GrassBlockBuildable/grassblocksetBuildable1.png')
        dirt_img = pygame.image.load('../ClassicPlatformerAssets/GrassBlockBuildable/grassblocksetBuildable4.png')
        water_img = pygame.image.load('../ClassicPlatformerAssets/Water/water.png')

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
                    # coin
                    coin_x = BLOCK_SIZE * col_count
                    coin_y = BLOCK_SIZE * row_count
                    # (filepath, x, y, value) -> coin = Coin() -> super()
                    coin = Coin('../brackeys_platformer_assets/sprites/coin.png', coin_x, coin_y, 1)
                    coin.get_object_image(16, 16, 1, (0, 0, 0), 1, 12, coin.object_img_list)
                    self.obj_list.append(coin)
                if block == '5':
                    # spike block
                    spike_x = BLOCK_SIZE * col_count
                    skipe_y = BLOCK_SIZE * row_count
                    spike = Spike('../ClassicPlatformerAssets/Props/spikes.png', spike_x, skipe_y)
                    spike.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, spike.object_img_list)
                    self.obj_list.append(spike)
                # chests will be increasingly more valuable as the number is higer
                if block == '6':
                    # tier 1 chest (least nice)
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest = Chest('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y, 2, 2)
                    chest.get_object_image(48, 32, 1, (0, 0, 0), 1, 5, chest.object_img_list)
                    chest.get_object_image(48, 32, 1, (0, 0, 0), 2, 5, chest.object_img_list)
                    self.obj_list.append(chest)
                if block == '7':
                    # tier 2 chest
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest = Chest('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y, 2, 10)
                    chest.get_object_image(48, 32, 1,(0, 0, 0), 3, 5, chest.object_img_list)
                    chest.get_object_image(48, 32, 1, (0, 0, 0), 4, 5, chest.object_img_list)
                    self.obj_list.append(chest)
                if block == '8':
                    # tier 3 chest
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest = Chest('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y, 2)
                    chest.get_object_image(48, 32, 1,(0, 0, 0), 5, 5, chest.object_img_list)
                    chest.get_object_image(48, 32, 1, (0, 0, 0), 6, 5, chest.object_img_list)
                    self.obj_list.append(chest)
                if block == '9':
                    # tier 4 chest (nicest)
                    chest_x = BLOCK_SIZE * col_count
                    chest_y = BLOCK_SIZE * row_count
                    chest = Chest('../brackeys_platformer_assets/sprites/chests.png', chest_x, chest_y, 2)
                    chest.get_object_image(48, 32, 1,(0, 0, 0), 7, 5, chest.object_img_list)
                    chest.get_object_image(48, 32, 1, (0, 0, 0), 8, 5, chest.object_img_list)
                    self.obj_list.append(chest)
                if block == 'a':
                    # tree
                    tree_x = BLOCK_SIZE * col_count
                    tree_y = BLOCK_SIZE * row_count
                    tree = Tree('../ClassicPlatformerAssets/Tree/tree.png', tree_x, tree_y)
                    tree.get_object_image(48, 80, 1.2, (0, 0, 0), 1, 1, tree.object_img_list)
                    self.obj_list.append(tree)
                if block == 'b':
                    # end of level flag
                    flag_x = BLOCK_SIZE * col_count
                    flag_y = BLOCK_SIZE * row_count
                    flag = EndOfLevelObject('../ClassicPlatformerAssets/Checkpoint/checkpoint.png', flag_x, flag_y, 0)
                    flag.get_object_image(48, 32, 1, (0, 0, 0), 1, 1, flag.object_img_list)
                    self.obj_list.append(flag)
                if block == 'c':
                    # enemy (slime)
                    slime_x = BLOCK_SIZE * col_count
                    slime_y = BLOCK_SIZE * row_count
                    slime = Slime('../brackeys_platformer_assets/sprites/slime_purple.png', slime_x, slime_y, 20)
                    # 20 is a test value (hardcoded for now - will change later)
                    slime.get_object_image(24, 24, 1.35, (0, 0, 0), 2, 4, slime.object_img_list)
                    # 1.35 hardcoded value (gives the impression that the slime is touching the ground)
                    self.obj_list.append(slime)
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
    world = World(path_to_world_data) # new world
    world.get_world_data() # get data
    world.get_block_list(world.world_data) # get blocks (and objects)
    return world

def reset_world(path_to_world_data):
    """
    A method that creates a world based on the Object's methods for the grid and the blocks.
    """
    world = World(path_to_world_data) # new world
    world.get_world_data() # get data
    world.get_block_list(world.world_data) # get blocks (and objects)
    return world

# main menu
world_main_menu = create_world("../worlds/main_menu.txt")

# level worlds
world_level_01 = create_world("../worlds/world1.txt")
world_level_02 = create_world("../worlds/world2.txt")

# empty world (good for menus)
empty_level = create_world("../worlds/empty_world.txt")
