import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COIN_MULTIPLIER
from settings import screen, loss_sound, victory_sound, mixer
from character import player
from worlds import world_main_menu
from buttons import Button

restart_button = Button(400, 600, "Retry")
restart_button.get_img(1, "button_images_01", 5, "png")

main_menu_button = Button(600, 600, "Quit")
main_menu_button.get_img(1, "button_images_01", 5, "png")

class Level():
        def __init__(self, bg_img, world):
                self.running = True
                bg_surf = pygame.image.load(bg_img)
                self.bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.world = world
                self.clock = pygame.time.Clock()
                self.start_time = pygame.time.get_ticks()
                self.state = "playing"
                self.ending_time = 0
                self.fallen_buttons = False
                self.main_menu_button = None
                self.restart_button = None

        def reset(self):
                self.start_time = pygame.time.get_ticks()
                self.state = "playing"
                player.player_is_alive = True
                player.reset()
                mixer.music.rewind()
                mixer.music.play()
                restart_button.was_pressed = 0
                main_menu_button.was_pressed = 0
                for obj in self.world.obj_list:
                        obj.object_shown = True

        def display_world(self):
                screen.blit(self.bg_surf, (0, 0))
                self.world.draw()

        def display_player(self):
                player.update(self.world)
        
        def display_objects(self):
                for obj in self.world.obj_list:
                        obj.obj_animation()
        
        def display_update(self):
                pygame.display.update()

        def display_score(self):
                score_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
                score = player.coins_collected * 10
                score_surf = score_font.render(f'Score: {score}', True, (64, 64, 64))
                score_rect = score_surf.get_rect(center = (SCREEN_WIDTH - 150, 50))
                screen.blit(score_surf, score_rect)

        def display_time(self):
                time_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 25)
                time = pygame.time.get_ticks() - self.start_time
                time = (int)(time / 1000) # transform to seconds
                minutes = (int)(time / 60)
                seconds = (int)(time % 60)

                time_surf = time_font.render(f'Time: {minutes:02}:{seconds:02}', True, (64, 64, 64))
                time_rect = time_surf.get_rect(center = (SCREEN_WIDTH - 150, 100))
                screen.blit(time_surf, time_rect)

        def display_ending(self):
                ending_font = pygame.font.Font('brackeys_platformer_assets/fonts/PixelOperator8-Bold.ttf', 45)
                score = player.coins_collected * COIN_MULTIPLIER
                time = (int)(self.ending_time / 1000) # transform to seconds
                minutes = time // 60
                seconds = time % 60

                bg_surf = pygame.image.load('backgrounds/fallen_menu.jpg')
                bg_surf = pygame.transform.scale(bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
                if self.state == "fallen":
                        ending_surf = ending_font.render(f'You have lost!', True, (64, 64, 64))
                elif self.state == "completed":
                        ending_surf = ending_font.render(f'You have won!', True, (64, 64, 64))
                fallen_rect = ending_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
                
                score_surf = ending_font.render(f'Score: {score}', True, (64, 64, 64))
                score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                
                time_surf = ending_font.render(f'Time: {minutes:02}:{seconds:02}', True, (64, 64, 64))
                time_rect = time_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

                screen.blit(bg_surf, (0, 0))
                screen.blit(ending_surf, fallen_rect)
                screen.blit(score_surf, score_rect)
                screen.blit(time_surf, time_rect)

                restart_button.update()
                main_menu_button.update()

                if restart_button.was_pressed >= 1:
                        self.reset()
                        self.state = "playing"
                        
                elif main_menu_button.was_pressed >= 1:
                        self.running = False
                
                self.display_update()
        
        def display_death(self):
                player.death_img_index += 0.1
                if player.death_img_index >= len(player.death_img_list):
                        player.death_img_index = 0
                        self.state = "fallen" # after the death amnimation, treat the rest as the fallen case
                        self.ending_time = pygame.time.get_ticks() - self.start_time
                        pygame.time.delay(200) # avoid making the transition very sudden  
                        mixer.music.stop()
                        loss_sound.play()
                        return
                
                img_frame = player.death_img_list[int(player.death_img_index)][0] # the surface
                screen.blit(img_frame, player.player_rect)
        
        def display_victory(self):
                self.ending_time = pygame.time.get_ticks() - self.start_time
                pygame.time.delay(100) # avoid making the transition very sudden
                mixer.music.stop()
                victory_sound.play()

        def run_level(self):
                self.clock.tick(FPS)

                if self.state == "playing":
                        self.display_world() # layer 1
                        self.display_objects() # layer 2
                        self.display_player() # layer 3

                        if player.player_is_alive == False:
                                self.state = "dead"
                        else:
                                self.display_score() # layer 4
                                self.display_time() # layer 5

                if player.completed_current_level == True and self.state != "completed":
                        self.state = "completed"
                        self.display_victory()

                if self.state == "dead":
                        # call all of these to have a fluid death animation
                        self.display_world()
                        self.display_objects()
                        self.display_death()

                if self.state == "completed" or self.state == "fallen":
                        self.display_ending()
                             
                self.display_update() # go back to layer 1

main_menu = Level('backgrounds/sky.jpg', world_main_menu)
