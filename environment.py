
import pygame
import math
import random

from bird import Bird
from hills import Hills
from constants import *
from graphics import Graphics
class Environment:
    def __init__(self):
        self.hills = Hills()
        self.bird = Bird(self.hills)  # Pass hills reference
        self.distance = 0
        self.reset()
        self.gfc = Graphics()
        self.update()
        

    def reset(self):
        # נתונים בסיסיים של הציפור    
        self.hills.reset()
        self.bird.reset()
        self.distance = 0
        



    def update(self, space_pressed=False):
        self.bird.update(self.distance, dive=space_pressed)
        self.distance += self.bird.vx
        self.gfc.draw_all(self,self.bird.vt)