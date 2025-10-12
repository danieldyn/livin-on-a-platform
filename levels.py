import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LOSS_SCREEN_DURATION,  screen, loss_sound, mixer
from character import player
from objects import obj_list
from worlds import world_main_menu, world_level_01


class Level():
        def __init__(self, bg_img, world):
                self.running = True
                # background
                bg_surf = pygame.image.load(bg_img)
                self.bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                # world map
                self.world = world
                # timer start
                self.clock = pygame.time.Clock()
                # player info
                self.player_is_alive = False

        # once there is a main menu
        #def go_to_main_menu(self):

        def display_world(self):
                screen.blit(self.bg_surf, (0, 0))
                self.world.draw()

        def display_player(self):
                player.update()
                if player.player_rect.y >= SCREEN_HEIGHT:
                        self.player_is_alive = False
                else:
                        self.player_is_alive = True
        
        def display_objects(self):
                for obj in obj_list:
                        obj.obj_animation()

        def display_score(self):
                score_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
                score = player.coins_collected * 10
                score_surf = score_font.render(f'Score: {score}', True, (64, 64, 64))
                score_rect = score_surf.get_rect(center = (SCREEN_WIDTH - 150, 50))
                screen.blit(score_surf, score_rect)

        def display_time(self):
                time_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
                time = pygame.time.get_ticks()
                time = (int)(time / 1000) # transform to seconds
                minutes = (int)(time / 60)
                seconds = (int)(time % 60)
        
                if seconds < 10:
                        time_surf = time_font.render(f'Time: 0{minutes}:0{seconds}', True, (64, 64, 64))
                elif seconds < 60:
                        time_surf = time_font.render(f'Time: 0{minutes}:{seconds}', True, (64, 64, 64))
                time_rect = time_surf.get_rect(center = (SCREEN_WIDTH - 150, 100))
                screen.blit(time_surf, time_rect)

        def display_fallen(self, time):
                pygame.time.delay(250) # avoid making the transition very sudden
                bg_surf = pygame.image.load('backgrounds/fallen_menu.jpg')
                bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(bg_surf, (0, 0))

                fallen_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 45)
                score = player.coins_collected * 10
                time = (int)(time / 1000) # transform to seconds
                minutes = (int)(time / 60)
                seconds = (int)(time % 60)

                fallen_surf = fallen_font.render(f'You have fallen!', True, (64, 64, 64))
                fallen_rect = fallen_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60)) # determined by successive tries

                score_surf = fallen_font.render(f'Score: {score}', True, (64, 64, 64))
                score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

                if seconds < 10:
                        time_surf = fallen_font.render(f'Time: 0{minutes}:0{seconds}', True, (64, 64, 64))
                elif seconds < 60:
                        time_surf = fallen_font.render(f'Time: 0{minutes}:{seconds}', True, (64, 64, 64))
                time_rect = time_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

                #restart_button = Button(400, 400, "Try Again")
                #restart_button.get_img(1, "button_images_01", 5, "png") 

                screen.blit(fallen_surf, fallen_rect)
                screen.blit(score_surf, score_rect)
                screen.blit(time_surf, time_rect)

                pygame.display.update()

                # stop background music
                mixer.music.unload()

                # play loss music
                loss_sound.play()

                # delayed exit
                pygame.time.delay(LOSS_SCREEN_DURATION)

                # quit level
                self.running = False

        def display_update(self):
                pygame.display.update()

        def start_level(self):
                self.display_world() # layer 1
                self.display_objects() # layer 2
                # layer 3 (player layer)
                self.display_player()
                if self.player_is_alive == False: # if player is dead
                        self.display_fallen(pygame.time.get_ticks())
                else: 
                        self.display_score() # layer 4
                        self.display_time() # layer 5
                        self.display_update() # go back to layer 1

        def start_main_menu(self):
                pass # couldn't figure it out, yet
        

main_menu = Level('backgrounds/sky.jpg', world_main_menu)
level1 = Level('backgrounds/sky.jpg', world_level_01)