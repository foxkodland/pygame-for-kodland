import pygame
import random

WIDTH = 600  # ширина игрового окна
HEIGHT = 480 # высота игрового окна
FPS = 30 # частота кадров в секунду
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Для Экзамена)")
clock = pygame.time.Clock()


class Button_start(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(WIDTH/2, HEIGHT/2))


class Fon(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(WIDTH/2, HEIGHT/2))

# враги
class White_circle(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()

        r = random.randint (1,4)
        if r == 1:
            self.direction = "вверх"
            self.rect = self.image.get_rect(center=(random.randint(191,402), HEIGHT - 10))
        elif r == 2:
            self.direction = "вниз"
            self.rect = self.image.get_rect(center=(random.randint(191,402), 10))
        elif r == 3:
            self.direction = "влево"                                
            self.rect = self.image.get_rect(center=(WIDTH - 10, random.randint(133,344)))
        elif r == 4:
            self.direction = "вправо"
            self.rect = self.image.get_rect(center=(10, random.randint(133,344)))
    
    def update(self):
        if self.direction == 'вверх':
            self.rect.y -= 1
            if self.rect.y < 10:
                self.kill()
        elif self.direction == 'вниз':
            self.rect.y += 1
            if self.rect.y > HEIGHT - 10:
                self.kill()
        elif self.direction == 'влево':
            if self.rect.x < 10:
                self.kill()
            self.rect.x -= 1
        elif self.direction == 'вправо':
            if self.rect.x > WIDTH - 10:
                self.kill()
            self.rect.x += 1
        
        if game_status == 'проигрыш':
            self.kill()

# сердчечко
class Heart(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(WIDTH/2, HEIGHT/2))

    def update(self):
        # keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 191:
                self.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            if self.rect.x < 380:
                self.rect.x += 3
        if keys[pygame.K_UP]:
            if self.rect.y > 135:
                self.rect.y -= 3
        if keys[pygame.K_DOWN]:
            if self.rect.y < 320:
                self.rect.y += 3


heart = Heart('images/heart.png')
button_start = Button_start ('images/button_start.png')

all_sprites = pygame.sprite.Group()
all_sprites.add(button_start)

enemies = []
game_status = 'menu'  # 3 состояния игры: menu, game, проигрыш

def start_game():
    '''
    игра начинается
    1. пустой список врагов
    2. Добавлен спрайт фона и сердечка
    3. изменен статус игры
    '''
    global enemies, game_status, all_sprites
    enemies = []
    game_status = 'game'
    all_sprites = pygame.sprite.Group() 
    all_sprites.add(Fon('images/fon_game.svg'))                   
    all_sprites.add(heart)


def click_start():
    ''' 
    клик мышкой по кнопке Start (не по спрайту, а по похожим координатам) или Enter
    '''
    global game_status, keys
    pressed = pygame.mouse.get_pressed()
    if pressed[0] or keys[pygame.K_RETURN]:
        pos = pygame.mouse.get_pos()
        if pos[0] > 206 and pos[0] < 397 and pos[1] > 209 and pos[1] < 273 or keys[pygame.K_RETURN]:
            start_game()


def new_enemies():
    '''
    с некоторой случайностю создаёт нового врага
    all_sprites - все спрайты
    enemies - список с врагами
    '''
    if random.randint(1,20) == 1:
        new_enemi = White_circle('images/enemy.png')
        all_sprites.add(new_enemi)
        enemies.append(new_enemi)


def check_collision():
    '''
    проверка столкновения сердечка и списка врагов
    '''
    global game_status, all_sprites
    hits = pygame.sprite.spritecollide(heart, enemies, False)
    if hits:
        game_status = 'проигрыш'
        all_sprites = pygame.sprite.Group()
        all_sprites.add (Fon('images/fon_lose.jpg'))


running = True
while running:
    # возможность закрыть окно с игрой
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() # получить нажатые клавишы

    if game_status == 'menu':   
        click_start() # клик мышкой по Start или Enter
    if game_status == 'game':
        new_enemies() # генерация новых врагов
        check_collision() # столкновение с врагами
    if game_status == 'проигрыш':
        if keys[pygame.K_RETURN]:  # перезапуск игры по Enter  
            start_game()

    # отрисовка 
    screen.fill(BLACK)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
quit()
