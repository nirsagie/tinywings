import pygame
from constants import *

class Graphics:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("Arial", 24)
        self.zoom = 1.0

    def draw_all(self, env, speed):
        self.screen.fill(SKY_BLUE)

        # Zoom out when speed increases, with smooth interpolation.
        target_zoom = 1.0 - min(abs(speed) * 0.01, 0.4)
        self.zoom += (target_zoom - self.zoom) * 0.1

        env.hills.draw(self.screen, env.distance, self.zoom)
        env.bird.draw(self.screen, self.zoom)

        pygame.display.flip()
