import pygame
import os
from pygame import mixer

pygame.init()
mixer.init()

win_size = [900, 720]
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption("The Southside Soldier")
clock = pygame.time.Clock()
mixer.music.load('music/DatingFight!.mp3')
mixer.music.play()

character_size = (50, 50)
GRAVITY = 0.5


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, character_type, animation):
        pygame.sprite.Sprite.__init__(self)
        self.flip = False
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.speed = speed
        nums_of_frames = os.listdir(f'img/{character_type}/{animation}')
        self.image = pygame.transform.scale(pygame.image.load(f'img/luke.png').convert(), character_size)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def moving(self):
        if self.moving_left:
            self.rect.centerx -= self.speed
            self.flip = True
        if self.moving_right:
            self.rect.centerx += self.speed
            self.flip = False
        if self.jumping:
            self.jumping = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Character(50, 50, 5, 'player')
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_SPACE:
                player.jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_SPACE:
                player.jumping = False
    screen.fill((0, 0, 0))
    player.draw()
    player.moving()
    pygame.display.update()

pygame.time.delay(1000)
pygame.quit()
