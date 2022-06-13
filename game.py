from typing import NewType
import pygame, sys, os, random

from pygame.constants import K_RETURN

from settings import *
from os import walk
from pygame import mixer
from map_data import levels
from math import sin



pygame.init()
clock = pygame.time.Clock() 

mixer.music.load("Audio/gameplay.mp3")
mixer.music.play(-1)

Player_score = 0
Background_speed = 0

entered = False

x = 0

if character_used == 'Alex Sprites':
  rect_width = 65
else:
    rect_width = 90

user_name = ''
base_font = pygame.font.Font(None, 60)

def import_folder(path):
    surface_list = []
    dir_name = os.listdir(path)
    for item in dir_name:
        if item.endswith('.db'):
            os.remove(os.path.join(path, item)) #deletes the files that end with .db
    
    for _,__,img_files in walk(path):
        img_files = sorted(img_files, key=lambda x: x[1], reverse=False) #sorts the images in order
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha() #loads the image
            surface_list.append(image_surf)
    return surface_list

class Level:
    def __init__(self,current_level,change_score, change_health, surface, create_overworld):
        
        #user interface
        self.change_score = change_score
        self.display_surface = surface 

        #audio
        self.mob_death = pygame.mixer.Sound('audio/mob death.mp3')
        self.coin_collect = pygame.mixer.Sound('audio/coin.wav')
        self.powerup = pygame.mixer.Sound('audio/powerup.wav')
        self.victory = pygame.mixer.Sound('audio/victory.wav')

        #overwoeld setup
        self.current_level = current_level
        self.create_overworld = create_overworld
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        self.world_shift = 0

        #terrain setup
        terrain_layout = csv_data(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #coins setup
        coins_layout = csv_data(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        #powerup setup
        powerups_layout = csv_data(level_data['powerups'])
        self.powerups_sprites = self.create_tile_group(powerups_layout, 'powerups')

        #constraint_layout
        constraint_layout = csv_data(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        #mob setup
        mob_layout = csv_data(level_data['enemies'])
        self.mob_sprites = self.create_tile_group(mob_layout, 'enemies')

        #traps setup
        traps_layout = csv_data(level_data['traps'])
        self.traps_sprites = self.create_tile_group(traps_layout, 'traps')

        #player setup
        player_layout = csv_data(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        self.change_health = change_health

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout): #loops through the rows in layout (data)
            for col_index, val in enumerate(row): #loops though the data in the rows
                if val != '-1':
                    #setting the coordinates
                    x = col_index * tile_size                    
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = cut_tiles('map/tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x,y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'powerups':
                        if val == '0':
                            tile_surface = pygame.image.load("map/powerups/jump_boost.png")
                            value = "jump boost"
                        elif val == '1':
                            tile_surface = pygame.image.load("map/powerups/Health.png")
                            value = "health"
                        elif val == '2':
                            tile_surface = pygame.image.load("map/powerups/Speed_boost.png")
                            value = "speed boost"

                        sprite = Powerups(tile_size, x,y, tile_surface, value)
                        sprite_group.add(sprite) #adds the sprite to the spite groups
                    
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x,y,'Coins Sprites/Gold', 10)
                        if val == '1':
                            sprite = Coin(tile_size, x,y,'Coins Sprites/Silver', 5)
                        sprite_group.add(sprite)
                    
                    if type == 'enemies':
                        sprite = Mob(tile_size, x,y)
                        sprite_group.add(sprite)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x,y)
                        sprite_group.add(sprite)
                    
                    if type == 'traps':
                        if val == '0':
                            tile_surface = pygame.image.load('map/spikes.png')
                        sprite = StaticTile(tile_size, x,y, tile_surface)
                        sprite_group.add(sprite)

        return sprite_group

    def mob_borders_collision(self):
        for mob in self.mob_sprites.sprites(): #loops for each mob in the sprite group
            if pygame.sprite.spritecollide(mob, self.constraint_sprites, False): #checks if the mob collides with the constraints
                mob.reverse()
    
    def player_setup(self, layout, change_health):
        #reading the data from the csv file
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y), change_health)
                    self.player.add(sprite)
                if val == '1':
                    finish_line = pygame.image.load('map/house1.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,finish_line)
                    self.goal.add(sprite)

    def scroll_x(self):
        global Background_speed
        player = self.player.sprite
        player_x = player.rect.centerx #gets the centre of the x position
        direction_x = player.direction.x #gets the direction the player will move in

        if player_x < WIDTH /4 and direction_x < 0:
            self.world_shift = player.player_speed + 8 #sets map scrolling speed
            player.speed = 0
            if player.player_speed > 1:
                Background_speed = 1.5
            else:
                Background_speed =0.5
        elif player_x > WIDTH - (WIDTH / 2) and direction_x > 0:
            self.world_shift = -player.player_speed - 8 #sets map scorlling speed in the opposite direction
            player.speed = 0
            if player.player_speed > 1:
                Background_speed =-1.5
            else:
                Background_speed =-0.5
        else:
            self.world_shift = 0
            player.speed = 8
            Background_speed = 0
    
    def collisions(self):
        global Health
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites(): #cycles through all the tiles that the player can collide with
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0: #checks if the player is moving left
                    player.collision_rect.left = sprite.rect.right

                elif player.direction.x > 0: #checks if the player is moving right
                    player.collision_rect.right = sprite.rect.left

        player.apply_gravity()
        
        #checks if the player has fallen of the map
        if player.direction.y > 40:
            self.change_health(-5)

        for sprite in self.terrain_sprites.sprites(): #cycles through all the tiles that the player can collide with
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0: #checks if the player is going down
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0 #cancels out the gravity when the player is standing still   
                    player.on_ground = True

                elif player.direction.y < 0: #checks if the player is going up
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0 #cancels out any negative y direction movement
                    player.on_celiling = True
        
        

            if player.on_ground == True and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False

    def coins_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True) #checks if the player collides with the coins
        if collided_coins:
            for coin in collided_coins: #checks every coin on the map
                self.coin_collect.play()
                self.change_score(coin.value)

    def mob_collision(self):
        mob_collisons = pygame.sprite.spritecollide(self.player.sprite, self.mob_sprites, False)
        if mob_collisons:
            for mob in mob_collisons:#loops through all mobs on the map
                mob_center = mob.rect.centery
                mob_top = mob.rect.top
                player_bottom = self.player.sprite.rect.bottom

                if mob_top < player_bottom < mob_center and self.player.sprite.direction.y >= 0:#checks if tha player is moving down on mob
                    self.mob_death.play()
                    mob.kill()
                    self.player.sprite.direction.y = -17 #makes the character jump
                    self.change_score(15)
                else:
                    self.player.sprite.get_damage()

    def traps_collision(self):
        traps_collisons = pygame.sprite.spritecollide(self.player.sprite, self.traps_sprites, False)
        if traps_collisons:
            for traps in traps_collisons:
                self.player.sprite.get_damage()

    def powerups_collision(self):
        player = self.player.sprite
        powerup_collisons = pygame.sprite.spritecollide(self.player.sprite, self.powerups_sprites, True)
        if powerup_collisons:
            for powerup in powerup_collisons:
                self.powerup.play() #plays sound effect
                #checking type of powerup
                if powerup.value == "health":
                    self.change_health(+1)
                elif powerup.value == "speed boost":
                    player.change_speed(1.3)
                elif powerup.value == "jump boost":
                    player.change_jump_speed(-25)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):#checks if the player collided with the end point
            self.victory.play()
            self.create_overworld(self.current_level, self.new_max_level)

    def run(self):
        
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        self.powerups_sprites.draw(self.display_surface)
        self.powerups_sprites.update(self.world_shift)

        self.mob_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.mob_sprites.draw(self.display_surface)
        self.mob_borders_collision()

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.player.update()
        self.collisions()
        self.player.draw(self.display_surface)

        self.traps_collision()
        self.traps_sprites.update(self.world_shift)
        self.traps_sprites.draw(self.display_surface)
        
        self.scroll_x()
        self.check_win()

        self.coins_collisions()
        self.mob_collision()
        self.powerups_collision()

class Player(pygame.sprite.Sprite): #inherits from sprite.sprite
    def __init__(self, pos, change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 1
        self.animation_speed = 0.35
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft = pos)

        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.player_speed = 1
        self.jump_speed = -20
        self.collision_rect = pygame.Rect(self.rect.topleft, (rect_width , self.rect.height)) 

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False

        self.change_health = change_health
        self.invincible = False
        self.invincible_duration = 1200
        self.damage_time = 0
 
    def import_character_assets(self):
        character_path = f"{character_used}/"
        self.animations = {'idle': [], 'run':[], 'jump':[], 'dead':[]}
        keys = pygame.key.get_pressed()        

        for animation in self.animations.keys(): #cycles through the variables in the dictionary
            full_path = character_path + animation #add the directory of the images
            self.animations[animation] = import_folder(full_path)
   
    def animate(self):
        animation = self.animations[self.status] # selects which animation to load from the dictionary 
        
        #increments the index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        if self.facing_right: #checks which direction the character is facing
            image = animation[int(self.frame_index)]
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            image = pygame.transform.flip(animation[int(self.frame_index)], True, False)#flips the image
            self.rect.bottomright = self.collision_rect.bottomright
        self.image = image

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha) #sets the player to transparent
        else:
            self.image.set_alpha(255) 

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = self.player_speed
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -self.player_speed
            self.facing_right = False
        else:
                self.direction.x = 0
        if keys[pygame.K_w] and self.on_ground or keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_speed #makes the character jump
            
    def get_status(self):
        #setting the status based on the movement
        if self.direction.y != self.gravity and self.direction.y != 0 or self.direction.y < 0:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity #makes the player experience gravity
        self.collision_rect.y += self.direction.y

    def get_damage(self):
        if not self.invincible:
            self.change_health(-1)
            self.invincible = True
            self.damage_time = pygame.time.get_ticks()#gets the time when the player recieved damage
            self.player_speed = 1
            self.jump_speed = - 20

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.damage_time >= self.invincible_duration: #checks if the cooldown is over
                self.invincible = False

    def change_speed(self, value):
        self.player_speed = value

    def change_jump_speed(self, value):
        self.jump_speed = value

    def wave_value(self):
        value = sin(pygame.time.get_ticks()) #gets the x coordinates of the wave
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()

class Tile(pygame.sprite.Sprite): #inhertis from sprite.sprite
    def __init__(self,size, x,y): #position and size of each tile
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y)) #gets the rectangler shape of the tile

    def update(self,x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y)) #centers the image on the surface

class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size, x,y)
        self.frames = import_folder(path) #gets the images to display
        self.frame_index = 0
        self.image = self.frames[self.frame_index] #displays the images
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]#displayes the image
    
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

class Coin(AnimatedTile):
    def __init__(self,size, x, y, path, value):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))#sets the poisition to be centered
        self.value = value

class Powerups(StaticTile):
    def __init__(self,size,x,y,surface, value):
        super().__init__(size,x,y,surface)
        self.value = value
               
class Mob(AnimatedTile):
    def __init__(self,size, x, y):
        super().__init__(size,x,y, 'mobs/male/walk')
        self.rect.y += size - self.image.get_size()[1] +1.8 #sets the position of the sprite
        self.speed = random.randint(2,5)

    def move(self):
        self.rect.x += self.speed

    def reverse_img(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)#flips the image

    def reverse(self):
        self.speed *= -1 #flips the direction of the mob
    
    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_img()

class Game:
    def __init__(self):
        self.health = 4
        self.score = 0
        
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, SCREEN, self.create_level)
        self.status = 'overworld'

        self.elements = Elements(SCREEN)

    def change_score(self, amount):
        self.score += amount

    def change_health(self, ammount):
        self.health += ammount


    def check_game_over(self):
        if self.health <= 0:
            self.health = 4
            self.score = 0

    def get_score(self):
        return self.score

    def create_level(self, current_level):
        self.level = Level(current_level, self.change_score, self.change_health, SCREEN, self.create_overworld) #loads the level
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level: #ensures that the player only can access unlocked levels
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, SCREEN, self.create_level)
        self.status = 'overworld'
        self.health = 4 #resets the health to 4

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.elements.show_health(self.health)
            self.elements.show_score(self.score)
            self.check_game_over()

class Elements:
    def __init__(self, surface):
        self.display_surface = surface
    
    def show_health(self,current):
        #checks the health status
        if current == 8:
            self.health_bar = pygame.image.load('health bar/8 health.png')
        elif current == 7:
            self.health_bar = pygame.image.load('health bar/7 health.png')
        elif current == 6:
            self.health_bar = pygame.image.load('health bar/6 health.png')
        elif current == 5:
            self.health_bar = pygame.image.load('health bar/5 health.png')
        elif current == 4:
            self.health_bar = pygame.image.load('health bar/4 health.png')
        elif current == 3:
            self.health_bar = pygame.image.load('health bar/3 health.png')
        elif current == 2:
            self.health_bar = pygame.image.load('health bar/2 health.png')
        elif current == 1:
            self.health_bar = pygame.image.load('health bar/1 health.png')
        else:
            self.health_bar = pygame.image.load('health bar/0 health.png')
            game_over()
        self.health = current

        self.display_surface.blit(self.health_bar, (1060,63))

    def show_score(self, amount):
        #creating text
        score_text = create_text('Score: ', 'fonts/American Captain.ttf', 70, 70, 40, WHITE) 
        score_num = create_text(str(amount), 'fonts/American Captain.ttf', 120, 50, 40, WHITE, False)
        #bliting the text
        score_text.set_text()
        score_num.set_text()

class Overworld:
    def __init__ (self, start_level, max_level, surface, create_level):

        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        #movement
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.moving = False

        # sprites
        self.setup_stages()
        self.setup_icon()
            
    def setup_stages(self):
        self.stages = pygame.sprite.Group()
        for index, stage_data in enumerate(levels.values()): #reads the data from thr game data file
            if index <= self.max_level: #checks if the player has unlocked the level
                stage_sprite = Stage(stage_data['stage_pos'], 'unlocked', self.speed, stage_data['stage_graphics'])
            else:
                stage_sprite = Stage(stage_data['stage_pos'], 'locked', self.speed, stage_data['stage_graphics'])
            self.stages.add(stage_sprite)
    
    def draw_paths(self):
        if self.max_level > 0:
            points = [
                stage['stage_pos'] for index, stage in enumerate(levels.values()) 
                if index <= self.max_level]  #gets the stage position from game data only if the index is <= max_level
            pygame.draw.lines(self.display_surface,'#0C6A17', False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.stages.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next') #passes the next stage to visit
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous') #passes the next stage to visit
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level) #passes the level to load

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed #sets the player at the center of the stage
            target_stage = self.stages.sprites()[self.current_level]
            if target_stage.detection_zone.collidepoint(self.icon.sprite.pos): #checks if the player collides with the center of the stage
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.stages.sprites()[self.current_level].rect.center) #position of player where he is suppose to be at the start

        if target == 'next':
            end = pygame.math.Vector2(self.stages.sprites()[self.current_level + 1].rect.center) #position of player where he would be going to
        else:
            end = pygame.math.Vector2(self.stages.sprites()[self.current_level - 1].rect.center) #position of player where he would be going to

        return (end - start).normalize()

    def run(self):
        self.draw_paths()
        self.stages.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.stages.update()

class Stage(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()

        if status == 'unlocked':
            self.status = 'unlocked'
        else:
            self.status = 'locked'
        
        self.image = pygame.image.load(path)

        if self.status != 'unlocked':
            tint_surf = self.image.copy() #creates a copy of self.image
            tint_surf.fill(BLACK, None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0,0))

        self.rect = self.image.get_rect(center = pos)

        #collisoin zone
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(f'{character_used}/idle/1.png').convert_alpha() #draws the character

        #resizing the image
        if character_used == 'Alex Sprites':
            self.image = pygame.transform.scale(self.image, (43,68))
        else:
            self.image = pygame.transform.scale(self.image, (62,68))
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos


game = Game()

def main_game():
  running = True
  bg = pygame.image.load('map/game_background.png').convert()
  global x
  while running:
    SCREEN.fill(WHITE)
    Clock.tick(FPS)
    
    if game.status == 'overworld':
        background = pygame.image.load('backgrounds/overworld.png')
        SCREEN.blit(background, (0,0))
    else:
        #scrolling background
        rel_x = x % bg.get_rect().width
        SCREEN.blit(bg, (rel_x - bg.get_rect().width, 0))
        if rel_x < WIDTH:
            SCREEN.blit(bg, (rel_x, 0))
        x += Background_speed

    game.run()
    mute_button()


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()
  pygame.quit()

def quit():
    pygame.quit()
    sys.exit()

def game_over():
    running = True
    global user_name, entered
    final_username = ''
    input_rect = pygame.Rect(450,350, 100, 64)
    game_over_text = create_text('Game Over', 'fonts/American Captain.ttf', WIDTH /2 + 7,100, 120, WHITE)
    Enter_name = create_text('enter your name', 'fonts/American Captain.ttf', WIDTH /2 + 7, 300, 60, WHITE)
    Quit = create_button("Exit to desktop",500,550,320,50, GREEN, quit, 40, 'fonts/theboldfont.ttf', DARK_GREEN)
    instruction = create_text('Press enter once your done', 'fonts/American Captain.ttf', 650, 500, 60, WHITE)

    #loading the music track
    mixer.music.load("Audio/game_over.mp3")
    mixer.music.play(-1)
    

    while running:
        SCREEN.fill(BLACK)
        mute_button()
        #creating the text
        text_surface = base_font.render(user_name, True, WHITE)
        input_rect.w = max(400, text_surface.get_width() + 10) #creating the width of the box

        game_over_text.set_text()
        Enter_name.set_text()
        Quit.button()
        instruction.set_text()

        SCREEN.blit(text_surface,(input_rect.x + 10, input_rect.y + 10))

        keys = pygame.key.get_pressed()
            
        #drawing the box
        if not entered:
            pygame.draw.rect(SCREEN, BLUE, input_rect, 2)
            if len(final_username) < 4 and keys[K_RETURN]: #checks if the username length is valid
                pygame.draw.rect(SCREEN, RED, input_rect, 2)     
        else:
            pygame.draw.rect(SCREEN, GREEN, input_rect, 2)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if not entered:
                        user_name = user_name[:-1]
                    else:
                        user_name = user_name
                        final_username = user_name
                elif entered:
                    final_username = user_name

                elif event.key == pygame.K_RETURN:
                    final_username = user_name
                    if not entered:
                        if len(user_name) >=4:
                            f = open('Leaderboard.txt', 'r')
                            temp = eval(f.read())
                            f.close()
                            leaderboard_sorted = sorted(temp, key=lambda x: x[1], reverse=True)
                            player_stats = [final_username, game.get_score()]
                            leaderboard_sorted.append(player_stats)
                            list = str(leaderboard_sorted)


                            f = open('Leaderboard.txt', 'w')
                            f.write(list)
                            f.close()
                            entered = True
                else:
                    user_name += event.unicode
        pygame.display.update()
    pygame.quit()

main_game()