import pygame
import random

WIDTH = 600  # ширина игрового окна
HEIGHT = 480 # высота игрового окна
FPS = 30 # частота кадров в секунду

# Цвет
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

# сердчечко
class Heart(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(WIDTH/2, HEIGHT/2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 191:
                self.rect.x -= 3
        elif keys[pygame.K_RIGHT]:
            if self.rect.x < 380:
                self.rect.x += 3
        elif keys[pygame.K_UP]:
            if self.rect.y > 135:
                self.rect.y -= 3
        elif keys[pygame.K_DOWN]:
            if self.rect.y < 320:
                self.rect.y += 3


heart = Heart('images/heart.png')
button_start = Button_start ('images/button_start.png')
fon = Fon ('images/fon_menu.svg')

all_sprites = pygame.sprite.Group()
all_sprites.add(fon)
all_sprites.add(button_start)

enemies = []
game_status = 'menu'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # перезапуск игры по Enter
        if event.type == pygame.KEYDOWN:
            if game_status == 'проигрыш':
                if event.key == pygame.K_RETURN:
                    enemies = []
                    all_sprites.empty() 
                    all_sprites.add(Fon('images/fon_game.svg'))                   
                    all_sprites.add(Heart('images/heart.png'))
                    game_status = 'game'

    # мы в меню ждём клика по кнопке
    if game_status == 'menu':   
        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if pressed[0]:
            if pos[0] > 212 and pos[0] < 371 and pos[1] > 214 and pos[1] < 264:
                all_sprites.remove(button_start) 
                heart = Heart('images/heart.png') 
                all_sprites.add(heart)
                fon.image = pygame.image.load('images/fon_game.svg').convert_alpha()
                game_status = 'game'

    # генерация новых врагов
    if game_status == 'game':
        if random.randint(1,20) == 1:
            new_enemi = White_circle('images/enemy.png')
            all_sprites.add(new_enemi)
            enemies.append(new_enemi)

        # столкновение
        hits = pygame.sprite.spritecollide(heart, enemies, False)
        if hits:
            game_status = 'проигрыш'
            all_sprites.empty()
            all_sprites.add (Fon('images/fon_lose.jpg'))

    screen.fill(BLACK)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
quit()
