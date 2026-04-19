import math
import random
from constants import *
class Hills:
    def __init__(self):
        self.seed = random.uniform(0, 1000)
        

    def get_y(self, x):
        """ The math that defines the landscape """
        y = (HILL_AMPLITUDE * math.sin(x * 0.005 + self.seed) + 
             30 * math.sin(x * 0.02 + self.seed) + 
             20 * math.sin(x * 0.03 - self.seed) + HILL_BASE_Y)
        # y=HILL_BASE_Y+HILL_AMPLITUDE*math.sin(x * 0.005 + self.seed)
        return y

    def reset(self):
        self.seed = random.uniform(0, 1000)

    def get_slope(self, x):

        
        slope=(HILL_AMPLITUDE * 0.005 * math.cos(x * 0.005 + self.seed) + 
               30 * 0.02 * math.cos(x * 0.02 + self.seed) + 
               20 * 0.03 * math.cos(x * 0.03 - self.seed))
        # slope =HILL_AMPLITUDE*0.005*math.cos(x * 0.005 + self.seed)
        return slope
    def draw(self, screen, distance, zoom):
        points = []
        for screen_x in range(0, WIDTH + 11, 20):
            world_x = distance + BIRD_SCREEN_X + (screen_x - BIRD_SCREEN_X) / zoom
            y = self.get_y(world_x)
            screen_y = HEIGHT - (HEIGHT - y) * zoom
            points.append((screen_x, screen_y))
            
        points.append((WIDTH, HEIGHT))
        points.append((0, HEIGHT))
        pygame.draw.polygon(screen, HILL_GREEN, points)