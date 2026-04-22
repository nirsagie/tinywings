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
state = MENU
while running:
    # 2. Maintain 60 Frames Per Second
    clock.tick(60)  # Adjusted for faster testing, change to FPS for normal speed
    
    # לולאת אירועים (Events)   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = GAME
        elif state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    env.reset() 
                    state = MENU
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:              
                    space_pressed = False    
        elif state == GAME_OVER:
            gfx.draw_game_over(env)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    env.reset()
                    state = MENU
    #     3. Update the logic (Movement)
    time_sec = env.bird.countframes / FPS

    if time_sec >= GAMETIME and env.bird.onground and env.bird.vt <= 0.1:  # End game if time is up and bird is on the ground and has essentially stopped
        state = GAME_OVER
    if state == MENU:
        gfx.draw_menu(env)

    elif state == GAME:
        env.update(space_pressed)
        gfx.draw_all(env)
    if state == GAME_OVER:
        gfx.draw_game_over(env)
        
 # Commented out for still frame                 
    
    # 4. Draw the game using the instance 'gfx'
    
    
pygame.quit()                    