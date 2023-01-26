import pgzrun
import random

WIDTH = 590
HEIGHT = 400
TITLE = 'игра для экзамена'
FPS = 30

fon = Actor ('menu.svg')
heart = Actor ('heart', (250,250))
button_start = Actor ('button_start.png',(280,200))

status_game = 'menu' # состояние игры: menu, game, game_over
enemies = [] #список врагов

def draw():
    fon.draw()

    if status_game == 'menu':
        button_start.draw()

    if status_game == 'game':
        heart.draw()
        for d in enemies:
            d['object'].draw()
    
    if status_game == 'game_over':
        screen.draw.text("Так жаль, но это проигрыш(", pos=(210, 100), color="white", fontsize = 24)
        screen.draw.text("Нажимай ENTER, ты сможешь все исправить)", pos=(150, 130), color="white", fontsize = 24)


def create_new_enemy():
    '''
    по рандомной случайности создаётся новый враг в одной из сторон игры
    direction - в каком направлении он будет потом двигаться
    '''
    global enemies
    if random.randint(1,30) == 1:
        # добавим нового врага
        rand = random.randint (1,4)
        if rand == 1:
            direction = "вверх"
            y = HEIGHT
            x = random.randint(200, 390)
        elif rand == 2:
            direction = "вниз"
            y = 0
            x = random.randint(200, 390)
        elif rand == 3:
            direction = "вправо"
            y = random.randint(120, 315)
            x = 0
        else:
            direction = "влево"
            y = random.randint(120, 315)
            x = WIDTH

        d = {
            'object': Actor("enemy.png", (x, y)),
            'direction': direction
        }
        enemies.append(d)


def move_enemies():
    '''
    движение врагов
    '''
    global enemies
    for d in enemies:
        if d['direction'] == 'вверх':
            d['object'].y -= 1
            if d['object'].y < 10:
                enemies.remove(d)
        elif d['direction'] == 'вниз':
            d['object'].y += 1
            if d['object'].y > HEIGHT - 10:
                enemies.remove(d)
        elif d['direction'] == 'влево':
            d['object'].x -= 1
            if d['object'].x < 10:
                enemies.remove(d)
        else:
            d['object'].x += 1
            if d['object'].x > WIDTH - 10:
                enemies.remove(d)

def check_collision():
    '''
    проверка на столкновение с врагами
    '''
    global heart, enemies, status_game, fon
    for d in enemies:
        if heart.colliderect(d['object']):
            status_game = 'game_over'
            fon.image = 'menu.svg'

def move_heart():
    '''
    движение главного персонажа
    '''
    global heart
    if keyboard.left and heart.x > 200:
        heart.x -= 5
    elif keyboard.right and heart.x < 390:
        heart.x+= 5
    elif keyboard.up and heart.y > 120:
        heart.y -= 5
    elif keyboard.down and heart.y < 315:
        heart.y += 5 

def update(dt):
    global status_game

    if status_game == 'game':
        move_heart()
        check_collision() 
        create_new_enemy()
        move_enemies()    
    

def on_mouse_down(button, pos):
    global status_game, button_start, fon 
    if status_game == 'menu' and button_start.collidepoint(pos):
        fon.image = "bg-game.svg"
        status_game = 'game'

def on_key_down (key):
    '''
    перезапуск игры
    '''
    global status_game, enemies, fon
    if keyboard.K_RETURN and status_game == 'game_over':
        fon.image = 'bg-game.svg'
        enemies = []
        status_game = 'game'


pgzrun.go()