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

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 684

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Game')
bg_image = pygame.image.load("img/bg.png")
bg_image = pygame.transform.scale(bg_image,(SCREEN_WIDTH, SCREEN_HEIGHT))
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
scroll_speed = 5
#Game Checkers
game_over = False
pass_pipe = False
button_hit = False
Flying = False
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
    bird.rect.x = 60
    bird.rect.y = int(SCREEN_HEIGHT / 2)
    bird.reset_rotation()
    global scroll_speed, Flying
    scroll_speed = 5
    score = 0
    Flying = False
    return score



#create restart button instance
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_img)

keys = pygame.key.get_pressed()

#Making a pygame sprite list 
bullet_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
bird = Bird(60, int(SCREEN_HEIGHT/2), Flying, game_over, SCREEN_HEIGHT, keys)
bird_group.add(bird)


running = True
shoot = True
while running:
  clock.tick(FPS)

  #Variable storing keyboard inputs
  keys = pygame.key.get_pressed()

  #Getting the birds coordinates 
  for sprites in bird_group:
    bird_X,bird_y = sprites.rect.center
    sprites.Flying = Flying
    sprites.game_over = game_over
    sprites.keys = keys


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
  bird_group.update()
    
  #Draws and scrolls the background
  screen.blit(ground,(ground_scroll,SCREEN_HEIGHT - 100))

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
    
    #Shooting the bullets
    if keys[K_d] == 1 and shoot == True:
      shoot = False
      tempbullet = Bullet(bird_X,bird_y, SCREEN_WIDTH)
      bullet_group.add(tempbullet)
    if keys[K_d] == 0 and shoot == False:
      shoot = True
    
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
      #Making the pipes
      pipe_height = random.randint(-100, 100)
      btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT/2) + pipe_height, 1, False, scroll_speed)
      top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT/2) + pipe_height, -1, False, scroll_speed)
      
      target_height = random.randint(-50, 50)
      pipe_target = Target(SCREEN_WIDTH - 50, int(SCREEN_HEIGHT/2) + target_height, scroll_speed)

      target_group.add(pipe_target)
      pipe_group.add(btm_pipe)
      pipe_group.add(top_pipe)
      last_pipe = time_now



    #Detects if the bullet hits the target to open the pipe up.
    if pygame.sprite.groupcollide(bullet_group, target_group, True, True):
        top_pipe.move(top_pipe.rect.x, top_pipe.rect.y + (pipe_gap/2))
        btm_pipe.move(btm_pipe.rect.x, btm_pipe.rect.y - (pipe_gap/2))
       
    


    pipe_group.update()
    target_group.update()
      

  

      #Resets ground position to make the ground look like it is moving
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    
      
    #Game over checks
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
      game_over = True
      

    if bird.rect.bottom > SCREEN_HEIGHT - 110:
      game_over = True
      Flying = False

    #Varaible to make the ground move
    ground_scroll -= scroll_speed  
    
    
    
  if game_over == True:
      if button.draw(screen):
        game_over = False
        score = reset_game()
  


  #-----------------Event handeling-----------------
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN and Flying == False and game_over == False:
      if event.key == pygame.K_w:
        Flying = True
  pygame.display.update()

pygame.quit()    