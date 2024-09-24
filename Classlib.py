import pygame
# from Flappybird import Flying

class Bird(pygame.sprite.Sprite):
  def __init__(self,x,y, Flying, game_over, SCREEN_HEIGHT):
    super().__init__() #Inherit functionalities
    self.images = []
    self.index = 0
    self.counter = 0
    
    #Goes through the images to animate the bird
    for num in range(1,4):
        img = pygame.image.load(f"img/Bird{num}.png")
        self.images.append(img)

    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x,y]
    self.clicked = False
    
    
    
    #Gravity
    self.vel = 0 

    #main
    self.Flying = Flying
    self.game_over = game_over
    self.SCREEN_HEIGHT = SCREEN_HEIGHT
    
  def update(self):
    #Constantly changes the players y value. Gravity
    if self.Flying == True:
      self.vel += 0.5
      if self.vel > 8:
        self.vel = 8
      #Prevents the bird from falling through the window 
      if self.rect.bottom < self.SCREEN_HEIGHT - 100:
        self.rect.y += int(self.vel)

    if self.game_over == False:
      #Flapping
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
          self.clicked = True
          self.vel = -10
      if pygame.mouse.get_pressed()[0] == 0:
          self.clicked = False
      

      #handling the animations
      self.counter += 1
      flap_cooldown = 5
      #checks the animation counts to know when to reset
      if self.counter > flap_cooldown:
        self.counter = 0
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
      self.image = self.images[self.index]

      #Rotating the bird when space is clicked
      self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
    else:    
        #point the bird at the ground
        self.image = pygame.transform.rotate(self.images[self.index], -90)
                
  def reset_rotation(self):
      self.image = pygame.transform.rotate(self.images[self.index], 0)
        
    
     


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, open, scroll_speed):
      super().__init__()
      self.image = pygame.image.load('img/pipe.png')
      self.rect = self.image.get_rect()
      self.open = False
      

      if position == 1 and open == False: 
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect.bottomleft = [x,y]
         
      if position == -1 and open == False:
         self.rect.topleft = [x, y]

      #Flappybird.py imports
      self.scroll_speed = scroll_speed  

    def update(self):
      self.rect.x -= self.scroll_speed
      if self.rect.right < 0:
         self.kill()
         

    def move(self, change_x, change_y):
       self.rect.x = change_x
       self.rect.y = change_y
      
			    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, SCREEN_WIDTH):
      super().__init__()

      self.image = pygame.image.load("img/bullet.png")
      self.rect = self.image.get_rect()
      self.rect.center = [x,y]
      self.vel = 7

      #Main imports
      self.SCREEN_WIDTH = SCREEN_WIDTH
      
    def update(self):
       self.rect.x += self.vel
       if self.rect.x > self.SCREEN_WIDTH:
          self.kill()

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, scroll_speed):
       super().__init__()
       self.image = pygame.image.load("img/Target.png")
       self.rect = self.image.get_rect()
       self.rect.center = [x,y]

       #Flappybird.py imports
       self.scroll_speed = scroll_speed
    def update(self):
       self.rect.x -= self.scroll_speed
    
