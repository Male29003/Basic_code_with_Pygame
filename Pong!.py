import pygame
pygame.init()
win_size = [900, 720]
score_board_margin = 70
screen = pygame.display.set_mode(win_size)
BLACK, WHITE, GREY = (0, 0, 0), (255, 255, 255), (108, 108, 108)
BLUE, RED = (0, 0, 255), (255, 0, 0)
clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.get_default_font(), 30)
bar_size, ball_size = [20, 80], 20
board_size = [win_size[0], win_size[1] - score_board_margin]
default_speed, ball_speed = 4, [5.0, 5.0]
ball_start_point = (win_size[0]/2, (win_size[1] + score_board_margin)/2)

COOLDOWN = 450
speed_increase = clock.tick(30) / 1000

def board():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (win_size[0] / 2, score_board_margin), (win_size[0] / 2, win_size[1]), 5)
    pygame.draw.line(screen, WHITE, (0, score_board_margin), (win_size[0], score_board_margin), 5)
    screen.blit(font.render(str(player.score), True, BLUE, BLACK), (win_size[0] / 4, 20))
    screen.blit(font.render(str(ai.score), True, RED, BLACK), (3 * win_size[0] / 4, 20))


class Bar:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - bar_size[1]/2, bar_size[0], bar_size[1])
        self.speed = default_speed
        self.score = 0

    def draw(self, color):
        pygame.draw.rect(screen, color, self.rect)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > score_board_margin+5:
            self.rect.y -= self.speed
        elif key[pygame.K_DOWN] and self.rect.bottom < win_size[1]:
            self.rect.y += self.speed

    def ai_move(self):
        if self.rect.centery < ball.rect.top and self.rect.bottom < win_size[1]:
            self.rect.y += self.speed
        if self.rect.centery > ball.rect.bottom and self.rect.top > score_board_margin+5:
            self.rect.y -= self.speed


class Ball:
    def __init__(self, width, speed):
        self.rect = pygame.Rect(0, 0, width, width)
        self.alive = False
        self.speed = speed
        self.reset()
        self.winner = 0

    def draw(self):
        pygame.draw.ellipse(screen, GREY, self.rect)

    def move(self, p, a):
        if self.rect.bottom >= win_size[1]:
            self.speed[1] *= -1
        if self.rect.top <= score_board_margin+5:
            self.speed[1] *= -1
        if self.rect.colliderect(p) or self.rect.colliderect(a):
            self.speed[0] *= -1
        if self.rect.left == 0:
            self.winner = -1
            ai.score += 1
            self.reset()
        elif self.rect.right == win_size[0]:
            self.winner = 1
            player.score += 1
            self.reset()
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def reset(self):
        self.rect.center = ball_start_point
        self.speed[0] *= -1
        print(self.speed[0])
        self.alive = True
        self.winner = 0


player = Bar(0, (win_size[1] + score_board_margin) / 2)
ai = Bar(win_size[0] - bar_size[0], (win_size[1] + score_board_margin) / 2)
ball = Ball(ball_size, ball_speed)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    board()
    ai.draw(RED)
    player.draw(BLUE)
    if ball.alive:
        COOLDOWN -= 1
        ball.move(player, ai)
        if ball.winner == 0:
            ball.draw()
            player.move()
            ai.ai_move()
        else:
            ball.alive = False
            ball.reset()
    if COOLDOWN == 0:
        if ball.speed[0] > 0: ball.speed[0] += speed_increase
        else: ball.speed[0] -= speed_increase
        if ball.speed[1] > 0: ball.speed[1] += speed_increase
        else: ball.speed[1] -= speed_increase
        player.speed += speed_increase
        ai.speed += speed_increase
        COOLDOWN = 450

    pygame.display.update()
