import pygame
import os
import sys
from pygame.locals import *
import random
from Classlib import *
from Button import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 937

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird Game')
bg_image = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")
button_img = pygame.image.load("img/restart.png")

#color
WHITE = (255,255,255)
#Game variables
pipe_gap = 150
pipe_frequency = 4000 #in milliseconds
last_pipe = pygame.time.get_ticks() 
#Variables for making the ground animation
ground_scroll = 0
scroll_speed  = 5
#Game Checkers
game_over = pass_pipe = button_hit = Flying = False
score = 0
bullet = []

font = pygame.font.SysFont('Bauhaus 93', 60)
   
#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
    target_group.empty()
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = int(SCREEN_HEIGHT / 2)
    scroll_speed = 5
    score = 0
    return score



#create restart button instance
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_img)

#Making a pygame sprite list 
bullet_group, bird_group, target_group, pipe_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
bird = Bird(100, int(SCREEN_HEIGHT/2), Flying)
bird_group.add(bird)


running = True
shoot = True
while running:
    clock.tick(FPS)
    
    
    print(button_hit)
    
    #Variable storing keyboard inputs
    keys = pygame.key.get_pressed()

    #Getting the birds coordinates 
    for sprites in bird_group:
      bird_X,bird_y = sprites.rect.center
      sprites.Flying = Flying

    #Drawing and updating stuff on the screen
    screen.blit(bg_image,(0,0))

    #Drawing the bullet
    bullet_group.draw(screen)
    bullet_group.update()

    #Drawing the target
    target_group.draw(screen)

    #Drawing the pipe
    pipe_group.draw(screen)

    #Drawing the player
    bird_group.draw(screen)
    bird_group.update(game_over)

    #Draws and scrolls the background
    screen.blit(ground,(ground_scroll,768))

    #checks if the bird went past a pipe, increasing the score.
    if len(pipe_group) > 0:
      if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
        pass_pipe = True
      if pass_pipe == True:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
          score += 1
          scroll_speed += 1
          pass_pipe = False
    draw_text(str(score), font, WHITE, int(SCREEN_WIDTH / 2), 50)
  
    #-------------Game Logic (Update game state here)-------------
    if game_over == False and Flying == True:

      #Drawing the stuff onto the screen
      ground_scroll -= scroll_speed  #Varaible to make the ground move

      

      #Shooting the bullets
      if keys[K_SPACE] == 1 and shoot == True:
        shoot = False
        tempbullet = Bullet(bird_X,bird_y, SCREEN_WIDTH)
        bullet_group.add(tempbullet)
      if keys[K_SPACE] == 0 and shoot == False:
       shoot = True
       
      time_now = pygame.time.get_ticks()
      if time_now - last_pipe > pipe_frequency:
        #Making the pipes
        pipe_height = random.randint(-100, 100)
        btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT/2) + pipe_height, 1, False, scroll_speed)
        top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT/2) + pipe_height, -1, False, scroll_speed)
        
        target_height = random.randint(0, 100)
        pipe_target = Target(SCREEN_WIDTH - 50, int(SCREEN_HEIGHT/2) + target_height, scroll_speed)

        target_group.add(pipe_target)
        pipe_group.add(btm_pipe)
        pipe_group.add(top_pipe)
        last_pipe = time_now
      

      pipe_group.update()
      target_group.update()
    

      #Resets ground position to make the ground look like it is moving
      if abs(ground_scroll) > 35:
          ground_scroll = 0
      
      #Detects if the bullet hits the target to open the pipe up.
      if pygame.sprite.groupcollide(bullet_group, target_group, True, True):
        btm_pipe.move(btm_pipe.rect.x, btm_pipe.rect.y - (pipe_gap/2))
        top_pipe.move(top_pipe.rect.x, top_pipe.rect.y + (pipe_gap/2))

      #Game over checks
      if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True
        

      if bird.rect.bottom > 768:
        game_over = True
        Flying = False
      
      
      
    if game_over == True:
        if button.draw(screen):
          game_over = False
          score = reset_game()
    


    #-----------------Event handeling-----------------
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
      if event.type == pygame.MOUSEBUTTONDOWN and Flying == False and game_over == False:
        Flying = True
    
    pygame.display.update()

pygame.quit()    
    



