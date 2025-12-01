"""
Usage:
    With the cursor, hover over a block
Then press:
    -> 'e' to the next block in the list
    -> 'w' to delete to current block (and start over in the list)
    -> 'q' to go to the previous block in the list
"""

import sys
import os.path

if len(sys.argv) != 2:
    print("The command must be: python " + sys.argv[0] + " path-to-file")
    exit()

if not os.path.isfile(sys.argv[1]):
    print("Invalid path to file!")
    exit()

file_name = sys.argv[1]

import pygame
from settings import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE
from objects import Coin, Chest, DecorationObject, EndOfLevelObject, Slime, Spike, StaticObject, Heart, Acorn, Object

pygame.init()

run = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60

list_block_char = ['0', '1', 'g', 'h', 'i', 'j', 'k', '2', '3', '4', '5', 'd', 'e', 'f', 'b', 'c', '6', '7', '8', '9', 'a', 's']

class WorldEditor():
        def __init__(self, grid):
                self.obj_list = []

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
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/GrassBlockBuildable/grassblocksetBuildable4.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == '2':
                            # grass block
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/GrassBlockBuildable/grassblocksetBuildable1.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == '3':
                            # water block
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = DecorationObject('../assets/Water/water.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == '4':
                            # coin
                            coin_x = BLOCK_SIZE * col_count
                            coin_y = BLOCK_SIZE * row_count
                            # (filepath, x, y, value) -> coin = Coin() -> super()
                            coin = Coin('../assets/sprites/coin.png', coin_x, coin_y, 1)
                            coin.get_object_image(16, 16, 1, (0, 0, 0), 1, 12, coin.object_img_list)
                            self.obj_list.append(coin)
                        if block == '5':
                            # spike block
                            spike_x = BLOCK_SIZE * col_count
                            skipe_y = BLOCK_SIZE * row_count
                            spike = Spike('../assets/Props/spikes.png', spike_x, skipe_y)
                            spike.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, spike.object_img_list)
                            self.obj_list.append(spike)
                        # chests will be increasingly more valuable as the number is higer
                        if block == '6':
                            # tier 1 chest (least nice)
                            chest_x = BLOCK_SIZE * col_count
                            chest_y = BLOCK_SIZE * row_count
                            chest = Chest('../assets/sprites/chests.png', chest_x, chest_y, 2)
                            chest.get_object_image(48, 32, 1, (0, 0, 0), 1, 5, chest.object_img_list)
                            chest.get_object_image(48, 32, 1, (0, 0, 0), 2, 5, chest.object_img_list)
                            self.obj_list.append(chest)
                        if block == '7':
                            # tier 2 chest
                            chest_x = BLOCK_SIZE * col_count
                            chest_y = BLOCK_SIZE * row_count
                            chest = Chest('../assets/sprites/chests.png', chest_x, chest_y, 2)
                            chest.get_object_image(48, 32, 1,(0, 0, 0), 3, 5, chest.object_img_list)
                            chest.get_object_image(48, 32, 1, (0, 0, 0), 4, 5, chest.object_img_list)
                            self.obj_list.append(chest)
                        if block == '8':
                            # tier 3 chest
                            chest_x = BLOCK_SIZE * col_count
                            chest_y = BLOCK_SIZE * row_count
                            chest = Chest('../assets/sprites/chests.png', chest_x, chest_y, 2)
                            chest.get_object_image(48, 32, 1,(0, 0, 0), 5, 5, chest.object_img_list)
                            chest.get_object_image(48, 32, 1, (0, 0, 0), 6, 5, chest.object_img_list)
                            self.obj_list.append(chest)
                        if block == '9':
                            # tier 4 chest (nicest)
                            chest_x = BLOCK_SIZE * col_count
                            chest_y = BLOCK_SIZE * row_count
                            chest = Chest('../assets/sprites/chests.png', chest_x, chest_y, 2)
                            chest.get_object_image(48, 32, 1,(0, 0, 0), 7, 5, chest.object_img_list)
                            chest.get_object_image(48, 32, 1, (0, 0, 0), 8, 5, chest.object_img_list)
                            self.obj_list.append(chest)
                        if block == 'a':
                            # tree
                            tree_x = BLOCK_SIZE * col_count
                            tree_y = BLOCK_SIZE * row_count
                            tree = DecorationObject('../assets/Tree/tree.png', tree_x, tree_y)
                            tree.get_object_image(48, 80, 1.2, (0, 0, 0), 1, 1, tree.object_img_list)
                            self.obj_list.append(tree)
                        if block == 'b':
                            # end of level flag
                            flag_x = BLOCK_SIZE * col_count
                            flag_y = BLOCK_SIZE * row_count
                            flag = EndOfLevelObject('../assets/Checkpoint/checkpoint.png', flag_x, flag_y, 0)
                            flag.get_object_image(48, 32, 1, (0, 0, 0), 1, 1, flag.object_img_list)
                            self.obj_list.append(flag)
                        if block == 'c':
                            # enemy (slime)
                            slime_x = BLOCK_SIZE * col_count
                            slime_y = BLOCK_SIZE * row_count
                            slime = Slime('../assets/sprites/slime_purple.png', slime_x, slime_y, 20)
                            # 20 is a test value (hardcoded for now - will change later)
                            slime.get_object_image(24, 24, 1.35, (0, 0, 0), 2, 4, slime.object_img_list)
                            # 1.35 hardcoded value (gives the impression that the slime is touching the ground)
                            self.obj_list.append(slime)
                        if block == 'd':
                            # heart
                            heart_x = BLOCK_SIZE * col_count
                            heart_y = BLOCK_SIZE * row_count
                            heart = Heart('../assets/Heart/heartanim1.png', heart_x, heart_y, 0)
                            heart.get_object_image(16, 16, 1.2, (0, 0, 0), 1, 1, heart.object_img_list)
                            self.obj_list.append(heart)
                        if block == 'e':
                            # mushroom
                            shroom_x = BLOCK_SIZE * col_count
                            shroom_y = BLOCK_SIZE * row_count
                            shroom = DecorationObject('../assets/Props/shroom.png', shroom_x, shroom_y)
                            shroom.get_object_image(32, 32, 1, (0, 0, 0), 1, 1, shroom.object_img_list)
                            self.obj_list.append(shroom)
                        if block == 'f':
                            # flower
                            flower_x = BLOCK_SIZE * col_count
                            flower_y = BLOCK_SIZE * row_count
                            flower = DecorationObject('../assets/Props/flower.png', flower_x, flower_y)
                            flower.get_object_image(32, 32, 1.2, (0, 0, 0), 1, 1, flower.object_img_list)
                            self.obj_list.append(flower)
                        if block == 'g':
                            # underground tile 1
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/tiles/underground1.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == 'h':
                            # underground tile 2
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/tiles/underground2.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == 'i':
                            # stone block
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/tiles/stone.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == 'j':
                            # cobblestone tile 2
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/tiles/cobblestone1.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == 'k':
                            # cobblestone tile 2
                            block_x = BLOCK_SIZE * col_count
                            block_y = BLOCK_SIZE * row_count
                            block = StaticObject('../assets/tiles/cobblestone2.png', block_x, block_y)
                            block.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, block.object_img_list)
                            self.obj_list.append(block)
                        if block == 's':
                            acorn_x = BLOCK_SIZE * col_count
                            acorn_y = BLOCK_SIZE * row_count
                            acorn = Acorn('../assets/acorns/acorn_iocla.png', acorn_x, acorn_y, 10)
                            acorn.get_object_image(312, 293, 0.6, (255, 255, 255), 1, 1, acorn.object_img_list)
                            self.obj_list.append(acorn)
                        col_count += 1
                    row_count += 1

        def draw(self):
                for obj in self.obj_list:
                    obj : Object
                    obj.object_animation()
                    # pygame.draw.rect(screen, (255, 255, 255), block[1], 1) # for clarity


                
# for clarity 
def draw_grid():
        for line in range(0, 73):
            pygame.draw.line(screen, (0, 0, 0), (0, line * BLOCK_SIZE), (SCREEN_WIDTH, line * BLOCK_SIZE))
            pygame.draw.line(screen, (0, 0, 0), (line * BLOCK_SIZE, 0), (line * BLOCK_SIZE, SCREEN_HEIGHT))


world1_data = []

with open(file_name) as file:
        for line in file:
                world1_data.append([c for c in line.strip()])

world_data_index = []
for row in world1_data:
    block_type_row = []
    for block_char in row:
        if block_char in list_block_char:
            block_type_row.append(list_block_char.index(block_char))
        else:
            block_type_row.append(0)
    world_data_index.append(block_type_row)

# background
sky_surf = pygame.image.load('../assets/backgrounds/sky.jpg')
sky_surf = pygame.transform.scale(sky_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))

while run:
        clock.tick(FPS)
        world1 = WorldEditor(world1_data)

        screen.blit(sky_surf, (0, 0))

        draw_grid()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_e]: # press e
                        (mouseX, mouseY) = pygame.mouse.get_pos()
                        mouseX //= BLOCK_SIZE
                        mouseY //= BLOCK_SIZE
                        world_data_index[mouseY][mouseX] += 1
                        world_data_index[mouseY][mouseX] %= len(list_block_char)
                        world1_data[mouseY][mouseX] = list_block_char[world_data_index[mouseY][mouseX]]
                    if keys[pygame.K_q]: # press w
                        (mouseX, mouseY) = pygame.mouse.get_pos()
                        mouseX //= BLOCK_SIZE
                        mouseY //= BLOCK_SIZE
                        world_data_index[mouseY][mouseX] -= 1
                        if world_data_index[mouseY][mouseX] < 0:
                             world_data_index[mouseY][mouseX] = len(list_block_char) - 1
                        world1_data[mouseY][mouseX] = list_block_char[world_data_index[mouseY][mouseX]]
                    if keys[pygame.K_w]: # press q
                        (mouseX, mouseY) = pygame.mouse.get_pos()
                        mouseX //= BLOCK_SIZE
                        mouseY //= BLOCK_SIZE
                        world_data_index[mouseY][mouseX] = 0
                        world1_data[mouseY][mouseX] = list_block_char[world_data_index[mouseY][mouseX]]

        world1.draw()
        
        pygame.display.update()

with open(file_name, "w") as file:
    for row in world1_data:
        line_string = "".join(row)
        
        file.write(line_string + "\n")

pygame.quit()
        