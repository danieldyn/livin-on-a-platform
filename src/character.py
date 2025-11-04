"""
A module that handles the game's character (player).
"""

import pygame
from settings import BLOCK_SIZE, SCREEN_HEIGHT, ROLLING_IMAGE_INCREMENT, RUNNING_IMAGE_INCREMENT, IDLE_IMAGE_INCREMENT
from settings import screen, coin_sound, hit_sound, chest_sound

class Player():
    """
    A class that implements the player.
    """
    def __init__(self, x, y):
        # basic parameters
        self.starting_x = x
        self.starting_y = y
        self.player_gravity = -15
        self.player_width = 48
        self.player_height = 48
        # index for animation
        self.running_img_index = 0
        self.idle_img_index = 0
        self.rolling_img_index = 0
        self.death_img_index = 0
        # image lists
        self.running_img_list = []
        self.rolling_img_list = []
        self.idle_image_list = []
        self.death_img_list = []
        # relevant in-game aspects
        self.img = pygame.image.load('../brackeys_platformer_assets/sprites/knight.png').convert_alpha()
        self.player_rect = pygame.rect.Rect(self.starting_x, self.starting_y, self.player_width, self.player_height)
        self.can_jump = True
        self.player_is_rolling = False
        self.coins_collected = 0
        self.jump_sound = pygame.mixer.Sound('../brackeys_platformer_assets/sounds/jump.wav')
        self.player_is_alive = True
        self.completed_current_level = False

    def reset(self):
        """
        A method that resets a player's state.
        Usually, this will be called when restarting a level.
        """
        self.player_rect.topleft = (self.starting_x, self.starting_y)
        self.coins_collected = 0
        self.completed_current_level = False

    def get_img(self, sheet, width, height, color, row_number, number_of_images, list_of_images):
        """
        A method that completes a player's image list.
        """
        for i in range(0, number_of_images):
            # animation images
            img = pygame.surface.Surface((width, height)).convert_alpha()
            img.blit(sheet, (0, 0), (width * i, (row_number - 1) * height, width * (i + 1), row_number * height))
            img = pygame.transform.scale(img, (self.player_width, self.player_height))
            img.set_colorkey(color)
            player_mask = pygame.mask.from_surface(img) # mask for better collision
            img_rect = img.get_rect()
            image = (img, img_rect, player_mask)
            list_of_images.append(image)

    def update(self, level_world):
        """
        A method that updates the player's state.
        Usually, this will be called while running a level.
        """
        # movement
        dx = 0
        dy = self.player_gravity

        self.player_gravity += 1
        self.player_gravity = min(self.player_gravity, 10)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if keys[pygame.K_DOWN]:
                self.rolling_img_index += ROLLING_IMAGE_INCREMENT
                self.player_is_rolling = True
            else:
                self.player_is_rolling = False
                self.rolling_img_index = 0 # reset for next roll
                self.running_img_index += RUNNING_IMAGE_INCREMENT
            dx += 5

        if keys[pygame.K_LEFT]:
            if keys[pygame.K_DOWN]:
                self.rolling_img_index += ROLLING_IMAGE_INCREMENT
                self.player_is_rolling = True
            else:
                self.player_is_rolling = False
                self.rolling_img_index = 0 # reset for next roll
                self.running_img_index += RUNNING_IMAGE_INCREMENT
            dx -= 5

        if keys[pygame.K_SPACE]:
            if self.can_jump:
                self.jump_sound.play()
                self.player_gravity = -15
                dy = self.player_gravity
                self.can_jump = False # prevent button mashing and multi jumps

        if int(self.running_img_index) >= len(self.running_img_list):
            self.running_img_index = 0

        if int(self.rolling_img_index) >= len(self.rolling_img_list):
            self.rolling_img_index = 0

        img_mask = self.running_img_list[int(self.running_img_index)][2] # the mask of the player

        # collision

        for block in level_world.block_list:
            block_rect = block[1] # the rect of the block
            block_mask = block[2] # the mask of the block

            is_corner = False

            # going horizontally
            if img_mask.overlap(block_mask, (block_rect.x - (self.player_rect.x + dx), block_rect.y - self.player_rect.y)):
                dx = 0
                is_corner = True
            # going vertically
            if img_mask.overlap(block_mask, (block_rect.x - self.player_rect.x, block_rect.y - (self.player_rect.y + dy))):
                if is_corner:
                    if self.can_jump: # this fixes top corners
                        self.player_rect.bottom = block_rect.top
                    else: # this fixes bottom corners (still a bit glitchy, but it doesn't get stuck anymore)
                        self.player_rect.top = block_rect.bottom

                if self.player_gravity > 0: # landing on the ground
                    dy = 0
                    self.player_gravity = 0
                    self.can_jump = True # jumping should be allowed whilst on the ground

                elif self.player_gravity < 0: # hitting the ceiling
                    dy = 0
                    self.player_gravity = 0

        # print(level_world.dangerous_blocks_list)

        for danger_block in level_world.dangerous_blocks_list:
            danger_block_rect = danger_block[1]
            danger_block_mask : pygame.Mask = danger_block[2]

            # hitting the block
            if img_mask.overlap(danger_block_mask, (danger_block_rect.x - self.player_rect.x, block_rect.y - (self.player_rect.y + dy))) or img_mask.overlap(danger_block_mask, (danger_block_rect.x - (self.player_rect.x + dx), danger_block_rect.y - self.player_rect.y)):
                hit_sound.play()
                self.player_is_alive = False

        for enemy in level_world.enemy_list:
            for img in enemy.animation_img_list:
                enemy_mask = img[1]
                if img_mask.overlap(enemy_mask, (enemy.enemy_rect.x - self.player_rect.x, enemy.enemy_rect.y - self.player_rect.y)):
                    self.player_is_alive = False

        if self.player_is_alive:
            # checking if player is idle
            img_frame = pygame.surface.Surface((0, 0))

            if dx == 0 and dy == 0:
                self.running_img_index = 0 # start running animation from beginning after idle state
                self.idle_img_index += IDLE_IMAGE_INCREMENT

                if self.idle_img_index >= len(self.idle_image_list):
                    self.idle_img_index = 0

                img_frame = self.idle_image_list[int(self.idle_img_index)][0] # the surface

            else:
                if self.player_is_rolling:
                    img_frame = self.rolling_img_list[int(self.rolling_img_index)][0] # the surface
                else:
                    img_frame = self.running_img_list[int(self.running_img_index)][0] # the surface

                if dx < 0: # moving left
                    img_frame = pygame.transform.flip(img_frame, True, False).convert_alpha()

                self.player_rect.y += dy
                self.player_rect.x += dx

            # check if player is on screen (after possible movement)
            if player.player_rect.y >= SCREEN_HEIGHT:
                player.player_is_alive = False
            else:
                player.player_is_alive = True

            # Keep this commented unless you want to debug the player's hitbox range
            #pygame.draw.rect(screen, (255, 255, 255), self.player_rect, 3) # for clarity

            # check if the player "collected" an object

            for obj in level_world.obj_list:
                for img in obj.object_img_list:
                    obj_mask = img[2]
                    # print((self.player_rect.x, self.player_rect.y))
                    if img_mask.overlap(obj_mask, (obj.obj_rect.x - self.player_rect.x, obj.obj_rect.y - self.player_rect.y)):
                        if obj.object_can_be_collected:
                            if obj.object_shown:
                                coin_sound.play()
                                self.coins_collected += 1 # avoid point farming after collecting the coin
                            obj.object_shown = False # remove the object from screen

                        elif obj.can_interact_with_player:
                            # interaction will happen when ENTER is pressed
                            if keys[pygame.K_RETURN]:
                                chest_sound.play()
                                obj.player_is_interacting_with_object = True
                                if len(obj.object_img_list) == 1: # check if the object is the end level flag
                                    self.completed_current_level = True

            screen.blit(img_frame, self.player_rect)
        else:
            pass

# player
player = Player(7 * BLOCK_SIZE, SCREEN_HEIGHT - 7 * BLOCK_SIZE)
# getting running images
player.get_img(player.img, 32, 32, (0, 0, 0), 3, 8, player.running_img_list)
# getting rolling images
player.get_img(player.img, 32, 32, (0, 0, 0), 6, 8, player.rolling_img_list)
# getting idle images
player.get_img(player.img, 32, 32, (0, 0, 0), 1, 4, player.idle_image_list)
# death animation
player.get_img(player.img, 32, 32, (0, 0, 0), 8, 4, player.death_img_list)
