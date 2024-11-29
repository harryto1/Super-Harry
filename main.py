import sys
from menus.game_menu import Menu
from constants.constants import *
from menus.pause_menu import PauseMenu

class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2 + 200
        self.width = 200
        self.height = 200
        self.color = (255, 0, 0)
        self.health = 100
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.moving = False
        self.facing_left = False
        self.jumping = False
        self.jump_velocity = 0
        self.gravity_force = 1
        self.idle_spritesheet = pygame.image.load('assets/characters/player/Soldier-Idle.png')
        self.idle_sprites = []
        for i in range(6):
            sprite = self.idle_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
            self.idle_sprites.append(sprite)
        self.walk_spritesheet = pygame.image.load('assets/characters/player/Soldier-Walk.png')
        self.walk_sprites = []
        for i in range(8):
            sprite = self.walk_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
            self.walk_sprites.append(sprite)
        self.idle_frame = 0
        self.walk_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # milliseconds per frame

    def draw_idle(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.idle_frame = (self.idle_frame + 1) % len(self.idle_sprites)
        sprite = pygame.transform.scale(self.idle_sprites[self.idle_frame], (self.width, self.height))
        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, (self.x, self.y))

    def draw_walk_animation(self):
        if not self.walk_sprites:
            return  # Avoid division by zero if walk_sprites is empty
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_sprites)
        sprite = pygame.transform.scale(self.walk_sprites[self.walk_frame], (self.width, self.height))
        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, (self.x, self.y))

    def update_position(self, keys):
        self.moving = False
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.moving = True
            self.facing_left = True
        if keys[pygame.K_d]:
            self.x += self.speed
            self.moving = True
            self.facing_left = False
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jump_velocity = -15  # Initial jump velocity
            self.jumping = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def gravity(self):
        if self.jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity_force
            if self.y >= HEIGHT // 2 + 200:
                self.y = HEIGHT // 2 + 200
                self.jumping = False
                self.jump_velocity = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

pygame.init()
Clock = pygame.time.Clock()
screen = pygame.display.set_mode()
pygame.display.set_caption("Game Menu")
menu_items = ['Start', 'Quit']
menu = Menu(GRAY, menu_items)
selected = menu.run()
if selected == 1:
    sys.exit()
elif selected == 0:
    print('Starting game...')
    screen.fill(BLACK)
    player = Player()
    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        player.update_position(keys)
        player.gravity()
        if player.moving:
            player.draw_walk_animation()
        else:
            player.draw_idle()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_selected = PauseMenu().run()
                    if pause_selected == 1:
                        sys.exit()
        pygame.display.update()
        Clock.tick(60)  # Set the frame rate to 60 FPS