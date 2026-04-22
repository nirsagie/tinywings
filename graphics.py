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
    def draw_text(self, text, x, y):
        img = self.font.render(text, True, WHITE)
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
            self.target_zoom -= HEIGHT/(HEIGHT - screen_maxy) * 0.02

        # Zoom IN (only when clearly back down)
        elif screen_maxy > bottom_limit:
            self.target_zoom += HEIGHT/(HEIGHT - screen_maxy) * 0.02

        # Clamp
        self.target_zoom =  min(1.0, self.target_zoom)
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
    def draw_all(self, env):
        self.screen.fill(self.sky_color(env.bird.countframes/FPS))

        self.calculate_zoom(env)
        self.zoom += (self.target_zoom - self.zoom) * 0.05
        
        self.draw_text(f"Distance: {int(env.distance/100)}", 10, 10)
        self.draw_text(f"Speed: {int(env.bird.vx)}", 10, 40)
        self.draw_text(f"time: {int(env.bird.countframes/FPS)}s", 10, 70)

        self.draw_sun(env)
        self.draw_moon(env)
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)

        pygame.display.flip()
