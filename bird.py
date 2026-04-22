from tkinter import SEL

import pygame
import math
from constants import *
import graphics
class Bird:
    def __init__(self, hills=None):
        self.image = pygame.image.load("img/bird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.gfx=graphics.Graphics()
        self.hills = hills
        
        
    def reset(self):
        
        while self.hills.get_slope(BIRD_SCREEN_X)<=0.1:  # Ensure we start on a downward slope
            self.hills.seed += 0.1
        self.bird_x = BIRD_SCREEN_X
        self.y = self.hills.get_y(BIRD_SCREEN_X)
        self.vx = 0
        self.vy = 0
        self.vt = 0
        self.countframes=0
        self.score = 0
        self.jump_score = 0
        self.landing_timer=0
        self.onground = True
        self.g= GRAVITY
        self.last_landing_text=""
        


    def physics(self, dive=False):
        

        hill_y = self.hills.get_y(self.bird_x)
        slope = self.hills.get_slope(self.bird_x)
        angle = math.atan(slope)
        self.vt = self.vx * math.cos(angle) + self.vy * math.sin(angle)
        if self.y <= hill_y - 5:
            # באוויר
            self.vy += self.g  # Gravity
            
            if dive and self.countframes/FPS < GAMETIME:  # Only allow diving before time is up
                self.vy += DIVE_FORCE
            
            self.onground = False   

            self.jump_score += 1
            
        else:
            # על הקרקע → רק לאורך השיפוע
            if not self.onground and self.vy >= 0:  # Just landed
                self.landing(angle)
                self.onground = True
        

            # 🔥 שומר כיוון ומהירות מינימלית
            
            if self.countframes/FPS < GAMETIME:
                if abs(self.vt) < 5:
                    self.vt = max(self.vt, 5)  # Ensure minimum speed to keep the game moving
                if dive and slope > 0:  # Only dive if slope is negative (going downhill)
                    self.vt += DIVE_FORCE * math.cos(angle)*0.5 # Add a small boost to help initiate the dive
                if dive and slope < -0.1 and self.vt>1:  # If diving while going uphill, reduce speed to simulate struggle
                    self.vt -= DIVE_FORCE * math.cos(angle)*0.5
            else:
                    self.vt *= 0.98  # Gradually slow down in the last seconds to create tension
          
            
            if self.y - hill_y > 2:  # tweak this
                self.y -= (self.y-hill_y)*0.5

            self.vx = abs(self.vt * math.cos(angle)) 
            self.vy = abs(self.vt) * math.sin(angle)
            
            if   slope<0 and not dive: # If we're moving fast and should lunch
                self.vy-=abs(self.vt*math.sin(angle))*0.05 # Launch up based on speed, adjust multiplier for more/less launch

            self.vt *= (1 - FRICTION)  # Apply friction to slow down on the ground
            
            

            

       
        
        
        # if self.countframes%10==0:
        #     print(angle, slope, self.vx, self.vy,dive)
    
    def landing(self,hillangle):
        
        birdangle = math.atan(self.vy / self.vx) if self.vx != 0 else 0
        angle_diff = abs(birdangle - hillangle)
        if angle_diff < math.radians(30) and hillangle>0:  #the diffrence in angles is small enough and we're going downhill
            self.vt *= 1.1  # Perfect landing, give a small boost
            if self.jump_score > 20:
                self.last_landing_text = "Perfect Landing! x3 Score! score added: " + str(int(self.jump_score*3))
                self.added_score = int(self.jump_score*3)
                self.landing_timer = 100  # frames
            self.score += self.jump_score*3
            # print("Perfect landing! Bonus applied.")
        elif angle_diff < math.radians(45) and hillangle>0:  # Acceptable landing
            self.vt *= 0.8
            if self.jump_score > 20:
                self.last_landing_text = "Good Landing! x2 Score! score added: " + str(int(self.jump_score*2))
                self.added_score = int(self.jump_score*2)
                self.landing_timer = 100  # frames
            self.score += self.jump_score*2
            # print("Good landing.")
        else:             
            self.vt *= 0.5  # Bad landing, heavy penalty
            if self.jump_score > 20:
                self.last_landing_text = "Bad Landing! score added: " + str(int(self.jump_score*1))
                self.added_score = int(self.jump_score*1)
                self.landing_timer = 100  # frames
            self.score += self.jump_score*1
            # print("Bad landing, penalty applied.")
        self.jump_score=0

    
    def update(self, distance, dive=False):
        # print(f"Bird X: {self.bird_x:.2f}, Y: {self.y:.2f}, VX: {self.vx:.2f}, VY: {self.vy:.2f}")
        self.bird_x = distance + BIRD_SCREEN_X
        
        self.physics(dive=dive)
        
        self.y += self.vy
        
        self.score += self.vx * 0.05  # Increment score based on distance traveled

        self.countframes+=1

        
            
    def draw(self, screen, zoom):
        scaled_width = max(1, int(40 * zoom))
        scaled_height = max(1, int(40 * zoom))
        bird_image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))
        bird_image = pygame.transform.rotate(bird_image, -math.degrees(math.atan(self.vy / self.vx)) if self.vx != 0 else 0)

        screen_y = HEIGHT - (HEIGHT - self.y) * zoom
        x = int(BIRD_SCREEN_X - scaled_width / 2)
        y = int(screen_y - scaled_height / 2)
        screen.blit(bird_image, (x, y))
    