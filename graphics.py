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
        self.screen.blit(shadow, (x+2-shadow.get_width()//2, y+2))

        img = font.render(text, True, color)
        self.screen.blit(img, (x-img.get_width()//2, y))
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
        moon_y = max(HEIGHT/3, HEIGHT * 1.2 -  20 *  (env.bird.countframes / (FPS) - 20))   # Move moon up over time
        self.screen.blit(self.moon_img, (moon_x - self.moon_img.get_width() // 2, moon_y - self.moon_img.get_height() // 2))
    
    def draw_menu(self,env):
        self.screen.fill((SKY_BLUE))

        self.draw_text("BIRD GAME", WIDTH//2 , HEIGHT//3)
        self.draw_text("Press SPACE to dive and to start", WIDTH//2 , HEIGHT//2)
        self.draw_text("inspired by Tiny Wings", WIDTH//2 , HEIGHT//3 + 30)
        
        # self.zoom = 1.5
        # self.target_zoom = 1.0
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)
        self.draw_sun(env)
        pygame.display.flip() 


    def draw_game_over(self, env):
    # --- dark overlay instead of full black ---
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.set_alpha(180)
        fade.fill((0, 0, 0))

        # draw last frame behind
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)
        self.draw_moon(env)

        self.screen.blit(fade, (0, 0))

        # --- animation ---
        t = pygame.time.get_ticks() / 300
        offset = int(5 * math.sin(t))

        # --- fonts ---
        font_big = pygame.font.SysFont("Arial", 64, bold=True)
        font_small = pygame.font.SysFont("Arial", 32)

        # --- dynamic score color ---
        if env.bird.score >= env.bird.highscore:
            score_color = (255, 215, 0)  # gold
            title_text = "NEW RECORD!"
        else:
            score_color = (255, 200, 100)
            title_text = "DAY OVER"

        # --- render ---
        title = font_big.render(title_text, True, (255, 255, 255))
        score = font_small.render(f"Score: {int(env.bird.score)}", True, score_color)
        distance = font_small.render(f"Distance: {int(env.distance/100)}", True, (200, 200, 200))
        high_score = font_small.render(f"High Score: {int(env.bird.highscore)}", True, score_color)
        restart = font_small.render("Press R to restart", True, (150, 150, 150))

        # --- draw centered ---
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 140 + offset))
        self.screen.blit(score, (WIDTH//2 - score.get_width()//2, 240))
        self.screen.blit(high_score, (WIDTH//2 - high_score.get_width()//2, 280))
        self.screen.blit(distance, (WIDTH//2 - distance.get_width()//2, 320))
        self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 400))

        pygame.display.flip()
    def draw_path(self, env):
        points = []
        divepoints = []

        if env.bird.vx == 0:
            return

        normal_landing = None
        dive_landing = None

        for screen_x in range(0, WIDTH + 11, 10):
            world_x = env.distance + BIRD_SCREEN_X + (screen_x - BIRD_SCREEN_X) / self.zoom
            
            dx = world_x - env.bird.bird_x
            t = dx / env.bird.vx

            if t < 0:
                continue

            # --- trajectories ---
            y = env.bird.y + env.bird.vy * t + 0.5 * GRAVITY * t * t
            divey = env.bird.y + env.bird.vy * t + 0.5 * (GRAVITY + DIVE_FORCE) * t * t

            hill_y = env.hills.get_y(world_x)

            # detect landing
            if normal_landing is None and y > hill_y:
                normal_landing = (world_x, t)

            if dive_landing is None and divey > hill_y:
                dive_landing = (world_x, t)

            screen_y = HEIGHT - (HEIGHT - y) * self.zoom
            screendivey = HEIGHT - (HEIGHT - divey) * self.zoom

            points.append((screen_x, screen_y))
            divepoints.append((screen_x, screendivey))

        # --- NORMAL landing color ---
        if normal_landing is None:
            normal_color = (150, 150, 150)
        else:
            wx, t = normal_landing
            vy_t = env.bird.vy + GRAVITY * t
            bird_angle = math.atan2(vy_t, env.bird.vx)

            slope = env.hills.get_slope(wx)
            hill_angle = math.atan(slope)

            diff = abs(bird_angle - hill_angle)

            if diff < math.radians(25):
                normal_color = (0, 255, 0)
            elif diff < math.radians(45):
                normal_color = (255, 200, 0)
            else:
                normal_color = (255, 50, 50)

        # --- DIVE landing color ---
        if dive_landing is None:
            dive_color = (150, 150, 150)
        else:
            wx, t = dive_landing
            vy_t = env.bird.vy + (GRAVITY + DIVE_FORCE) * t
            bird_angle = math.atan2(vy_t, env.bird.vx)

            slope = env.hills.get_slope(wx)
            hill_angle = math.atan(slope)

            diff = abs(bird_angle - hill_angle)

            if diff < math.radians(25):
                dive_color = (0, 255, 0)
            elif diff < math.radians(45):
                dive_color = (255, 200, 0)
            else:
                dive_color = (255, 50, 50)

        # --- draw ---
        if len(points) > 1:
            pygame.draw.lines(self.screen, normal_color, False, points, 2)

        if len(divepoints) > 1:
            pygame.draw.lines(self.screen, dive_color, False, divepoints, 2)
    def draw_all(self, env):
        self.screen.fill(self.sky_color(env.bird.countframes/FPS))

        self.calculate_zoom(env)
        self.zoom += (self.target_zoom - self.zoom) * 0.05
        
        self.draw_text(f"Distance: {int(env.distance/100)}", 70, 10)
        self.draw_text(f"Time left: {max(0, GAMETIME - int(env.bird.countframes/FPS))}", WIDTH/2, 10)
        self.draw_text(f"Score: {int(env.bird.score)}", WIDTH-120, 10)    
        self.draw_text(f"High Score: {int(env.bird.highscore)}", WIDTH-100, 40)

        # Show jump score if it's above 20
        if env.bird.jump_score > 20:
            self.draw_text(f"Jump Score: {int(env.bird.jump_score)}", WIDTH//2 , HEIGHT//4  - 30)
        if env.bird.landing_timer > 0:
            self.draw_text(env.bird.last_landing_text, WIDTH//2 , HEIGHT//4)
            self.draw_text(f"+{env.bird.added_score}", WIDTH -30, 10)
            env.bird.landing_timer -= 1

        
        self.draw_sun(env)
        self.draw_moon(env)
        # self.draw_path(env)
        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)

        pygame.display.flip()
