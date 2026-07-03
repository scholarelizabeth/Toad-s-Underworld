import pygame
import sys
import math

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Toad Hell")
clock = pygame.time.Clock()

GROUND_HEIGHT = 100
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

try:
    pygame.mixer.music.load("Music.mp3")   
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

except pygame.error as e:
    print(f"Audio asset missing or broken: {e}. Running game without music.")

try:
    BACKGROUND_IMG = pygame.image.load("Toad Hellll!!!.png").convert()
    BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    PLAYER_IMG = pygame.image.load("TOOOOAAAADDDDD.png").convert_alpha()
    ENEMY_IMG = pygame.image.load("Evil_Toad_Ghost.webp").convert_alpha()
    HEART_IMG = pygame.image.load("I'm the Best!.gif").convert_alpha()
except pygame.error as e:
    print(f"Image asset missing or broken: {e}. Using flat color fallbacks.")
    BACKGROUND_IMG = None
    TITLE_BACKGROUND_IMG = None
    PLAYER_IMG = pygame.Surface((40, 60))
    PLAYER_IMG.fill((0, 0, 255))
    ENEMY_IMG = pygame.Surface((40, 40))
    ENEMY_IMG.fill((255, 165, 0))
    HEART_IMG = pygame.Surface((20, 20))
    HEART_IMG.fill(RED)

HEART_IMG = pygame.transform.scale(HEART_IMG, (30, 30))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = GROUND_Y

        self.speed = 5
        self.jump_power = -30
        self.y_vel = 0
        self.is_jumping = False
        self.health = 4
        self.invulnerable = False
        self.invuln_timer = 0

    def update(self):
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invuln_timer > 1000:
                self.invulnerable = False

        self.y_vel += 0.8
        self.rect.y += self.y_vel

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.y_vel = 0
            self.is_jumping = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.y_vel = self.jump_power
            self.is_jumping = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speed = 2
        self.y_vel = 0

    def update(self, player_x):
        self.y_vel += 0.8
        self.rect.y += self.y_vel
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.y_vel = 0

        if self.rect.x < player_x:
            self.rect.x += self.speed
        elif self.rect.x > player_x:
            self.rect.x -= self.speed

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

enemy = Enemy(600, GROUND_Y)
all_sprites.add(enemy)
enemies.add(enemy)

font = pygame.font.SysFont("Arial", 64)

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                player = Player()
                all_sprites = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                all_sprites.add(player)
                enemy = Enemy(600, GROUND_Y)
                all_sprites.add(enemy)
                enemies.add(enemy)
                game_over = False

    if not game_over:
        player.update()
        enemies.update(player.rect.x)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            if player.y_vel > 0 and player.rect.bottom <= hit.rect.top + 15:
                hit.kill()
                player.y_vel = player.jump_power / 1.5

                new_enemy = Enemy(SCREEN_WIDTH if player.rect.x < 400 else 0, GROUND_Y)
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)
            else:
                if not player.invulnerable:
                    player.health -= 1
                    player.invulnerable = True
                    player.invuln_timer = pygame.time.get_ticks()
                    if player.health <= 0:
                        game_over = True

    if game_over:
        screen.fill(BLACK)
        game_over_text = font.render("FAAAAAAAAA!!!!!", True, WHITE)
        restart_text = pygame.font.SysFont("Arial", 24).render("Press R to Restart", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    else:
        if BACKGROUND_IMG:
            screen.blit(BACKGROUND_IMG, (0, 0))
        else:
            screen.fill((135, 206, 235)) 

        pygame.draw.rect(screen, GREY, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))

        for sprite in all_sprites:
            if sprite == player and player.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
                continue 
            screen.blit(sprite.image, sprite.rect)

        for i in range(player.health):
            screen.blit(HEART_IMG, (10 + (i * 35), 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
