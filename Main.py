# Author : Adrien Pillou
# Date : 10/31/2020
# Description : Python port of Space Invaders arcade version

# https://www.classicgaming.cc/classics/space-invaders/play-guide

import pygame
import random
import math
import json
import os
import time

from Alien import alien
from Player import player
from Shelter import Shelter
from Alarm import alarm
from Particle import Particle
from Spritesheet import spritesheet
from Object import Object
from AnimatedObject import AnimatedObject
from Ship import Ship
from Save import Save

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def spawn_aliens(columns=11, rows=5):
    aliens = []
    padding = 0
    alien_type = 1
    group_width = columns * 16 + (columns-1)* padding
    group_height = rows * 8 + (rows-1)*padding
    for j in range(rows):
        if j == 0:
            alien_type = 'A'
        if j == 1 or j == 2:
            alien_type = 'B'
        if j == 3 or j == 4:
            alien_type = 'C'
        frames = [sheet.get_sprite(f'ALIEN-{alien_type}-0'), sheet.get_sprite(f'ALIEN-{alien_type}-1')]
        for i in range(columns):
            new_alien = alien(f"Alien {i}{j}", "ENEMY", alien_type)
            new_alien.set_images(frames)
            new_alien.set_position(((WIDTH/2 - group_width/2) + (i*16), (HEIGHT/6-group_height/2)+ (j+1) * 12))
            aliens.append(new_alien)
    alien_move_alarm = alarm(alien_movement_delay)
    return aliens

def spawn_mystery_ship():
    global mystery_ship
    mystery_ship = Ship("Mystery Alien "+str(score))
    mystery_ship.set_image(sheet.get_sprite('MYSTERY-ALIEN'))
    mystery_ship.tint((255, 0, 0))
    mystery_ship.direction = 2*random.randint(0, 1)-1
    if mystery_ship.direction == 1:
        mystery_ship.set_position((-16, 16))
    elif mystery_ship.direction == -1:
        mystery_ship.set_position((WIDTH+16, 16))

def spawn_shelters(amount):
    shelters = []
    shelter_width = 24
    x = 0
    y = HEIGHT-64
    image = sheet.get_sprite("SHELTER")
    for i in range(amount):
        x = (i+1)*WIDTH/(amount+1)-shelter_width/2
        new_shelter = Shelter(f"Barrier {i}", "PLAYER")
        new_shelter.set_position((x, y))
        new_shelter.set_image(image)
        new_shelter.tint((0, 255, 0))
        shelters.append(new_shelter)
    return shelters

def shoot(position, velocity):
    instance = AnimatedObject("bullet", "DEFAULT")
    instance.set_position(position)
    instance.set_velocity(velocity)
    bullets.append(instance)
    return instance

def update_aliens():
    # Invaders movements
    if alien_move_alarm.is_ended():
        # Difficulty curve
        x = len(aliens)
        alien_movement_delay = .2+ (2*math.log10(x))/10
        alien_move_alarm.reset(alien_movement_delay)
        alien_move_alarm.start()

        if check_aliens_can_move():
            move_aliens()
        else:
            move_aliens_down()
    
    if check_aliens_collision():
        game_over()

    # Shooting mechanics
    if(alien_shoot_alarm.is_ended()):
        alien_shoot_alarm.reset(1)
        alien_shoot_alarm.start()
        random_alien = random.choice(aliens)
        while random_alien == None:
            random_alien = random.choice(aliens)
        instance = shoot((random_alien.get_x() + random_alien.width/2, random_alien.get_y()), (0, 100))
        instance.set_tag("ENEMY")
        random_type_index = random.randint(0, 2)
        projectile_type = chr(65+random_type_index)
        frames = [sheet.get_sprite(f"PROJECTILE-{projectile_type}-0"), sheet.get_sprite(f"PROJECTILE-{projectile_type}-1"), sheet.get_sprite(f"PROJECTILE-{projectile_type}-2"), sheet.get_sprite(f"PROJECTILE-{projectile_type}-2")]
        instance.set_images(frames)
        instance.set_animation_speed(25)
    
    global ship_score_threshold
    if score >= ship_score_threshold and not isinstance(mystery_ship, Ship) and score!=0:
        spawn_mystery_ship()
        ship_score_threshold += random.randint(50, 500)

def move_aliens_down():
    vertical_step = 8
    global alien_direction
    alien_direction *= -1
    for alien in aliens:
            alien.next_frame()
            alien.set_position((alien.get_x(), alien.get_y()+vertical_step))

def move_aliens():
    horizontal_step = 8
    for alien in aliens:
        new_position = (alien.get_x() + (alien_direction * horizontal_step), alien.position[1])
        alien.set_position(new_position)
        alien.next_frame()

def check_aliens_can_move():
    global alien_direction
    horizontal_step = 8
    x_positions = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208]
    for alien in aliens:
        next_position = alien.get_x() + alien_direction * horizontal_step
        if not next_position in x_positions:
                return False
    return True

def check_aliens_collision():
    for alien in aliens:
        for shelter in shelters:
            if check_collision(alien.get_rect(), shelter.get_rect()):
                return True
            elif check_collision(alien.get_rect(), player.get_rect()):
                return True
    return False
       
def draw_aliens():
    for alien in aliens:
        if(alien != None):
            alien.draw(base_surface)

def update_ship():
    global mystery_ship
    x = mystery_ship.get_x()+mystery_ship.direction*100*dt
    y = mystery_ship.get_y()
    if x < -32 or x > WIDTH+32:
        mystery_ship = None
    else:
        mystery_ship.set_position((x, y))
        mystery_ship.draw(base_surface)

def update_projectiles():
    for bullet in bullets:
        bullet.set_position((bullet.get_x() + bullet.velocity[0]*dt, bullet.get_y() + bullet.velocity[1]*dt))
        bullet.draw(base_surface)
        if(isinstance(bullet, AnimatedObject)):
            bullet.animate(dt)
        if(bullet.get_y()<=0 or bullet.get_y() > HEIGHT - 15 - bullet.height):
            if(bullet in bullets):
                create_particle('IMPACT', bullet.position, .2)
                bullets.remove(bullet)
        
        # Checking collision with aliens
        for alien in aliens:
            if(alien == None):
                continue
            if bullet.tag == "PLAYER" and check_collision(bullet.get_rect(), alien.get_rect()):
                play_sound_effect("INVADER KILLED", .1)
                create_particle('EXPLOSION', alien.position, .2)
                if alien in aliens:
                    aliens.remove(alien)
                bullets.remove(bullet)
                global score
                destroyed_alien_type = alien.get_type()
                if alien.type == 'A':
                    score += 30
                elif alien.type == 'B':
                    score += 20
                elif alien.type == 'C':
                    score += 10
                break

        # Checking collision with shelters
        for shelter in shelters:
            if check_collision(bullet.get_rect(), shelter.get_rect()):
                shelter.hp-=1
                if(shelter.hp<=0):
                    shelters.remove(shelter)
                create_particle('IMPACT', bullet.position, .2)
                bullets.remove(bullet)
                break

        # Checking collision with other bullets
        for other_bullet in bullets:
            if bullet.tag == other_bullet.tag or other_bullet == bullet:
                continue
            if check_collision(bullet.get_rect(), other_bullet.get_rect()):
                bullets.remove(other_bullet)
                if bullet in bullets:
                    bullets.remove(bullet)
                create_particle('IMPACT', other_bullet.position, .2)
        
        # Collision with a ship
        global mystery_ship
        if(not mystery_ship is None):
            if bullet.tag == "PLAYER" and check_collision(mystery_ship.get_rect(), bullet.get_rect()):
                bullets.remove(bullet)
                create_particle('EXPLOSION', mystery_ship.position,.2)
                mystery_ship = None
                score += 100
                
        # Checking collision with the player ship
        if bullet.tag == "ENEMY" and check_collision(player.get_rect(), bullet.get_rect()):
            bullets.remove(bullet)
            global lives
            if(lives>0):
                destroy_player()
            else:
                game_over()

def create_particle(sheet_id:str, position:tuple, lifetime):
    particle = Particle(f"Particle-{len(particles)}", "DEFAULT", lifetime)
    particle.set_image(sheet.get_sprite(sheet_id))
    particle.set_position(position)
    particles.append(particle)

def draw_shelters():
    for shelter in shelters:
        shelter.draw(base_surface)

def draw_particles():
    for p in particles:
        p.update(dt)
        p.draw(base_surface)
        if(p.lifetime <= 0):
            particles.remove(p)

def draw_interface():
    # Drawing lives stocks
    for l in range(lives):
        stock_object = Object(f"Stock-{l}", "UI")
        stock_object.set_image(sheet.get_sprite('PLAYER'))
        stock_object.set_position((16+(stock_object.width+2)*l,HEIGHT-10))
        interface_elements.append(stock_object)
    
    # Drawing all interface elements
    for element in interface_elements:
        element.draw(base_surface)
    interface_elements.clear()

def update_player():
    keys = pygame.key.get_pressed()
    if(player.can_move):
        if keys[pygame.K_RIGHT]:
            if(player.get_x() + player.width < WIDTH):
                player.move(1, 0, player.speed*dt)
        if keys[pygame.K_LEFT]:
            if(player.get_x() >= 0):
                player.move(-1, 0, player.speed*dt)

        if(player.get_can_shoot() and player.is_shooting):
            play_sound_effect("PLAYER SHOOT", .1)
            player.can_shoot = False
            player.shooting_alarm.reset(player.rate_of_fire)
            player.shooting_alarm.start()
            instance = shoot((player.get_x() + player.width/2, player.get_y()-2), (0, -256))
            instance.add_image(sheet.get_sprite('PLAYER-PROJECTILE'))
            instance.set_tag("PLAYER")

def destroy_player():
    global lives
    lives-=1
    play_sound_effect("PLAYER KILLED", .1)
    '''player.can_move = False
    frametime = .2
    player.set_image(sheet.get_sprite('PLAYER-EXPLOSION-0'))
    player.set_image(sheet.get_sprite('PLAYER-EXPLOSION-1'))
    player.set_image(sheet.get_sprite('PLAYER-EXPLOSION-0'))
    player.set_image(sheet.get_sprite('PLAYER-EXPLOSION-1'))
    player.can_move = True
    player.set_image(sheet.get_sprite('PLAYER'))'''
    player.set_position((WIDTH/2-player.width/2, player.get_y()))

def update(dt):
    global base_surface
    # Setting the base surface to a blak one with base resolution
    base_surface = pygame.surface.Surface((224, 256))
    screen.fill(background_colour)
    update_player()
    player.draw(base_surface)
    if(len(aliens)>0):
        update_aliens()
        draw_aliens()
    else:
        start_game()
    if mystery_ship != None:
        update_ship()
    update_projectiles()
    draw_shelters()
    draw_particles()
    
    # Drawing the game interface
    draw_text((0, 0), f"score<1> hi-score")
    draw_text((12, 10), zero_fill(score, 4))
    draw_text((60, 10), zero_fill(highscore, 4))
    draw_text((6,HEIGHT-10), str(lives))
    draw_text((WIDTH-60, HEIGHT-10), f"CREDIT {zero_fill(coins, 2)}")
    draw_interface()
    pygame.draw.line(base_surface,(0, 255, 0) , (0, HEIGHT-12), (WIDTH, HEIGHT-12))
    base_surface = pygame.transform.scale(base_surface, GAME_RESOLUTION)
    screen.blit(base_surface, (0, 0))
    pygame.display.update()
   
def check_collision(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    if(x1 >= x2 and x1 <= x2 + w2):
        if(y1 >= y2 and y1 <= y2 + h2):
            return True
    if(x2 >= x1 and x2 <= x1 + w1):
        if(y2 >= y1 and y2 <= y1 + h1):
            return True
    return False

def play_sound_effect(effect_name, volume = 1):
    sound_effect_file_name = sound_effects.get(effect_name)
    if sound_effect_file_name is None:
        print(f"Sound effect {effect_name} does not exists !")
        return
    sound_effect_path = os.path.join('assets/sounds', sound_effect_file_name)
    sound_effect = pygame.mixer.Sound(sound_effect_path)
    sound_effect.set_volume(volume * GLOBAL_VOLUME)
    sound_effect.play()

def zero_fill(number:int, length:int):
    number_string = str(number)
    number_string = number_string.zfill(length)
    return number_string

def draw_text(position, text):
    (xpos, ypos) = position
    text = text.upper()
    # Converting text to sprites
    for i in range(len(text)):
        if(text[i] in sheet.sprites.keys() or text[i] == "<" or text[i] == ">"):
            char = Object(f"Char {text[i]}", "INTERFACE")
            if text[i] == "<":
                char.set_image(sheet.sprites["LT"])
            elif text[i] == ">":
                char.set_image(sheet.sprites["GT"])
            else:
                char.set_image(sheet.sprites[text[i]])
            char.set_position((xpos + i*6, ypos))
            interface_elements.append(char)

def start_game():
    global aliens, shelters, highscore, coins
    coins -= 1
    highscore = save_manager.get_int_value("hi-score")
    coins = save_manager.get_int_value("credit")
    aliens  = spawn_aliens()
    shelters = spawn_shelters(4)

def game_over():
    global lives, score, highscore, coins
    if(score>highscore):
        #write_save_file({"hi-score":score, "credit":coins})
        save_manager.set_value('hi-score', score)
        save_manager.set_value('credit', coins)
        highscore = score
    else:
        save_manager.set_value('credit', coins)
    score = 0
    lives = 3
    bullets = []
    player.set_position((WIDTH//2-player.width//2, HEIGHT-32))
    start_game()

def write_save_file(data):
    save_manager.save(data)

def load_save_file():
    save_manager.load()

# Constants
WIDTH = 224
HEIGHT = 256 
TARGET_FPS = 120
GLOBAL_VOLUME = .1
RESOLUTION_SCALER = 3
GAME_RESOLUTION = (WIDTH*RESOLUTION_SCALER, HEIGHT*RESOLUTION_SCALER)

pygame.init()

# Sound related stuff
pygame.mixer.pre_init(44100, -16, 2, 32)
pygame.mixer.set_num_channels(32)
sound_effects = {}
sound_effects["PLAYER SHOOT"] = "shoot.wav"
sound_effects["INVADER KILLED"] = "invaderkilled.wav"
sound_effects["PLAYER KILLED"]=  "explosion.wav"

run = True

alien_shoot_alarm = alarm(3)
alien_move_alarm = alarm(0)
alien_movement_delay = .5
interface_elements = []

sheet = spritesheet(os.path.join('assets', 'spritesheet.png'))
sheet.add_descriptive(os.path.join('assets', 'spritesheet.xml'))
sheet.set_color_to_alpha((0, 0, 0))
sheet.slice_sprites()

# Global variables
global save_manager
save_manager = Save("save.json")
save_manager.set_default_object({'hi-score':0, 'credit':0})
save_manager.load()

global highscore
highscore = 0 
global score
score = 0
global ship_score_threshold
ship_score_threshold = random.randint(100, 500)
global lives
lives = 3
global coins
coins = 0
mystery_ship = None

player = player("player", "PLAYER")
player.set_image(sheet.sprites['PLAYER']) 
player.set_position((WIDTH//2-player.width//2, HEIGHT-32))
player.tint((0, 255, 0))

bullets = []
aliens = []
particles = []

start_game()
global alien_direction
alien_direction = 1
shelters = spawn_shelters(4)
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centering the window on the screen (SDL flag ?)
background_colour = (0, 0, 0)

dt = 1/TARGET_FPS
screen = pygame.display.set_mode(GAME_RESOLUTION)
global base_surface
base_surface = pygame.Surface((WIDTH, HEIGHT))

icon = pygame.image.load(os.path.join('assets', 'icon32.png'))
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")

while run:
    dt = clock.tick(TARGET_FPS) / 1000
    update(dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_manager.set_value('hi-score', highscore)
            save_manager.set_value('credit', coins)
            run = False
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                player.is_shooting = True
            if event.key == pygame.K_c:
                if(coins<99):
                    coins += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.is_shooting = False

