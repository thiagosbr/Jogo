import random
from pgzero.builtins import Actor, music
import pgzrun
from pygame import Rect  
import math  

WIDTH = 900
HEIGHT = 700
game_state = 'menu' 
congratulations_time = 0 
sound_on = True
HERO_SIZE = 50  
ENEMY_SIZE = 30  
CONQUEST_SIZE = 30
MAP_WIDTH = 800
MAP_HEIGHT = 600
MAP_X = (WIDTH - MAP_WIDTH) // 2  
MAP_Y = (HEIGHT - MAP_HEIGHT) // 2
music.queue('background_music.ogg') 
music.play('background_music.ogg')  
game_over_sound = music 
hero = Actor('hero_idle', (400, 300))
hero_run_frames = [Actor(f'hero_run_{i}', (hero.x, hero.y)) for i in range(1, 5)]
hero.vx = 0
hero.vy = 0
hero.current_frame = 0
hero.frame_counter = 0

enemies = []
enemy_run_frames = []
conquest_frames = [
    Actor('conquest_1', (MAP_X + MAP_WIDTH - 35, MAP_Y + MAP_HEIGHT - 35)),  
    Actor('conquest_2', (MAP_X + MAP_WIDTH - 35, MAP_Y + MAP_HEIGHT - 35)),
    Actor('conquest_3', (MAP_X + MAP_WIDTH - 35, MAP_Y + MAP_HEIGHT - 35))
]
conquest_current_frame = 0
conquest_frame_counter = 0

def update_conquest():
    global conquest_current_frame, conquest_frame_counter
    conquest_frame_counter += 1
    if conquest_frame_counter >= 5:  
        conquest_current_frame = (conquest_current_frame + 1) % len(conquest_frames)
        conquest_frame_counter = 0

def create_enemy():
    x = random.randint(MAP_X + 50, MAP_X + MAP_WIDTH - 50)
    y = random.randint(MAP_Y + 50, MAP_Y + MAP_HEIGHT - 50)
    while math.sqrt((hero.x - x) ** 2 + (hero.y - y) ** 2) < 200:  
        x = random.randint(MAP_X + 50, MAP_X + MAP_WIDTH - 50)
        y = random.randint(MAP_Y + 50, MAP_Y + MAP_HEIGHT - 50)

    enemy_frames = [Actor(f'enemy_run_{i}', (x, y)) for i in range(1, 7)]  
    enemy_data = {'actor': enemy_frames, 'current_frame': 0, 'frame_counter': 0}
    enemies.append(enemy_data)


def update_conquest():
    global conquest_current_frame, conquest_frame_counter
    conquest_frame_counter += 1
    if conquest_frame_counter >= 3:  
        conquest_current_frame = (conquest_current_frame + 1) % len(conquest_frames)
        conquest_frame_counter = 0

def start_game():
    global game_state
    game_state = 'playing'
    hero.x = 400
    hero.y = 300
    for _ in range(5):
        create_enemy()
game_over_time = 0 
congratulations_time = 0 
def update():
    
    if game_state == 'playing':
        update_hero()
        update_enemies()
        update_conquest()
        check_collisions()  
    elif game_state == 'game_over':
        global game_over_time 
        game_over_time += 1  
        if game_over_time >= 300: 
            game_over_time = 0
            reset_game()
    elif game_state == 'congratulations':
        global congratulations_time
        congratulations_time += 1  
        if congratulations_time >= 300:  
            congratulations_time = 0
            reset_game()  

def update_hero():
    hero.x += hero.vx
    hero.y += hero.vy
    hero.x = max(MAP_X + HERO_SIZE // 2, min(MAP_X + MAP_WIDTH - HERO_SIZE // 2, hero.x))
    hero.y = max(MAP_Y + HERO_SIZE // 2, min(MAP_Y + MAP_HEIGHT - HERO_SIZE // 2, hero.y))

    if hero.vx != 0 or hero.vy != 0:  
        hero.frame_counter += 1
        if hero.frame_counter >= 5:  
            hero.current_frame = (hero.current_frame + 1) % len(hero_run_frames)
            hero.frame_counter = 0
    else:
        hero.current_frame = 0  


    hero_run_frames[hero.current_frame].pos = (hero.x, hero.y)

def update_enemies():
    for enemy_data in enemies:
        enemy_frames = enemy_data['actor']
        enemy = enemy_frames[enemy_data['current_frame']]

        direction_x = hero.x - enemy.x
        direction_y = hero.y - enemy.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)  

        if distance > 0:  
            direction_x /= distance
            direction_y /= distance
            smooth_factor = 0.1 
            enemy.x += direction_x * 15.0 * smooth_factor  
            enemy.y += direction_y * 15.0 * smooth_factor
            enemy_data['frame_counter'] += 1
            if enemy_data['frame_counter'] >= 2: 
                enemy_data['current_frame'] = (enemy_data['current_frame'] + 1) % len(enemy_frames)
                enemy_data['frame_counter'] = 0

        enemy.x = max(MAP_X + ENEMY_SIZE // 2, min(MAP_X + MAP_WIDTH - ENEMY_SIZE // 2, enemy.x))
        enemy.y = max(MAP_Y + ENEMY_SIZE // 2, min(MAP_Y + MAP_HEIGHT - ENEMY_SIZE // 2, enemy.y))
def check_collisions():
    global game_state, game_over_time, congratulations_time
    hero_center = (hero.x, hero.y)  
    for enemy_data in enemies:
        enemy = enemy_data['actor'][enemy_data['current_frame']]
        enemy_center = (enemy.x, enemy.y)  
        distance = math.sqrt((hero_center[0] - enemy_center[0]) ** 2 + (hero_center[1] - enemy_center[1]) ** 2)
        
        if distance < (HERO_SIZE // 2 + ENEMY_SIZE // 2):
            print("Collision detected!")
            if sound_on != False: 
                music.stop()  
                music.play('game_over_sound.ogg') 
            game_state = 'game_over'  
    for conquest in conquest_frames:
            if hero.colliderect(conquest):  
                print("Conquest reached!")
                if sound_on != False:
                    music.stop()  
                    music.play('winning.ogg') 
                game_state = 'congratulations'  
def on_key_down(key):
    if key == keys.LEFT:
        hero.vx = -5
    elif key == keys.RIGHT:
        hero.vx = 5
    elif key == keys.UP:
        hero.vy = -5
    elif key == keys.DOWN:
        hero.vy = 5
    elif game_state == 'game_over':  
        reset_game()
    elif game_state == 'congratulations':  
        reset_game()

def reset_game():
    global game_state, enemies, game_over_time, congratulations_time
    game_over_time = 0
    music.queue('background_music.ogg')  
    music.play('background_music.ogg')  
    game_state = 'menu'  
    enemies = []  
  
    hero.x = 400
    hero.y = 300
    hero.current_frame = 0
    hero.frame_counter = 0

def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        hero.vx = 0
    if key in (keys.UP, keys.DOWN):
        hero.vy = 0


def draw():
    screen.clear()
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'playing':
        draw_map()  
        
        if hero.vx != 0 or hero.vy != 0:
            hero_run_frames[hero.current_frame].draw()  
        else:
            hero.draw()  

        for enemy_data in enemies:
            enemy_frames = enemy_data['actor']
            enemy_frames[enemy_data['current_frame']].draw()  
            conquest_frames[conquest_current_frame].draw()  
    elif game_state == 'game_over':
        draw_game_over()
    elif game_state == 'congratulations':
        draw_congratulations()  

def draw_congratulations():
    screen.draw.text("Parabens!", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=50, color="green")
    screen.draw.text("Voltando ao menu em 3 segundos...", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=30)

def draw_game_over():
    screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=50, color="red")
    screen.draw.text("Voltando ao menu em 3 segundos...", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=30)
    
    

def draw_menu():
    
    screen.draw.text("Iniciar Jogo", center=(400, 250), fontsize=50)
    screen.draw.text("Habilitar/Desabilitar som ", center=(400, 350), fontsize=50)
    screen.draw.text("Sair", center=(400, 450), fontsize=50)
    screen.draw.text("Obs. No menu utilize o mouse, ao jogar utilize o teclado", center=(400, 50), fontsize=30)

def draw_map():
    map_rect = Rect(MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT) 
    screen.draw.rect(map_rect, (150, 150, 150)) 

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == 'menu':
        if (100 < pos[0] < 700) and (220 < pos[1] < 280):
            start_game() 
        elif (100 < pos[0] < 700) and (320 < pos[1] < 380):
            sound_on = not sound_on  
            if sound_on:
                music.play('background_music.ogg')  
            else:
                music.stop()  
        elif (100 < pos[0] < 700) and (420 < pos[1] < 480):
            exit()  

pgzrun.go()
