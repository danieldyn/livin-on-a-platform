"""
A module that handles the game's character (player).
"""

import pygame
from settings import BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from settings import ROLLING_IMAGE_INCREMENT, RUNNING_IMAGE_INCREMENT, IDLE_IMAGE_INCREMENT
from settings import screen
from objects import Object, CollectableObject, InteractableObject, DangerousObject, StaticObject, DecorationObject, Acorn
from objects import Coin, Heart, EndOfLevelObject
from sounds import SoundAssets

class Player(SoundAssets):
    """
    A class that implements the player.
    """
    def __init__(self, x, y):
        # basic parameters
        self.starting_x = x
        self.starting_y = y
        # player physics
        self.velocity_y = 0.0
        self.gravity_strength = 0.85 # the higher it is, the less floaty it feels
        self.jump_force = -13.0 # the lower it is, the snappier it feels
        self.max_fall_speed = 12.0 # cap falling speed
        # visuals
        self.player_width = 48
        self.player_height = 48
        self.visual_sink_y = 6 # helps keep the feet of the character on the ground, visually speaking
        # hitbox (what the player actually seees, influenced by transparent pixels)
        self.hitbox_width = 18 # sprite width is approx 20 px
        self.hitbox_height = 30 # sprite height is approx 30px
        # offsets to center the image on the hitbox, adjusted by vertical correction factor
        self.draw_offset_x = (self.player_width - self.hitbox_width) // 2
        self.draw_offset_y = (self.player_height - self.hitbox_height) - self.visual_sink_y
        # image lists
        self.running_img_list = []
        self.rolling_img_list = []
        self.idle_image_list = []
        self.death_img_list = []       
        # index for animation
        self.running_img_index = 0
        self.idle_img_index = 0
        self.rolling_img_index = 0
        self.death_img_index = 0
        # relevant in-game aspects
        self.img = pygame.image.load('../assets/sprites/knight.png').convert_alpha()
        self.player_rect = pygame.rect.Rect(self.starting_x, self.starting_y, self.hitbox_width, self.hitbox_height)
        self.can_jump = True
        self.player_is_rolling = False
        self.coins_collected = 0
        self.jump_sound = pygame.mixer.Sound('../assets/sounds/jump.wav')
        self.lives = 3
        self.last_hit_time = 0
        self.hit_cooldown = 1500 # miliseconds
        self.player_is_alive = True
        self.completed_current_level = False
        self.dx = 0
        self.dy = 0
        self.touched_acorn = False
        # animations
        self.get_img(self.img, 32, 32, (0, 0, 0), 3, 8, self.running_img_list)
        self.get_img(self.img, 32, 32, (0, 0, 0), 6, 8, self.rolling_img_list)
        self.get_img(self.img, 32, 32, (0, 0, 0), 1, 4, self.idle_image_list)
        self.get_img(self.img, 32, 32, (0, 0, 0), 8, 4, self.death_img_list)

    def update(self, level_world, can_move = True):
        """
        A method that updates player physics and rendering.
        """
        # apply gravity
        self.dx = 0

        self.velocity_y += self.gravity_strength
        self.velocity_y = min(self.velocity_y, self.max_fall_speed)
        self.dy = int(self.velocity_y)

        # movement input capturing
        keys = pygame.key.get_pressed()
        if can_move:    
            self.get_movement_input(keys) 

        # animation index updates
        if int(self.running_img_index) >= len(self.running_img_list):
            self.running_img_index = 0

        if int(self.rolling_img_index) >= len(self.rolling_img_list):
            self.rolling_img_index = 0
        
        # horizontal collisions and movement
        self.player_rect.x += self.dx
        for obj in level_world.obj_list:
            if isinstance(obj, StaticObject) and not isinstance(obj, DecorationObject):
                if self.player_rect.colliderect(obj.obj_rect):
                    if self.dx > 0: # going right
                        self.player_rect.right = obj.obj_rect.left
                    elif self.dx < 0: # going left
                        self.player_rect.left = obj.obj_rect.right
                    self.dx = 0

        # vertical collisions and movement
        self.player_rect.y += self.dy
        for obj in level_world.obj_list:
            if isinstance(obj, StaticObject) and not isinstance(obj, DecorationObject):
                if self.player_rect.colliderect(obj.obj_rect):
                    if self.dy > 0: # landing on the ground
                        self.player_rect.bottom = obj.obj_rect.top
                        self.velocity_y = 0
                        self.dy = 0
                        self.can_jump = True
                    elif self.dy < 0: # hitting the ceiling
                        self.player_rect.top = obj.obj_rect.bottom
                        self.velocity_y = 0 
                        self.dy = 0

        # hitbox debugging, keep commented
        #pygame.draw.rect(screen, (255, 255, 255), self.player_rect, 3) # for clarity

        # object interaction
        self.handle_interactions(level_world, keys)

        # image rendering
        if self.player_is_alive:
            self.render_image()

    def render_image(self):
        """
        A method that renders the player's image according to current state: 
        idle, jumping, rolling, dying, hit by enemies or obstacles.
        The drawn image is affected by the offsets determined by __init__().
        """
        img_frame = pygame.surface.Surface((0, 0))

        if self.dx == 0 and self.dy == 0 and self.can_jump:
            self.running_img_index = 0
            self.idle_img_index += IDLE_IMAGE_INCREMENT
            if self.idle_img_index >= len(self.idle_image_list):
                self.idle_img_index = 0
            img_frame = self.idle_image_list[int(self.idle_img_index)][0]
        else:
            if self.player_is_rolling:
                img_frame = self.rolling_img_list[int(self.rolling_img_index)][0]
            else:
                img_frame = self.running_img_list[int(self.running_img_index)][0]

            if self.dx < 0: # flip the image, making the player "turn"
                img_frame = pygame.transform.flip(img_frame, True, False).convert_alpha()

        # compute actual draw coordinated by subtracting the offsets
        draw_pos_x = self.player_rect.x - self.draw_offset_x
        draw_pos_y = self.player_rect.y - self.draw_offset_y

        # decide whether the image is normal or flickering after a hit
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < self.hit_cooldown:
            if (current_time // 200) % 2 == 0:
                screen.blit(img_frame, (draw_pos_x, draw_pos_y))
        else:
            screen.blit(img_frame, (draw_pos_x, draw_pos_y))

        # death by falling out of the map
        if self.player_rect.y >= SCREEN_HEIGHT:
            self.lives = 0
            self.player_is_alive = False
        else:
            self.player_is_alive = True

    def get_movement_input(self, keys):
        """
        A method that captures user input related to movement and updates self.dx and self.dy accordingly.
        Input for object interactions is taken care by handle_interactions().
        """
        if keys[pygame.K_RIGHT]:
            if keys[pygame.K_DOWN]:
                self.rolling_img_index += ROLLING_IMAGE_INCREMENT
                self.player_is_rolling = True
            else:
                self.player_is_rolling = False
                self.rolling_img_index = 0
                self.running_img_index += RUNNING_IMAGE_INCREMENT
            self.dx += 5

        if keys[pygame.K_LEFT]:
            if keys[pygame.K_DOWN]:
                self.rolling_img_index += ROLLING_IMAGE_INCREMENT
                self.player_is_rolling = True
            else:
                self.player_is_rolling = False
                self.rolling_img_index = 0
                self.running_img_index += RUNNING_IMAGE_INCREMENT
            self.dx -= 5

        if keys[pygame.K_SPACE]:
            if self.can_jump:
                self.jump_sound.play()
                self.velocity_y = self.jump_force
                self.dy = int(self.velocity_y)
                self.can_jump = False

    def handle_interactions(self, level_world, keys):
        """
        A method that handles interactions with all objects in the given level world.
        Also takes care of interpreting player input for these interactions.
        """
        img_mask = self.running_img_list[int(self.running_img_index)][2] # the mask of the player
        # check player interaction with objects
        for obj in level_world.obj_list:
            # blocks already covered
            if isinstance(obj, StaticObject): 
                continue
            # mask collision for items and obstacles
            for img in obj.object_img_list:
                obj_mask = img[2]
                # compute relative distance between the dangerous object and the visual image of the player
                offset_x = obj.obj_rect.x - (self.player_rect.x - self.draw_offset_x)
                offset_y = obj.obj_rect.y - (self.player_rect.y - self.draw_offset_y)
                if img_mask.overlap(obj_mask, (offset_x, offset_y)):
                    # overlapping with an object
                    if isinstance(obj, CollectableObject):
                        if obj.object_is_usable:
                            obj.sound.play()
                            if isinstance(obj, Coin):
                                self.coins_collected += 1 # avoid point farming after collecting the coin
                            elif isinstance(obj, Heart) and self.lives < 3:
                                self.lives += 1
                        obj.object_is_usable = False # remove object from screen

                    elif isinstance(obj, InteractableObject):
                        # interaction will happen when ENTER is pressed
                        if keys[pygame.K_RETURN]:
                            if obj.object_is_usable and obj.number_of_interactions > 0: # you can try using it
                                obj.object_is_usable = False
                                if obj.sound is not None:
                                    obj.sound.play()
                                if isinstance(obj, EndOfLevelObject): # end of level flag
                                    self.completed_current_level = True
                                elif isinstance(obj, Acorn):
                                    self.touched_acorn = True
                                else: # it is a chest containing a fixed amount of coins
                                    self.coins_collected += obj.value

                    elif isinstance(obj, DangerousObject):
                        current_time = pygame.time.get_ticks()
                        # check if the player is not in the invulnerable window
                        if current_time - self.last_hit_time > self.hit_cooldown:
                            if obj.sound is not None:
                                obj.sound.play()
                            self.lives -= 1
                            self.last_hit_time = current_time # timer reset
                            if self.lives <= 0:
                                self.player_is_alive = False

    def reset(self):
        """
        A method that resets a player's state.
        Usually, this will be called when restarting a level.
        """
        self.player_rect.topleft = (self.starting_x, self.starting_y)
        self.coins_collected = 0
        if self.lives == 0: # make sure it isn't used for level transition
            self.lives = 3
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
