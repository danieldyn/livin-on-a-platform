"""
A module that handles the worlds in the game.
"""
from settings import BLOCK_SIZE, screen
from objects import Coin, Chest, DecorationObject, EndOfLevelObject, Slime, Spike, StaticObject, Heart, Acorn

class World():
    """
    A class that implements an in-game world.
    Every world has a map of static objects and a list of dynamic ones.
    """
    def __init__(self, file_path):
        self.block_list = []
        self.tile_map = {} # map for fast queries on static blocks
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
        A method that populates a world's block map according to the grid (a matrix of characters).
        """

        row_count = 0
        for row in grid:
            col_count = 0
            for block in row:
                # current coordinates
                x = BLOCK_SIZE * col_count
                y = BLOCK_SIZE * row_count

                # static objects go in the map
                if block in ['1', '2', 'g', 'h', 'i', 'j', 'k']:
                    img_path = ''
                    if block == '1':
                        img_path = '../assets/GrassBlockBuildable/grassblocksetBuildable4.png'

                    elif block == '2':
                        img_path = '../assets/GrassBlockBuildable/grassblocksetBuildable1.png'

                    elif block == 'g':
                        img_path = '../assets/tiles/underground1.png'

                    elif block == 'h':
                        img_path = '../assets/tiles/underground2.png'

                    elif block == 'i':
                        img_path = '../assets/tiles/stone.png'

                    elif block == 'j':
                        img_path = '../assets/tiles/cobblestone1.png'

                    elif block == 'k':
                        img_path = '../assets/tiles/cobblestone2.png'

                    # all static objects are instantiated the same
                    static_obj = StaticObject(img_path, x, y)
                    static_obj.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, static_obj.object_img_list)
                    self.tile_map[(col_count, row_count)] = static_obj
                # everything else belongs in the list
                else:
                    new_obj = None

                    if block == '-':
                        # ignore block
                        # some objects are inserted into the text file as 1 block, but they occupy more space
                        # adding an ignore block lets us signal that some adjacent blocks are occupied
                        pass

                    if block == '3': # water
                        new_obj = DecorationObject('../assets/Water/water.png', x, y)
                        new_obj.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, new_obj.object_img_list)
                    
                    elif block == '4': # coin
                        # (filepath, x, y, value) -> coin = Coin() -> super()
                        new_obj = Coin('../assets/sprites/coin.png', x, y, 1)
                        new_obj.get_object_image(16, 16, 1, (0, 0, 0), 1, 12, new_obj.object_img_list)

                    elif block == '5': # spike
                        new_obj = Spike('../assets/Props/spikes.png', x, y)
                        new_obj.get_object_image(16, 16, 1, (0, 0, 0), 1, 1, new_obj.object_img_list)
                    
                    elif block == '6': # tier 1 chest, will be increasingly more valuable as the number is higher
                        new_obj = Chest('../assets/sprites/chests.png', x, y, 2)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 1, 5, new_obj.object_img_list)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 2, 5, new_obj.object_img_list)

                    elif block == '7': # tier 2 chest
                        new_obj = Chest('../assets/sprites/chests.png', x, y, 4)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 3, 5, new_obj.object_img_list)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 4, 5, new_obj.object_img_list)

                    elif block == '8': # tier 3 chest
                        new_obj = Chest('../assets/sprites/chests.png', x, y, 6)
                        new_obj.get_object_image(48, 32, 1,(0, 0, 0), 5, 5, new_obj.object_img_list)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 6, 5, new_obj.object_img_list)
                    
                    elif block == '9': # tier 4 chest
                        new_obj = Chest('../assets/sprites/chests.png', x, y, 10)
                        new_obj.get_object_image(48, 32, 1,(0, 0, 0), 7, 5, new_obj.object_img_list)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 8, 5, new_obj.object_img_list)
                    
                    elif block == 'a': # tree
                        new_obj = DecorationObject('../assets/Tree/tree.png', x, y)
                        new_obj.get_object_image(48, 80, 1.2, (0, 0, 0), 1, 1, new_obj.object_img_list)
                    
                    elif block == 'b': # end of level flag
                        new_obj = EndOfLevelObject('../assets/Checkpoint/checkpoint.png', x, y, 0)
                        new_obj.get_object_image(48, 32, 1, (0, 0, 0), 1, 1, new_obj.object_img_list)

                    elif block == 'c': # slime
                        new_obj = Slime('../assets/sprites/slime_purple.png', x, y, 20)
                        # 20 is a test value (hardcoded for now - will change later)
                        new_obj.get_object_image(24, 24, 1.35, (0, 0, 0), 2, 4, new_obj.object_img_list)
                        # 1.35 hardcoded value (gives the impression that the slime is touching the ground)

                    elif block == 'd': # heart
                        new_obj = Heart('../assets/Heart/heartanim1.png', x, y, 0)
                        new_obj.get_object_image(16, 16, 1.2, (0, 0, 0), 1, 1, new_obj.object_img_list)

                    elif block == 'e': # mushroom
                        new_obj = DecorationObject('../assets/Props/shroom.png', x, y)
                        new_obj.get_object_image(32, 32, 1, (0, 0, 0), 1, 1, new_obj.object_img_list)
                    
                    elif block == 'f': # flower
                        new_obj = DecorationObject('../assets/Props/flower.png', x, y)
                        new_obj.get_object_image(32, 32, 1.2, (0, 0, 0), 1, 1, new_obj.object_img_list)

                    elif block == 's': # acorn
                        new_obj = Acorn('../assets/acorns/acorn_iocla.png', x, y, 10)
                        new_obj.get_object_image(312, 293, 0.6, (255, 255, 255), 1, 1, new_obj.object_img_list)

                    # add to list if we created one
                    if new_obj:
                        self.obj_list.append(new_obj)

                col_count += 1
            row_count += 1

        # create a list for drawing purposes only
        self.draw_list = list(self.tile_map.values()) + self.obj_list

    def draw(self):
        """
        A method that draws a world.
        """
        for block in self.draw_list:
            screen.blit(block[0], block[1])
            # Keep this commented unless you want to debug the screen layout
            # pygame.draw.rect(screen, (255, 255, 255), block[1], 1)

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
