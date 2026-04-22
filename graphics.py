import math

import pygame
from constants import *

class Graphics:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("Arial", 24)
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.sun_img = pygame.image.load("img/sun.png").convert_alpha()
        self.moon_img = pygame.image.load("img/moon.png").convert_alpha()

        # scale base images once
        self.sun_img = pygame.transform.smoothscale(self.sun_img, (200, 200))
        self.moon_img = pygame.transform.smoothscale(self.moon_img, (200, 200))
    def draw_text(self, text, x, y, color=WHITE):
        font = self.font

        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x+2, y+2))

        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))
    # This function calculates the maximum y position of the bird based on its current vertical velocity and gravity.
    def find_maxy(self, y, VY):
        if VY >= 0:
            return y  # already falling → no higher point

        T = -VY / GRAVITY
        return y + VY * T + 0.5 * GRAVITY * T**2
    def calculate_zoom(self, env):
        screen_maxy = HEIGHT -(HEIGHT-self.find_maxy(env.bird.y, env.bird.vy)) * self.target_zoom
        
        top_limit = HEIGHT * 0.05
        bottom_limit = HEIGHT * 0.2

        # Zoom OUT
        if screen_maxy < top_limit:
            self.target_zoom -=   0.02

        # Zoom IN (only when clearly back down)
        elif screen_maxy > bottom_limit:
            self.target_zoom += HEIGHT/(HEIGHT - screen_maxy) * 0.02

        # Clamp
        self.target_zoom =  min(1.0, self.target_zoom)
        if env.bird.countframes/FPS > GAMETIME-2:  # In the last 3 seconds, zoom out more to create a dramatic effect
            self.target_zoom = min(self.target_zoom, 0.7)
        if env.bird.countframes/FPS > GAMETIME and  env.bird.onground:  # In the last 3 seconds, zoom out more to create a dramatic effect
            self.target_zoom = 2.0
    def sky_color(self, time):
        t = min(time / 60, 1.0)
        r = SKY_BLUE[0] * (1 - t)
        g = SKY_BLUE[1] * (1 - t)
        b = SKY_BLUE[2] * (1 - t)

        return (int(r), int(g), int(b))
    def draw_sun(self, env):
        sun_x = WIDTH - 200
        sun_y = 300 +  20* env.bird.countframes / (FPS)   # Move sun down over time
              
        
        
        
        self.screen.blit(self.sun_img, (sun_x - self.sun_img.get_width() // 2, sun_y - self.sun_img.get_height() // 2))
    def draw_moon(self, env):
        
        moon_x = WIDTH - 450
        moon_y = HEIGHT * 1.2 -  20* env.bird.countframes / (FPS)   # Move moon up over time
        self.screen.blit(self.moon_img, (moon_x - self.moon_img.get_width() // 2, moon_y - self.moon_img.get_height() // 2))
    
    def draw_menu(self,env):
        self.screen.fill((SKY_BLUE))

        self.draw_text("BIRD GAME", WIDTH//2 - 80, HEIGHT//3)
        self.draw_text("Press SPACE to dive and to start", WIDTH//2 - 120, HEIGHT//2)
        self.draw_text("inspired by Tiny Wings", WIDTH//2 - 100, HEIGHT//3 + 30)
        
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)
        self.draw_sun(env)
        pygame.display.flip() 

    def draw_game_over(self, env):
        self.screen.fill((10, 10, 10))
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)
        self.draw_moon(env)
        font_big = pygame.font.SysFont("Arial", 64, bold=True)
        font_small = pygame.font.SysFont("Arial", 32)

        title = font_big.render("DAY OVER", True, (255, 255, 255))
        score = font_small.render(f"Score: {int(env.bird.score)}", True, (255, 200, 100))
        distance = font_small.render(f"Distance: {int(env.distance/100)}", True, (255, 200, 100))
        restart = font_small.render("Press R to restart", True, (200, 200, 200))

        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        self.screen.blit(score, (WIDTH//2 - score.get_width()//2, 260))
        self.screen.blit(distance, (WIDTH//2 - distance.get_width()//2, 300))

        self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 340))

       

        pygame.display.flip()

    def draw_all(self, env):
        self.screen.fill(self.sky_color(env.bird.countframes/FPS))

        self.calculate_zoom(env)
        self.zoom += (self.target_zoom - self.zoom) * 0.05
        
        self.draw_text(f"Distance: {int(env.distance/100)}", 10, 10)
        self.draw_text(f"Time left: {max(0, GAMETIME - int(env.bird.countframes/FPS))}", WIDTH/2-50, 10)
        self.draw_text(f"Score: {int(env.bird.score)}", WIDTH-200, 10)    

        # Show jump score if it's above 20
        if env.bird.jump_score > 20:
            self.draw_text(f"Jump Score: {int(env.bird.jump_score)}", WIDTH//2 - 100, HEIGHT//4  - 30)
        if env.bird.landing_timer > 0:
            self.draw_text(env.bird.last_landing_text, WIDTH//2 - 200, HEIGHT//4)
            self.draw_text(f"+{env.bird.added_score}", WIDTH - 200, 30)
            env.bird.landing_timer -= 1

        
        self.draw_sun(env)
        self.draw_moon(env)
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)

        pygame.display.flip()
