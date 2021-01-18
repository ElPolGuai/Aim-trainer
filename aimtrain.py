import pygame as p 
import os
import random as r
import sys
import math

os.environ['SDL_VIDEO_CENTERED'] = '1'
p.init()
p.display.set_caption('Aim Trainer By ElPolG')

WIDTH, HEIGHT = 1600, 800
BLACK = (51, 51, 51)
ORANGE = (254, 92, 76)
SCREEN = p.display.set_mode((WIDTH, HEIGHT))
CLOCK = p.time.Clock()
FONT = p.font.SysFont('Comic Sans MS', 50, True)
FONT1 = p.font.SysFont('Comic Sans MS', 30, True)
DIRECTORY = 'C:/Users/Sonia/Desktop/Software/Python/AimTrainer/' #Change this directory to yours
PLAY_BUTTON = p.transform.scale(p.image.load(f'{DIRECTORY}Images/PLAY_BUTTON.png'), (300, 100))
PLAY_AGAIN_BUTTON = p.transform.scale(p.image.load(f'{DIRECTORY}Images/PLAY_AGAIN_BUTTON.png'), (300, 100))
AIM_WIDTH, AIM_HEIGHT = 50, 50
AIM_TARGET = p.transform.scale(p.image.load(f'{DIRECTORY}Images/aim_target.jpg'), (AIM_WIDTH, AIM_HEIGHT))

click = False

def main_menu():
    while True: 
        SCREEN.fill(BLACK)
        SCREEN.blit(PLAY_BUTTON, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        
        mouse_x, mouse_y = p.mouse.get_pos()
        button_play = p.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)

        if button_play.collidepoint((mouse_x, mouse_y)): #If mouse is on the play button 
            if click:
                game()

        click = False 

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        p.display.update()
        CLOCK.tick(60)

def game():
    time_countdown = 3
    time_in_game = 63
    timer_countdown = p.USEREVENT + 1
    timer_in_game = p.USEREVENT + 2
    timer_text_countdown = FONT.render(" 3", True, (ORANGE))
    timer_text_in_game = FONT1.render("60", True, (ORANGE))
    p.time.set_timer(timer_countdown, 1000)
    p.time.set_timer(timer_in_game, 1000)
    random_x, random_y = r.randint(0, WIDTH - AIM_WIDTH), r.randint(60, HEIGHT - AIM_HEIGHT)
    radius = AIM_WIDTH // 2
    rect = AIM_TARGET.get_rect(center=(random_x + AIM_WIDTH // 2, random_y + AIM_HEIGHT // 2))
    global points, misses
    points, misses = 0, 0

    while True:    
        SCREEN.fill(BLACK)
        
        mouse_x, mouse_y = p.mouse.get_pos()
        dist_x, dist_y = mouse_x - rect.centerx, mouse_y - rect.centery

        click = False 

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            
            elif event.type == timer_countdown:
                if time_countdown > 0:
                    time_countdown -= 1
                    timer_text_countdown = FONT.render("%2d" % time_countdown, True, (ORANGE))
                
                else:
                    p.time.set_timer(timer_countdown, 0)
            
            elif event.type == timer_in_game:
                if time_in_game > 0:
                    time_in_game -= 1
                    timer_text_in_game = FONT1.render("TIME: %02d" % time_in_game, True, (ORANGE))
                
                else:
                    p.time.set_timer(timer_in_game, 0)
     
        if time_countdown > 0:
            SCREEN.blit(timer_text_countdown, (WIDTH // 2 - 25, HEIGHT // 2 - 25))
        
        else:
            if time_in_game > 0:
                SCREEN.blit(timer_text_in_game, (WIDTH - 190, 25))
            
            else:
                result()
                break

            SCREEN.blit(AIM_TARGET, (random_x, random_y))
            if click:
                if math.hypot(dist_x, dist_y) < radius:
                    random_x, random_y = r.randint(0, WIDTH - AIM_WIDTH), r.randint(60, HEIGHT - AIM_HEIGHT)
                    dist_x, dist_y = mouse_x - rect.centerx, mouse_y - rect.centery
                    rect = AIM_TARGET.get_rect(center=(random_x + AIM_WIDTH // 2, random_y + AIM_HEIGHT // 2))
                    points += 1
                
                else:
                    misses += 1
        
            SCREEN.blit(FONT1.render(f"POINTS: {points}", True, (ORANGE)), (50, 25))       

        p.display.update()
        CLOCK.tick(60)

def result():
    if points + misses == 0:
        accuracy = 0
    
    else:
        accuracy = round(points / (points + misses) * 100, 2)

    while True:
        mouse_x, mouse_y = p.mouse.get_pos()
        button_play_again = p.Rect(WIDTH // 2 - 200, HEIGHT - 250, 300, 100)

        SCREEN.fill(BLACK)
        SCREEN.blit(FONT1.render(f"TOTAL HIT TARGETS: {points}", True, (ORANGE)), (200, HEIGHT // 2 - 115))
        SCREEN.blit(FONT1.render(f"MISSED TARGETS: {misses}", True, (ORANGE)), (200, HEIGHT // 2 - 75))
        SCREEN.blit(FONT1.render(f"ACCURACY: {accuracy}%", True, (ORANGE)), (900, HEIGHT // 2 - 75))
        SCREEN.blit(FONT1.render(f"TARGETS HIT PER SECOND: {round(points / 60, 2)}", True, (ORANGE)), (900, HEIGHT // 2 - 115))
        SCREEN.blit(FONT.render(f"TOTAL SCORE: {int(round(points * accuracy / 10, 0))}", True, (ORANGE)), (500, HEIGHT // 3 - 100))
        SCREEN.blit(PLAY_AGAIN_BUTTON, (WIDTH // 2 - 200, HEIGHT - 250))

        if button_play_again.collidepoint((mouse_x, mouse_y)):
            if click:
                main_menu()

        click = False

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
                
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        p.display.update()
        CLOCK.tick(60)

main_menu()