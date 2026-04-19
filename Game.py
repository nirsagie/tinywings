import pygame
from constants import *
from graphics import Graphics
from environment import Environment

# Initialize display first (needed for Bird to load image)
gfx = Graphics()
# 1. Create the ACTUAL objects (Instances)
env = Environment()
clock = pygame.time.Clock()
space_pressed = False
running = True
while running:
    # 2. Maintain 60 Frames Per Second
    clock.tick(60)  # Adjusted for faster testing, change to FPS for normal speed
    
    # לולאת אירועים (Events)   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                env.reset()
            if event.key == pygame.K_SPACE:
                space_pressed = True
            if event.key == pygame.K_l:
                env.bird.lunch()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:              
                space_pressed = False    
    #     3. Update the logic (Movement)
    env.update(space_pressed)  # Commented out for still frame                 
    
    # 4. Draw the game using the instance 'gfx'
    
    
pygame.quit()                    