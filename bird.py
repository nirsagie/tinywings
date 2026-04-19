import pygame
import math
from constants import *

class Bird:
    def __init__(self, hills=None):
        self.image = pygame.image.load("img/bird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        
        self.hills = hills
        
        self.bird_x = BIRD_SCREEN_X
        self.y = hills.get_y(BIRD_SCREEN_X)
        
        self.vx = 0
        self.vy = 0
        self.vt = 0
        self.countframes=0

    def reset(self):
        
        while self.hills.get_slope(BIRD_SCREEN_X)<0:
            self.hills.seed += 0.1
        self.y = self.hills.get_y(BIRD_SCREEN_X)
        self.vx = 0
        self.vy = 0
        self.vt = 0
        self.onground = True
        self.countframes=0
        
        


    def physics(self, dive=False):
        

        hill_y = self.hills.get_y(self.bird_x)
        slope = self.hills.get_slope(self.bird_x)
        angle = math.atan(slope)
        
        if self.y <= hill_y - 5:
            # באוויר
            self.vy += GRAVITY
            
            if dive:
                self.vy += DIVE_FORCE
            
            self.onground = False   
            
        else:
            # על הקרקע → רק לאורך השיפוע
            self.vt = self.vx * math.cos(angle) + self.vy * math.sin(angle)
        

            # 🔥 שומר כיוון ומהירות מינימלית
            if abs(self.vt) < 0.5:
                self.vt = 0.5 if self.vx >= 0 else -0.5

            if dive and slope > 0:  # Only dive if slope is negative (going downhill)
                self.vt += DIVE_FORCE * math.cos(angle)*0.3 # Add a small boost to help initiate the dive
            
            if not self.onground and self.vy >= 0:  # Just landed
                self.landing(angle)
                self.onground = True
            
            if self.y - hill_y > 2:  # tweak this
                self.y -= (self.y-hill_y)*0.5

            self.vx = abs(self.vt * math.cos(angle)) 
            self.vy = abs(self.vt) * math.sin(angle)
            
            if  self.hills.get_slope(self.bird_x+self.vx)<slope and slope<0: # If we're moving fast and should lunch
                self.vy-=abs(self.vt*math.sin(angle))*0.1 # Launch up based on speed, adjust multiplier for more/less launch
            
            

            

       
        
        
        # if self.countframes%10==0:
        #     print(angle, slope, self.vx, self.vy,dive)
    
    def landing(self,hillangle):
        print("Landing check..."+str(self.countframes))
        birdangle = math.atan(self.vy / self.vx) if self.vx != 0 else 0
        angle_diff = abs(birdangle - hillangle)
        if angle_diff < math.radians(30) and hillangle>0:  #the diffrence in angles is small enough and we're going downhill
            self.vt *= 1.1  # Perfect landing, give a small boost
            # print("Perfect landing!")
        elif angle_diff < math.radians(45) and hillangle>0:  # Acceptable landing
            self.vt *= 0.8
            # print("Good landing.")
        else:             
            self.vt *= 0.5  # Bad landing, heavy penalty
            # print("Bad landing, penalty applied.")
            
    def update(self, distance, dive=False):
        # print(f"Bird X: {self.bird_x:.2f}, Y: {self.y:.2f}, VX: {self.vx:.2f}, VY: {self.vy:.2f}")
        self.bird_x = distance + BIRD_SCREEN_X
        
        self.physics(dive=dive)
        
        self.y += self.vy
        
        # Get hill surface height at this position
        hill_y = self.hills.get_y(self.bird_x)
        # if self.y > hill_y:
        #     self.y = hill_y
            # self.vy = 0

        self.countframes+=1
    def draw(self, screen, zoom):
        scaled_width = max(1, int(50 * zoom))
        scaled_height = max(1, int(50 * zoom))
        bird_image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

        screen_y = HEIGHT - (HEIGHT - self.y) * zoom
        x = int(BIRD_SCREEN_X - scaled_width / 2)
        y = int(screen_y - scaled_height / 2)
        screen.blit(bird_image, (x, y))
    