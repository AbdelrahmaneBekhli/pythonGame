from turtle import width
from settings import *
import pygame, sys
from pygame.locals import *
from pygame import mixer

pygame.init()

#setting up some global variables
alex_selection_count = 0
amy_selection_count = 0
Amy = False
Alex = False

selected = False

mixer.music.load("Audio/background.mp3")
mixer.music.play(-1)

def quitGame(): #Function to quit the game
  pygame.quit()
  sys.exit()

def controls(): #instructions screen

  QUIT_BUTTON = create_button("X",WIDTH/30,HEIGHT/15,60,75, GREEN, main_menu, 70, 'fonts/theboldfont.ttf', DARK_GREEN)
  Title_shadow = create_text('Game controls', 'fonts/American Captain.ttf', (WIDTH/2) + 7, (HEIGHT/6.3) + 5, 120, BLACK)
  Title = create_text('Game controls', 'fonts/American Captain.ttf', (WIDTH/2),(HEIGHT/6.3), 120, WHITE)

  #setting up the text
  Overworld_txt = create_text('Overworld:', 'fonts/American Captain.ttf', 50,250, 60, WHITE, False)
  Overworld_d_key = create_text('d - Move to next level', 'fonts/American Captain.ttf', 120,320, 50, WHITE, False)
  Overworld_a_key = create_text('a - Move to previous level', 'fonts/American Captain.ttf', 120,380, 50, WHITE, False)
  Overworld_space_key = create_text('Space bar - Enter level', 'fonts/American Captain.ttf', 120,440, 50, WHITE, False)

  game_txt = create_text('Gameplay:', 'fonts/American Captain.ttf', 800,250, 60, WHITE, False)
  game_d_key = create_text('d - Move right', 'fonts/American Captain.ttf', 870,320, 50, WHITE, False)
  game_a_key = create_text('a - Move left', 'fonts/American Captain.ttf', 870,380, 50, WHITE, False)
  game_w_key = create_text('w / Space bar - Jump', 'fonts/American Captain.ttf', 870,440, 50, WHITE, False)
  

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    SCREEN.fill(NAVY)
    mute_button()
    QUIT_BUTTON.button()
    
    #blitting text on screen
    Title_shadow.set_text()
    Title.set_text()

    Overworld_txt.set_text()
    Overworld_d_key.set_text()
    Overworld_a_key.set_text()
    Overworld_space_key.set_text()

    game_txt.set_text()
    game_d_key.set_text()
    game_a_key.set_text()
    game_w_key.set_text()

    pygame.display.update()
  pygame.quit()

def credits(): #credits
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
 

    SCREEN.fill(DARK_BLUE)#fills the screen with dark blue background
    w_center = WIDTH/2 #finds the centre of the horizantal screen
    h_top = HEIGHT/7 #finds the centre of the vertical screen

    Title_shadow = create_text('Credits', 'fonts/American Captain.ttf', w_center + 7, h_top + 5, 120, BLACK )# sets the title shadaw
    Title = create_text('Credits', 'fonts/American Captain.ttf', w_center,h_top, 120, WHITE )#sets the title of the screen
    #setting the buttons
    QUIT_BUTTON = create_button("X",WIDTH/30,HEIGHT/15,60,75, GREEN, main_menu, 70, 'fonts/theboldfont.ttf', DARK_GREEN)
    #setting the credits
    Author = create_text('Game made by: Abdelrahmane', 'fonts/arial_narrow_7.ttf', w_center, 250, 50, WHITE )
    soundtrack = create_text('Music tracks by: Alexander Nakarada,', 'fonts/arial_narrow_7.ttf', w_center, 350, 50, WHITE )
    artist2 = create_text('Otto Halmén,', 'fonts/arial_narrow_7.ttf', 738, 400, 50, WHITE )
    artist3 = create_text('Babasmas', 'fonts/arial_narrow_7.ttf', 705, 450, 50, WHITE )
    purpose = create_text('Game originally created for A-level 2021-2022 coursework', 'fonts/arial_narrow_7.ttf', w_center, 530, 50, WHITE )
    tool = create_text('Made with Pygame', 'fonts/arial_narrow_7.ttf', 1050, 655, 50, WHITE )


    #bliting all the elemnts to the screen
    QUIT_BUTTON.button()
    mute_button()

    Title_shadow.set_text()
    Title.set_text()
    Author.set_text()
    soundtrack.set_text()
    purpose.set_text()
    tool.set_text()
    artist2.set_text()
    artist3.set_text()

    pygame.display.update()
    if running == False:
      break

def leaderboard(): #leaaderboard
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    SCREEN.fill(DARK_BLUE)
    w_center = WIDTH/2
    h_top = HEIGHT/7

    f = open('Leaderboard.txt', 'r')
    temp = eval(f.read())
    f.close()
    player_count = 0
    player_info = 0
    leaderboard_sorted = sorted(temp, key=lambda x: x[1], reverse=True)
    

    name_axis = 180
    score_axis = 130
    for player in range (0,5):
      for i in range(0, 2):
        font = pygame.font.Font('fonts/American Captain.ttf', 80)  #sets the font and the size for the text
        text = font.render(str(leaderboard_sorted[player_count][player_info]), True, (WHITE))  #renders the text and sets its color
        textRect = text.get_rect() #Stores the x and y coordinates of the text
        if player_info == 0:
          textRect.topleft = (100, name_axis) #sets the x and y coordinates for the text 
        elif player_info == 1:
          textRect.topleft = (1000, score_axis)
        SCREEN.blit(text, textRect)
        player_info = player_info + 1
        if player_info > 1:
          player_info = 0
        name_axis = name_axis + 50
        score_axis = score_axis + 50
      player_count = player_count + 1
   

    
  


    Title_shadow = create_text('Leaderboard', 'fonts/American Captain.ttf', w_center + 7, h_top + 5, 120, BLACK)
    Title = create_text('Leaderboard', 'fonts/American Captain.ttf', w_center,h_top, 120, WHITE)

    QUIT_BUTTON = create_button("X",WIDTH/30,HEIGHT/15,60,75, GREEN, main_menu, 70, 'fonts/theboldfont.ttf', DARK_GREEN)

    QUIT_BUTTON.button()
    mute_button()


    Title_shadow.set_text()
    Title.set_text()




    pygame.display.update()
  pygame.quit()

def game(): #loads the game
 import game

def selection(): #selection screen function/process
  import settings
  global alex_selection_count, amy_selection_count, Amy, Alex, character_used, selected
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  alex = ['main_images/Alex selection.png','main_images/Alex selection hover.png']
  amy = ['main_images/Amy selection.png', 'main_images/Amy selection hover.png']

  
  alex_text = pygame.image.load('main_images/Alex text.png')
  Alex_text_scaled = pygame.transform.scale(alex_text, (140,40))
  amy_text = pygame.image.load('main_images/Amy text.png')
  Amy_text_scaled = pygame.transform.scale(amy_text, (140,40))

  if 200 + 750 > mouse[0] > 750 and 300 + 150 > mouse[1] > 150: #checks if the mouse is hovering over the button
    Alex_hover_img = pygame.image.load('main_images/Alex selection hover.png')
    Alex_hover = pygame.transform.scale(Alex_hover_img, (200, 300))
    SCREEN.blit(Alex_hover,(750,150))
    if click[0] == 1: #checks if the button has been clicked
      Alex = True
      Amy = False

  if Alex == True and Amy == False:
    alex_selection_count = 1
    settings.character_used = "Alex Sprites"
    selected = True

  else:
    alex_selection_count = 0

  if 265 + 250 > mouse[0] > 250 and 300 + 150 > mouse[1] > 150: #checks if the mouse is hovering over the button
    Amy_hover_img = pygame.image.load('main_images/Amy selection hover.png')
    Amy_hover = pygame.transform.scale(Amy_hover_img, (265,300))
    SCREEN.blit(Amy_hover, (250,150))
    if click[0] == 1: #checks if the button has been clicked
      Alex = False
      Amy = True
  if Amy == True and Alex == False:
    amy_selection_count = 1
    settings.character_used = "Amy Sprites"
    selected = True

  else:
      amy_selection_count = 0
      
  character_1 = pygame.image.load(alex[alex_selection_count])
  img_character_1 = pygame.transform.scale(character_1, (200,300))
  SCREEN.blit(img_character_1, (750,150))
  SCREEN.blit(Alex_text_scaled, (790, 455))

  character_2 = pygame.image.load(amy[amy_selection_count])
  img_character_2 = pygame.transform.scale(character_2, (265,300))
  SCREEN.blit(img_character_2, (250, 150))
  SCREEN.blit(Amy_text_scaled, (330,455))

def character_selection(): #Character selection screen
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    w_center = WIDTH/2
    h_top = HEIGHT/7.5

    Title_shadow = create_text('Select your character!', 'fonts/American Captain.ttf', w_center + 5, h_top + 4, 90, GREY) #shadow for the title 
    Title = create_text('Select your character!', 'fonts/American Captain.ttf',  w_center, h_top, 90, WHITE) # title text
    QUIT_BUTTON = create_button("X",WIDTH/30,HEIGHT/15,60,75, GREEN, main_menu, 70, 'fonts/theboldfont.ttf', DARK_GREEN)# quit game button
    lock_character = create_button('Lock in', 480, 580,300,75, GREEN, game, 60, 'fonts/BLACK.ttf', DARK_GREEN)#character lock button
    background = pygame.image.load('backgrounds/Dark forest.png').convert()#imports the background image

    SCREEN.blit(background, (0,0))#displays the background on the screen

    #blitting/calling the functions required
    Title_shadow.set_text()
    Title.set_text()
    mute_button()
    selection()
    QUIT_BUTTON.button()
    if selected == True:
     lock_character.button()

    pygame.display.update()
  pygame.quit()

def main_menu(): #main menu
  running = True

  background = pygame.image.load('backgrounds/Starry night Image.png')
  w_center = WIDTH/2
  h_top = HEIGHT/6.3

  #passing parameters into the classes
  Title_shadow = create_text('The adventures of the lost kid', 'fonts/Gainstone.ttf', w_center + 7, h_top + 5, 90, BLACK) 
  Title = create_text('The adventures of the lost kid', 'fonts/Gainstone.ttf', w_center, h_top, 90, WHITE) 
  Start_BUTTON = create_button("Start game",0,230,1280,30, BLACK, character_selection)
  GAME_CONTROLS_BUTTON = create_button("Game controls",0,260,1280,30, BLACK, controls)
  LEADERBOARD_BUTTON = create_button("Leaderboard",0,290,1280,30, BLACK, leaderboard)
  CREDITS_BUTTON = create_button("Credits",0,320,1280,30, BLACK, credits)
  QUIT_BUTTON = create_button("Quit game",0,350,1280,30, BLACK, quitGame)

  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
    
    SCREEN.blit(background, (0,0))

    #calling the function within the class
    Title_shadow.set_text()
    Title.set_text()
    LEADERBOARD_BUTTON.button()
    GAME_CONTROLS_BUTTON.button()
    CREDITS_BUTTON.button()
    QUIT_BUTTON.button()
    Start_BUTTON.button()
    

    mute_button()

    pygame.display.update()
  pygame.quit()

main_menu()