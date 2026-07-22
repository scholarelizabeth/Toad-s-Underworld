import pygame
import sys
import math

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1000 
SCREEN_HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Toads Underworld")
clock = pygame.time.Clock()

GROUND_HEIGHT = 120
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

try:
    TITLE_BACKGROUND_IMG = pygame.image.load("Title  Screen.png").convert()
    TITLE_BACKGROUND_IMG = pygame.transform.scale(TITLE_BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMG_1 = pygame.image.load("Level 1.webp").convert()
    BACKGROUND_IMG_1 = pygame.transform.scale(BACKGROUND_IMG_1, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMG_2 = pygame.image.load("Level 2.jpg").convert()
    BACKGROUND_IMG_2 = pygame.transform.scale(BACKGROUND_IMG_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMG_3 = pygame.image.load("Level 3.webp").convert()
    BACKGROUND_IMG_3 = pygame.transform.scale(BACKGROUND_IMG_3, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMG_4 = pygame.image.load("Level 4.webp").convert()
    BACKGROUND_IMG_4 = pygame.transform.scale(BACKGROUND_IMG_4, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMG_5 = pygame.image.load("Level 5.jpg").convert()
    BACKGROUND_IMG_5 = pygame.transform.scale(BACKGROUND_IMG_5, (SCREEN_WIDTH, SCREEN_HEIGHT))

    BACKGROUND_IMG_BOSS = pygame.image.load("Big Bad Boss Toad.png").convert()
    BACKGROUND_IMG_BOSS = pygame.transform.scale(BACKGROUND_IMG_BOSS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    PLAYER_IMG = pygame.image.load("Toad Player.png").convert_alpha()
    PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (40, 60))

    ENEMY_IMG_1 = pygame.image.load("Evil Toad Ghost 1.webp").convert_alpha()
    ENEMY_IMG_1 = pygame.transform.scale(ENEMY_IMG_1, (40, 40))

    ENEMY_IMG_2 = pygame.image.load("Evil Toad Ghost 2.webp").convert_alpha()
    ENEMY_IMG_2 = pygame.transform.scale(ENEMY_IMG_2, (40, 40))

    ENEMY_IMG_3 = pygame.image.load("Evil Toad Ghost 3.png").convert_alpha()
    ENEMY_IMG_3 = pygame.transform.scale(ENEMY_IMG_3, (40, 40))

    ENEMY_IMG_4 = pygame.image.load("Evil Toad Ghost 4.webp").convert_alpha()
    ENEMY_IMG_4 = pygame.transform.scale(ENEMY_IMG_4, (40, 40))

    ENEMY_IMG_5 = pygame.image.load("Evil Toad Ghost 5.webp").convert_alpha()
    ENEMY_IMG_5 = pygame.transform.scale(ENEMY_IMG_5, (40, 40))

    BOSS_IMG = pygame.image.load("Big Bad Boss Toad.png").convert_alpha()
    BOSS_IMG = pygame.transform.scale(BOSS_IMG, (100, 100))

    HEART_IMG = pygame.image.load("I'm the Best!.gif").convert_alpha()
    HEART_IMG = pygame.transform.scale(HEART_IMG, (30, 30))

    POWERUP_FLY_IMG = pygame.image.load("Flying Toad Powerup.png").convert_alpha()
    POWERUP_FLY_IMG = pygame.transform.scale(POWERUP_FLY_IMG, (30, 30))

    POWERUP_JUMP_IMG = pygame.image.load("Toad Jump High Powerup.png").convert_alpha()
    POWERUP_JUMP_IMG = pygame.transform.scale(POWERUP_JUMP_IMG, (30, 30))

except pygame.error as e:
    print(f"Image asset missing or broken: {e}. Using flat color fallbacks.")
    TITLE_BACKGROUND_IMG = None
    BACKGROUND_IMG_1 = None
    BACKGROUND_IMG_2 = None
    BACKGROUND_IMG_3 = None
    BACKGROUND_IMG_4 = None
    BACKGROUND_IMG_5 = None
    BACKGROUND_IMG_BOSS = None

    PLAYER_IMG = pygame.Surface((40, 60))
    PLAYER_IMG.fill((0, 0, 255))

    ENEMY_IMG_1 = pygame.Surface((40, 40))
    ENEMY_IMG_1.fill((255, 165, 0))
    ENEMY_IMG_2 = ENEMY_IMG_1.copy()
    ENEMY_IMG_3 = ENEMY_IMG_1.copy()
    ENEMY_IMG_4 = ENEMY_IMG_1.copy()
    ENEMY_IMG_5 = ENEMY_IMG_1.copy()
    BOSS_IMG = pygame.Surface((100, 100))
    BOSS_IMG.fill((200, 0, 0))

    HEART_IMG = pygame.Surface((30, 30))
    HEART_IMG.fill(RED)

    POWERUP_FLY_IMG = pygame.Surface((30, 30))
    POWERUP_FLY_IMG.fill((0, 255, 255))
    POWERUP_JUMP_IMG = pygame.Surface((30, 30))
    POWERUP_JUMP_IMG.fill((0, 255, 0))

def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)
    except pygame.error as e:
        print(f"Audio asset missing or broken: {e}. Running level without music.")

TITLE_MUSIC = "Toad's Underworld Title.mp3"
LEVEL_MUSIC = [
    "11 Ghost Valley.mp3",
    "16a Fortress (1).mp3.crdownload",
    "10 - Shifty Boo Mansion.mp3.crdownload",
    "15 Boo Waltz.mp3.crdownload",
    "13 Bowser's Castle.mp3",
]
BOSS_MUSIC = "07 - Boss Battle (1).mp3.crdownload"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = PLAYER_IMG
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = GROUND_Y

        self.speed = 6
        self.jump_power = -22 
        self.y_vel = 0
        self.is_jumping = False
        self.health = 4
        self.invulnerable = False
        self.invuln_timer = 0

        self.fly_mode = False
        self.high_jump = False
        self.fly_timer = 0
        self.jump_timer = 0

    def update(self, *args): 
        if self.invulnerable and pygame.time.get_ticks() - self.invuln_timer > 1000:
            self.invulnerable = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.fly_mode:
            if keys[pygame.K_UP]:
                self.rect.y -= 8
            if keys[pygame.K_DOWN]:
                self.rect.y += 8

        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_Y and not self.fly_mode:
            jp = self.jump_power
            if self.high_jump:
                jp -= 8  
            self.y_vel = jp
            self.is_jumping = True

        if not self.fly_mode:
            self.y_vel += 0.8
            self.rect.y += self.y_vel

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.y_vel = 0
            self.is_jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        now = pygame.time.get_ticks()
        if self.fly_mode and now - self.fly_timer > 5000:  
            self.fly_mode = False
        if self.high_jump and now - self.jump_timer > 7000: 
            self.high_jump = False

    def take_damage(self, amount=1):
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invuln_timer = pygame.time.get_ticks()

    def give_fly(self):
        self.fly_mode = True
        self.fly_timer = pygame.time.get_ticks()

    def give_high_jump(self):
        self.high_jump = True
        self.jump_timer = pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=2):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speed = speed
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

class Boss(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, speed=3)
        self.health = 20

    def take_hit(self):
        self.health -= 1

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image, kind):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.kind = kind  

class LevelConfig:
    def __init__(self, bg, enemy_img, kill_target, length, music, has_boss=False):
        self.bg = bg
        self.enemy_img = enemy_img
        self.kill_target = kill_target
        self.length = length
        self.music = music
        self.has_boss = has_boss

LEVELS = [
    LevelConfig(BACKGROUND_IMG_1, ENEMY_IMG_1, kill_target=10, length=2000, music=LEVEL_MUSIC[0]),
    LevelConfig(BACKGROUND_IMG_2, ENEMY_IMG_2, kill_target=15, length=2600, music=LEVEL_MUSIC[1]),
    LevelConfig(BACKGROUND_IMG_3, ENEMY_IMG_3, kill_target=20, length=3200, music=LEVEL_MUSIC[2]),
    LevelConfig(BACKGROUND_IMG_4, ENEMY_IMG_4, kill_target=25, length=3800, music=LEVEL_MUSIC[3]),
    LevelConfig(BACKGROUND_IMG_5, ENEMY_IMG_5, kill_target=30, length=4500, music=LEVEL_MUSIC[4]),
    LevelConfig(BACKGROUND_IMG_BOSS, BOSS_IMG, kill_target=1, length=5000, music=BOSS_MUSIC, has_boss=True),
]

font = pygame.font.SysFont(None, 32)

def draw_hud(player, kills, target, level_index):
    for i in range(player.health):
        screen.blit(HEART_IMG, (10 + i * 35, 10))

    text_kills = font.render(f"Kills: {kills}/{target}", True, (255, 105, 180))
    text_level = font.render(f"Level: {level_index + 1}", True, WHITE)
    screen.blit(text_kills, (10, 50))
    screen.blit(text_level, (10, 80))


def title_screen():
    play_music(TITLE_MUSIC)
    title_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        if TITLE_BACKGROUND_IMG:
            screen.blit(TITLE_BACKGROUND_IMG, (0, 0))
        else:
            screen.fill(BLACK)

        title_text = title_font.render("Toads Underworld", True, RED)
        prompt_text = small_font.render("Press any key to help him get through this nightmare...", True, WHITE)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))

        prompt_text = small_font.render("Press any key to help him get through this nightmare...", True, WHITE)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 350))

        pygame.display.flip()
        clock.tick(FPS)


def run_level(level_index):
    cfg = LEVELS[level_index]
    play_music(cfg.music)

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    kills = 0
    total_spawned = 0
    spawn_timer = 0

    boss = None
    if cfg.has_boss:
        boss = Boss(cfg.length - 200, GROUND_Y, cfg.enemy_img)
        enemies.add(boss)
        all_sprites.add(boss)
        total_spawned += 1

    for x in [400, 900, 1400, 1900]:
        p = Powerup(x, GROUND_Y - 150, POWERUP_FLY_IMG, "You can fly!")
        powerups.add(p)
        all_sprites.add(p)
        
    for x in [700, 1200, 1700]:
        p = Powerup(x, GROUND_Y - 150, POWERUP_JUMP_IMG, "Wahooo, Jump!")
        powerups.add(p)
        all_sprites.add(p)

    camera_x = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        spawn_timer += dt
        if spawn_timer > 1500 and not cfg.has_boss and total_spawned < cfg.kill_target:
            spawn_timer = 0
            ex = camera_x + SCREEN_WIDTH + 100
            enemy = Enemy(ex, GROUND_Y, cfg.enemy_img, speed=2 + level_index)
            enemies.add(enemy)
            all_sprites.add(enemy)
            total_spawned += 1

        all_sprites.update(player.rect.x)

        for e in enemies:
            if isinstance(e, Enemy):
                e.update(player.rect.x + camera_x)

        for enemy in enemies.copy():
            if player.rect.colliderect(enemy.rect):
                if player.y_vel >= 0 and player.rect.bottom <= enemy.rect.centery:
                    kills += 1
                    player.y_vel = player.jump_power / 2
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)
                    if isinstance(enemy, Boss):
                        enemy.take_hit()
                        if enemy.health <= 0:
                            kills = cfg.kill_target
                elif not player.invulnerable:
                    player.take_damage(1)
                    if player.health <= 0:
                        return False

        for p in powerups.copy():
            if player.rect.colliderect(p.rect):
                if p.kind == "You can fly!":
                    player.give_fly()
                elif p.kind == "Wahooo, Jump!":
                    player.give_high_jump()
                powerups.remove(p)
                all_sprites.remove(p)

        camera_x = max(0, min(player.rect.x - 200, cfg.length - SCREEN_WIDTH))

        if kills >= cfg.kill_target:
            return True

        if cfg.bg:
            screen.blit(cfg.bg, (-camera_x, 0))
        else:
            screen.fill(GREY)

        pygame.draw.rect(screen, BLACK, (0 - camera_x, GROUND_Y, cfg.length, GROUND_HEIGHT))

        for sprite in all_sprites:
            if sprite == player and player.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0:
                continue
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

        draw_hud(player, kills, cfg.kill_target, level_index)

        pygame.display.flip()


def main():
    title_screen()

    for i in range(len(LEVELS)):
        cleared = run_level(i)
        if not cleared:
            play_music(TITLE_MUSIC)
            go_font = pygame.font.SysFont(None, 64)
            msg = go_font.render("You Died!!! - Press any key to try again", True, RED)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        main()
                        return
                screen.fill(BLACK)
                screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - msg.get_height() // 2))
                pygame.display.flip()
                clock.tick(FPS)
                
        if i < len(LEVELS) - 1:
            play_music(TITLE_MUSIC)
            c_font = pygame.font.SysFont(None, 48)
            msg = c_font.render(f"Level {i + 1} Victory!!! Press any key for the next level.", True, pygame.Color("blue"))

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                screen.fill(BLACK)
                screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - msg.get_height() // 2))
                pygame.display.flip()
                clock.tick(FPS)

    play_music(TITLE_MUSIC)
    v_font = pygame.font.SysFont(None, 64)
    msg = v_font.render("Toad's Underworld, Beat I'm the best!!!", True, WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2,
                          SCREEN_HEIGHT // 2 - msg.get_height() // 2))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
