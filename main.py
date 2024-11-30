
import sys
from menus.game_menu import Menu
from constants.constants import *
from menus.pause_menu import PauseMenu
from worlds import level_1
print('Imported all modules')

class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2 + 200
        self.width = 35  # Rect width
        self.height = 40  # Rect height
        self.sprite_width = 200  # Sprite width
        self.sprite_height = 200  # Sprite height
        self.color = (255, 0, 0)
        self.health = 3
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
        sprite = pygame.transform.scale(self.idle_sprites[self.idle_frame], (self.sprite_width, self.sprite_height))
        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2, self.y - (self.sprite_height - self.height) + self.height + 45))
        self.draw_hitbox()

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
        self.draw_hitbox()

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

        # Update the player's rectangle position
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Check for horizontal collisions
        for block in current_world.blocks:
            if self.rect.colliderect(block):
                if self.rect.right > block.left and self.rect.left < block.right:
                    if self.facing_left:
                        self.x = block.right
                    else:
                        self.x = block.left - self.width

        # Update the player's rectangle position again after collision adjustment
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_if_on_block(self):
        blocks = current_world.blocks
        on_block = False

        if not self.jumping:  # Only check if the player is not jumping
            for block in blocks:
                # Check if the player is directly above a block
                if (
                        self.rect.bottom <= block.top + self.speed  # Near or touching the block's top
                        and self.rect.right > block.left  # Horizontally overlapping
                        and self.rect.left < block.right  # Horizontally overlapping
                ):
                    self.y = block.top - self.height  # Align player to the top of the block
                    on_block = True
                    break

            if not on_block:
                self.jumping = True  # Player starts falling if not above a block

    def gravity(self):
        blocks = current_world.blocks

        if self.jumping:  # Apply gravity if jumping or falling
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity_force  # Increase downward velocity
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # Check for landing on a block
            for block in blocks:
                if (
                        self.rect.colliderect(block)
                        and self.rect.bottom >= block.top  # Ensure player is actually landing
                        and self.rect.bottom <= block.top + self.jump_velocity + 1  # Account for overshoot
                        and self.rect.right > block.left  # Horizontally overlapping
                        and self.rect.left < block.right  # Horizontally overlapping
                ):
                    self.y = block.top - self.height  # Align with block's top
                    self.jumping = False  # Stop falling
                    self.jump_velocity = 0  # Reset vertical velocity
                    break
        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Check if player falls below the world or not on any block

    def check_dead(self):
        if self.y > HEIGHT:
            self.health -= 1
            self.x = 50
            self.y = HEIGHT // 2 + 200
        for spike in current_world.spikes:
            if self.rect.colliderect(spike):
                self.health -= 1
                self.x = 50
                self.y = HEIGHT // 2 + 200
        for spike in current_world.special_spikes:
            if self.rect.colliderect(spike):
                self.health -= 1
                self.x = 50
                self.y = HEIGHT // 2 + 200

    def draw_hitbox(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)

    def events(self):
        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.x > 250:
            current_world.draw_special_spike(0)
        if player.rect.x < 450:
            current_world.draw_special_spike(1)
        if player.rect.x > 500:
            current_world.special_spikes.pop()
            current_world.special_spikes.append(pygame.Rect(0, HEIGHT // 2 + 190, 50, 50))

print('Created player object')
pygame.init()
print('Initialized pygame')
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
    current_level = level_1.Level_1()
    current_world = level_1.Level_1.World_1()
    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        player.update_position(keys)
        player.gravity()
        player.check_if_on_block()
        player.check_dead()
        current_world.draw()
        player.events()
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