import pygame
import os
import random
pygame.init()
window_size = (1000, 550)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
BLACK, WHITE, GREY = (0, 0, 0), (255, 255, 255), (108, 108, 108)
BLUE, RED = (0, 0, 255), (255, 0, 0)
font = pygame.font.Font(pygame.font.get_default_font(), 18)

speed_increase = 10
GRAVITY = 8
score = 0
ground_img = pygame.image.load('img/ground.png')
x_gr_pos, y_gr_pos = 0, window_size[1] - 100
gr_img_width = ground_img.get_width()
obstacle = []


def score_counting():
    global score, speed_increase
    content = font.render(f'Score: {int(score)}', True, BLACK, WHITE)
    screen.blit(content, (window_size[0] - 200, 30))
    score += 0.3
    if int(score) % 150 == 0:
        speed_increase += 0.5


def background():
    screen.fill(WHITE)
    global x_gr_pos, gr_img_width
    screen.blit(ground_img, (x_gr_pos, y_gr_pos))
    if gr_img_width + x_gr_pos <= window_size[0]:
        screen.blit(ground_img, (gr_img_width + x_gr_pos, y_gr_pos))
    if x_gr_pos <= -gr_img_width:
        x_gr_pos = 0
    x_gr_pos -= speed_increase
    score_counting()


class Dinosaur:
    x = 70
    y = window_size[1] - 170
    vel = GRAVITY

    def __init__(self):
        self.is_jumping = False
        self.is_running = True
        self.animation_list = []
        self.num_of_frames = 0
        self.reset_step = 0
        self.update_animation_list('run')
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()

    def animation_update(self, key):
        if self.is_jumping:
            self.jump()
        else:
            if key[pygame.K_UP]:
                self.is_jumping = True
                self.is_running = False
            elif key[pygame.K_DOWN]:
                self.duck()
            else:
                self.is_running = True
                self.is_jumping = False
                self.run()
        self.reset_step += 1
        if self.reset_step == 20:
            self.reset_step = 0

    def run(self, TYPE='run'):
        self.update_animation_list(TYPE)
        self.image = self.animation_list[self.reset_step // 10]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, window_size[1] - 170

    def jump(self, TYPE='jump'):
        global GRAVITY
        self.image = pygame.image.load(f'img/Dino/{TYPE}/(1).png')
        if self.is_jumping:
            self.rect.y -= 3 * self.vel
            self.vel -= 0.5
        if self.vel <= -GRAVITY:
            self.is_jumping = False
            self.vel = GRAVITY

    def duck(self, TYPE='duck'):
        self.update_animation_list(TYPE)
        self.image = self.animation_list[self.reset_step // 10]
        self.rect.x, self.rect.y = self.x, window_size[1] - 170 + 34

    def update_animation_list(self, TYPE):
        self.animation_list = []
        self.num_of_frames = len(os.listdir(f'img/Dino/{TYPE}'))
        for i in range(self.num_of_frames):
            img = pygame.image.load(f'img/Dino/{TYPE}/({i + 1}).png')
            self.animation_list.append(img)

    def draw(self):
        screen.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.rect.x = window_size[0]

    def update(self):
        self.rect.x -= speed_increase
        if self.rect.right <= 0:
            obstacle.pop()

    def draw(self):
        screen.blit(self.image, self.rect)


class Bird(Obstacle):
    def __init__(self):
        self.type = 'bird'
        self.flap_count = 0
        num_of_frames = len(os.listdir('img/Bird'))
        self.animation_list = []
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/Bird/({i+1}).png')
            self.animation_list.append(img)
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(40, y_gr_pos - 50)
        Obstacle.__init__(self, self.image, self.rect)

    def update_animation(self):
        if self.flap_count >= 10:
            self.flap_count = 0
        self.image = self.animation_list[self.flap_count // 10]
        self.flap_count += 1


class Cactus(Obstacle):
    def __init__(self):
        temp = random.randint(1, 3)
        self.image = pygame.image.load(f'img/Cactus/({temp}).png')
        self.rect = self.image.get_rect()
        self.rect.y = y_gr_pos - 80
        Obstacle.__init__(self, self.image, self.rect)


bird = Bird()
dino = Dinosaur()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    key_press = pygame.key.get_pressed()
    background()
    dino.draw()
    dino.animation_update(key_press)

    if len(obstacle) == 0:
        obstacle.append(Cactus())

    for ob in obstacle:
        ob.draw()
        ob.update()
        if dino.rect.colliderect(ob.rect):
            pygame.time.delay(2000)
            running = False
    pygame.display.update()

pygame.time.delay(1000)
pygame.quit()
