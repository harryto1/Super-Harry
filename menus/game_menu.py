import random
import sys
from constants.constants import *
from menus.pause_menu import PauseMenu

class PlayerNPC:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 3 + HEIGHT // 3 + 100
        self.width = 35
        self.height = 40
        self.sprite_width = 200  # Sprite width
        self.sprite_height = 200  # Sprite height
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
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
        self.facing_left = False
        self.moving = False
        self.wandering = True
        self.destination_x = random.randint(50, WIDTH - 50)


    def draw_idle(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.idle_frame = (self.idle_frame + 1) % len(self.idle_sprites)
        sprite = pygame.transform.scale(self.idle_sprites[self.idle_frame], (self.sprite_width, self.sprite_height))
        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2, self.y - (self.sprite_height - self.height) + self.height + 45))

    def draw_walk_animation(self):
        if not self.walk_sprites:
            return  # Avoid division by zero if walk_sprites is empty
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_sprites)
        sprite = pygame.transform.scale(self.walk_sprites[self.walk_frame], (self.sprite_width, self.sprite_height))
        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2, self.y - (self.sprite_height - self.height) + self.height + 45))

    def wander(self):
        if self.wandering:
            if self.destination_x < self.x:
                self.facing_left = True
            else:
                self.facing_left = False
            if abs(self.x - self.destination_x) < self.speed:
                self.moving = False
                self.wandering = False
            elif self.x < self.destination_x:
                self.x += self.speed
                self.moving = True
            elif self.x > self.destination_x:
                self.x -= self.speed
                self.moving = True

    def run(self):
        self.wander()
        if not self.moving:
            self.draw_idle()
        else:
            self.draw_walk_animation()
        if random.randint(0, 100) == 0 and not self.wandering:
            self.wandering = True
            self.destination_x = random.randint(50, WIDTH - 50)



class Menu:
    def __init__(self, font_color, menu_items):
        self.screen = screen
        self.bg_color = bg_color
        self.title_font = pygame.font.Font('assets/font/Monocraft.ttf', 96)
        self.font = pygame.font.Font('assets/font/Monocraft.ttf', 36)
        self.font_color = font_color
        self.menu_items = menu_items
        self.selected_item = 0
        self.clock = pygame.time.Clock()
        self.menu_loop = True
        self.player_NPC = PlayerNPC()

    def draw(self):
        self.screen.fill(self.bg_color)
        title = self.title_font.render('Super Harry Game', 1, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        for i, item in enumerate(self.menu_items):
            if i == self.selected_item:
                label = self.font.render(item, 1, (255, 255, 255))
            else:
                label = self.font.render(item, 1, self.font_color)
            label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 75))
            self.screen.blit(label, label_rect)

    def run(self):
        while self.menu_loop:
            self.clock.tick(60)
            self.screen.fill(self.bg_color)
            self.draw()
            self.player_NPC.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    if event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    if event.key == pygame.K_RETURN:
                        self.menu_loop = False
                    if event.key == pygame.K_ESCAPE:
                        pause_selected = PauseMenu().run()
                        if pause_selected == 1:
                            sys.exit()
            pygame.display.flip()
        return self.selected_item


