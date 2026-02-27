from pygame import *

# Настройка окна.
WIDTH, HEIGHT = 1400, 1000 
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Пинг понг")

# Текст
font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None, 120)

# Картинки.
bg = transform.scale(image.load("bg.jpeg"), (WIDTH, HEIGHT))

scor1 = 0
scor2 = 0

# Классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_x, player_y, player_wid, player_hei, player_speed, player_image):
        super().__init__()
        self.width = player_wid
        self.height = player_hei
        self.image = transform.scale(image.load(player_image), (player_wid, player_hei))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y <= HEIGHT - self.height:
            self.rect.y += self.speed

    def update2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y <= HEIGHT - self.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_x, player_y, player_wid, player_hei, player_speed, player_image):
        super().__init__(player_x, player_y, player_wid, player_hei, player_speed, player_image)
        self.speed_x = player_speed
        self.speed_y = player_speed
        self.start_x = player_x
        self.start_y = player_y

    def update(self):
        global scor1, scor2
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - self.height:
            self.speed_y *= -1
        if sprite.collide_rect(player1, self):
            self.speed_x = self.speed
        if sprite.collide_rect(player2, self):
            self.speed_x = -1 * self.speed

        if self.rect.x <= 0:
            scor2 += 1
            self.rect.x = self.start_x
            self.rect.y = self.start_y
            self.speed_x *= -1
        if self.rect.x >= WIDTH - self.height:
            scor1 += 1
            self.rect.x = self.start_x
            self.rect.y = self.start_y
            self.speed_x *= -1

player1 = Player(100, 440, 100, 200, 5, "platform_left.png")
player2 = Player(1200, 440, 100, 200, 5, "platform_right.png")

ball = Ball(650, 450, 100, 100, 5, "ball.png")

# Цикл.
clock = time.Clock()
gameplay = True
finish = False

text_end = None

while gameplay:

    for e in event.get():
        if e.type == QUIT:
            gameplay = False
    
    screen.blit(bg, (0, 0))
    player1.reset()
    player2.reset()
    ball.reset()

    if not finish:
        player1.update1()
        player2.update2()
        ball.update()
    else:
        screen.blit(text_end, (220, 460))

    text_scor1 = font1.render("Счёт: " + str(scor1), True, (0, 255, 0))
    text_scor2 = font1.render("Счёт: " + str(scor2), True, (255, 0, 0))

    screen.blit(text_scor1, (100, 10))
    screen.blit(text_scor2, (1120, 10))

    if scor1 == 10:
        text_end = font2.render("Победил игрок слево!", True, (0, 255, 0))
        finish = True
    if scor2 == 10:
        text_end = font2.render("Победил игрок справо!", True, (255, 0, 0))
        finish = True

    display.update()
    clock.tick(60)
