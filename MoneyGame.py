import pygame
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
SPEED = 16

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT-30))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Block(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH), 0))
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()

player = Player()
blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
start_ticks = pygame.time.get_ticks()
speed_multiplier = 1
score = 0
high_score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.time.get_ticks() % 30 == 0:
        new_block = Block(SPEED * speed_multiplier)
        blocks.add(new_block)
        all_sprites.add(new_block)
        score += 1 * speed_multiplier

    all_sprites.update()

    if pygame.sprite.spritecollideany(player, blocks):
        if score > high_score:
            high_score = score
        player.kill()
        text = font.render("YOU DIED", True, RED)
        screen.blit(text, (WIDTH/2 - text.get_width() // 2, HEIGHT/2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        player = Player()
        all_sprites.add(player)
        blocks.empty()
        speed_multiplier = 1
        start_ticks = pygame.time.get_ticks()
        score = 0

    multiplier_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if multiplier_seconds > 15:
        speed_multiplier *= 1.5
        start_ticks = pygame.time.get_ticks()

    if score >= 300:
        text = font.render("YOU WON!!!", True, GREEN)
        screen.blit(text, (WIDTH/2 - text.get_width() // 2, HEIGHT/2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    screen.fill((0, 0, 0))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    timer_text = font.render(f"Timer: {int(pygame.time.get_ticks() / 1000)}s", True, WHITE)
    multiplier_text = font.render(f"Multiplier: x{speed_multiplier:.1f}", True, RED)
    win_text = font.render("REACH 300 POINTS FOR $50", True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 10))
    screen.blit(multiplier_text, (10, 70))
    screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT - 40))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
