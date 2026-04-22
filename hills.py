import math
import random
from constants import *
class Hills:
    def __init__(self):
        self.seed = random.uniform(0, 1000)
        

    def get_y(self, x):
        amp = HILL_AMPLITUDE * (1 + 0.3 * math.sin(x * 0.001 + self.seed))
        return (
            HILL_BASE_Y
            + amp * math.sin((math.sqrt(7) * x + self.seed) / HILL_PERIOD)
            + 0.5 * amp * math.sin((x + self.seed * 0.7) / (HILL_PERIOD * 0.5))
        )

    def reset(self):
        self.seed = random.uniform(0, 1000)

    def get_slope(self, x):
        amp= HILL_AMPLITUDE * (1 + 0.3 * math.sin(x * 0.001 + self.seed))
        return (
            amp * math.sqrt(7) / HILL_PERIOD * math.cos((math.sqrt(7) * x + self.seed) / HILL_PERIOD)
            + 0.5 * amp / (HILL_PERIOD * 0.5) * math.cos((x + self.seed * 0.7) / (HILL_PERIOD * 0.5))
        )
    def draw(self, screen, distance, zoom):
        points = []
        for screen_x in range(0, WIDTH + 11, 10):
            world_x = distance + BIRD_SCREEN_X + (screen_x - BIRD_SCREEN_X) / zoom
            y = self.get_y(world_x)
            screen_y = HEIGHT - (HEIGHT - y) * zoom 
            points.append((screen_x, screen_y))
            
        points.append((WIDTH, HEIGHT))
        points.append((0, HEIGHT))
        pygame.draw.polygon(screen, HILL_GREEN, points)