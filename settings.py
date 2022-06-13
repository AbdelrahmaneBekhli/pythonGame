import pygame
from csv import reader

WIDTH = 1280
HEIGHT = 700
SIZE = WIDTH, HEIGHT
pygame.display.set_caption('The adventures of the lost kid') #sets the title of the program
SCREEN = pygame.display.set_mode(SIZE) #loads the program with the set screen size
Clock = pygame.time.Clock()
FPS = 60

tile_size = 64

cooldown_count = 0
current_time = 0
button_press_time = 0
image_count = 0

music_status = True

character_used = None

menu = False

#colors are set as constants so they can recalled
BLACK = (0, 0, 0, 128)
WHITE = (255, 255, 255)
DARK_GREEN = (9,74,58)
GREEN = (9,128,58)
DARK_BLUE = (44,67,111)
PINK = (255,20,147)
BLUE = (0 ,0,255)
GREY = (128,128,128)
LIGHT_BLACK = (21,19,40)
NAVY = (0,0,128)
RED = (255, 0, 0)

class create_button():
  def __init__ (self,msg,x,y,width,height, hover_color,action=None, size=None, font=None, color = None,):
    self.msg = msg
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color
    self.hover_color = hover_color
    self.action = action
    self.size = size
    self.font = font

  def button(self): #Function to make the buttons
    pygame.init()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() 
    if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y: #checks if the mouse is hovering over the button
      if self.color != None:
        pygame.draw.rect(SCREEN, self.hover_color,(self.x,self.y,self.width,self.height)) #if the check was positive it will change the color of the button
      else:
        button_background = pygame.Surface((self.width,self.height))# the size of the rectangles
        button_background.set_alpha(180)# alpha level
        button_background.fill(self.hover_color)# this fills the entire surface
        SCREEN.blit(button_background, (self.x,self.y,self.width,self.height)) 
      
      if click[0] == 1 and self.action != None: #checks if the button has been clicked
          self.action()

              
    else:
      if self.color != None:
        pygame.draw.rect(SCREEN, self.color,(self.x,self.y,self.width,self.height)) #draws the box for the button
    if self.size == None and self.font == None: 
      text = create_text(self.msg,'fonts/BLACK.ttf', self.x+(self.width/2), self.y+(self.height/1.7), 30, WHITE)
    elif self.size != None and self.font == None:
      text = create_text(self.msg,'fonts/BLACK.ttf', self.x+(self.width/2), self.y+(self.height/1.7), self.size, WHITE)
    elif self.size != None and self.font != None:
      text = create_text(self.msg,self.font, self.x+(self.width/2), self.y+(self.height/1.7), self.size, WHITE)
    elif self.size == None and self.font != None:
      text = create_text(self.msg,self.font, self.x+(self.width/2), self.y+(self.height/1.7), 45, WHITE)
    text.set_text()

def music_control():
  global music_status
  if music_status == True: #checks if the music is already playing
    pygame.mixer.music.set_volume(0)#sets the volume music to 0
    music_status = False
  elif music_status == False:
    pygame.mixer.music.set_volume(1)#sets the volume to 1
    music_status = True

def cooldown():
  global cooldown_count, current_time, button_press_time
  if cooldown_count == 1: #checks if the button has been pressed
    if current_time - button_press_time > 10: #checks if the cooldown has passed
      cooldown_count = 0 #resets the variable so that it can check again for the button pressed

def mute_button(): #Function to make the buttons
  pygame.init()
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed() 
  mutes = ['main_images/unmute.png', 'main_images/mute.png']

  w = 50 #width of the image
  h = 50 #height of the image
  x = 1190 #x coordiante of the image
  y = 50 #y coordinate of the image
  global image_count, cooldown_count, current_time, button_press_time
  if w + x > mouse[0] > x and h + y > mouse[1] > y: #checks if the mouse is hovering over the button
    if click[0] == 1: #checks if the button has been clicked
      button_press_time = pygame.time.get_ticks() #gets the time when the user clicked the button
      if cooldown_count == 0:
        image_count = image_count + 1 #increases the index for the music images in the list
        music_control()
        cooldown_count = cooldown_count + 1 # adds 1 to the cooldown
  current_time = pygame.time.get_ticks() #gets the current time
  cooldown()
  if image_count > 1:
    image_count = 0
  image = pygame.image.load(mutes[image_count])
  img_size = pygame.transform.scale(image, (w,h))#resizes the image
  SCREEN.blit(img_size, (x, y))

def csv_data(path):
  data = [] #stores the values of each data in the file
  with open(path) as map:
    level = reader(map, delimiter = ",")
    for row in level: ##reads the content of the csv files
      data.append(list(row))
    return data

def cut_tiles(path):
  surface = pygame.image.load(path).convert_alpha()
  surface.set_colorkey(BLACK) #removes any back bakhground on the surface
  tile_num_x = int(surface.get_size()[0] / tile_size) #gets how many tiles on the x axis
  tile_num_y = int(surface.get_size()[1] / tile_size) #gets how many tiles on the y axis

  cut_tiles = []
  for row in range(tile_num_y):
    for col in range(tile_num_x):
      x = col * tile_size
      y = row * tile_size
      new_surf = pygame.Surface((tile_size,tile_size), flags = pygame.SRCALPHA)#removes the black bacground
      new_surf.blit(surface,(0,0), pygame.Rect(x,y, tile_size, tile_size))
      cut_tiles.append(new_surf)
  return cut_tiles

class create_text():
  def __init__ (self, string, font, x, y, fontSize, color, Center = None):
    self.string = string
    self.font = font
    self.x = x
    self.y = y
    self.fontSize = fontSize
    self.color = color
    self.center = Center

  def set_text(self): #Function to set text
      pygame.init()
      font = pygame.font.Font(self.font, self.fontSize)  #sets the font and the size for the text
      text = font.render(self.string, True, (self.color))  #renders the text and sets its color
      textRect = text.get_rect() #Stores the x and y coordinates of the text
      if self.center == None:
        textRect.center = (self.x, self.y) #sets the x and y coordinates for the text 
      else:
        textRect = (self.x, self.y)
      SCREEN.blit(text, textRect)