import time
initial_time = time.time()
import sys
from menus.game_menu import Menu
from constants.constants import *
from menus.pause_menu import PauseMenu
from worlds import level_1
from worlds.events import level1


print(f'Imported all modules in {time.time() - initial_time} seconds')

class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2 + 200
        self.width = 35  # Rect width
        self.height = 40  # Rect height
        self.sprite_width = 200  # Sprite width
        self.sprite_height = 200  # Sprite height
        self.color = (255, 0, 0)
        self.health = 5
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
        self.heart = pygame.image.load('assets/characters/ui/heart_scaled_to_256x256.png')

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
            if isinstance(block, list):
                for b in block:
                    if self.rect.colliderect(b):
                        if self.rect.bottom > b.top and self.rect.top < b.bottom:
                            if self.facing_left:
                                self.x = b.right
                            else:
                                self.x = b.left - self.width
            else:
                if self.rect.colliderect(block):
                    if self.rect.right > block.left and self.rect.left < block.right:
                        if self.facing_left:
                            self.x = block.right
                        else:
                            self.x = block.left - self.width
        if player.x < 0:
            player.x = 0

        # Update the player's rectangle position again after collision adjustment
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_if_on_block(self):
        if hasattr(current_world, 'moving_blocks'):
            blocks = current_world.blocks + [block[0] for block in current_world.moving_blocks]
        else:
            blocks = current_world.blocks
        on_block = False

        if not self.jumping:  # Only check if the player is not jumping
            for block in blocks:
                if isinstance(block, list):
                    for b in block:
                        if (
                                self.rect.bottom <= b.top + self.speed  # Near or touching the block's top
                                and self.rect.right > b.left  # Horizontally overlapping
                                and self.rect.left < b.right  # Horizontally overlapping
                        ):
                            on_block = True
                            break
                else:
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
        if hasattr(current_world, 'moving_blocks'):
            blocks = current_world.blocks + [block[0] for block in current_world.moving_blocks]
        else:
            blocks = current_world.blocks

        if self.jumping:  # Apply gravity if jumping or falling
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity_force  # Increase downward velocity
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # Check for landing on a block
            for block in blocks:
                if isinstance(block, list):
                    for b in block:
                        if (
                                self.rect.colliderect(b)
                                and self.rect.bottom >= b.top  # Ensure player is actually landing
                                and self.rect.bottom <= b.top + self.jump_velocity + 1  # Account for overshoot
                                and self.rect.right > b.left  # Horizontally overlapping
                                and self.rect.left < b.right  # Horizontally overlapping
                        ):
                            self.y = b.top - self.height
                            self.jumping = False
                            self.jump_velocity = 0
                            break
                else:
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
        if hasattr(current_world, 'spikes'):
            for spike in current_world.spikes:
                if self.rect.colliderect(spike):
                    self.health -= 1
                    self.x = 50
                    self.y = HEIGHT // 2 + 200
        if hasattr(current_world, 'special_spikes'):
            for spike in current_world.special_spikes:
                if self.rect.colliderect(spike):
                    self.health -= 1
                    self.x = 50
                    self.y = HEIGHT // 2 + 200

    def draw_hitbox(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)

    def draw_hearts(self):
        hearts_rects = [
            pygame.Rect(10 + i * 40, 10, 30, 30) for i in range(self.health)
        ]
        for heart_rect in hearts_rects:
            screen.blit(pygame.transform.scale(self.heart, (30, 30)), heart_rect)

    def events(self):
        if level == 0:
            if world == 0:
                level1.world1_events(player, current_world)

    def check_for_new_world(self):
        global world, current_world
        if self.x > WIDTH:
            world += 1
            current_world = current_level.worlds[world]
            self.x = 25
            for block in current_world.blocks:
                if isinstance(block, list):
                    for b in block:
                        if b.x == 0:
                            self.y = b.y - self.height
                else:
                    if block.x == 0:
                        self.y = block.y - self.height
            self.jumping = False
            self.jump_velocity = 0

    def check_0_health(self):
        global level, current_level, current_world, world
        if self.health == 0:
            title = pygame.font.Font(None, 72).render('Game Over', 1, (255, 0, 0))
            title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title, title_rect)
            pygame.display.update()
            pygame.time.wait(3000)
            current_world = current_level.worlds[0]
            world = 0
            if level == 0:
                level1.level1_start()
                current_level = level_1.Level1()
            self.events()
            current_world.draw()
            self.x = 25
            for block in current_world.blocks:
                if isinstance(block, list):
                    for b in block:
                        if b.x == 0:
                            self.y = b.y - self.height
                else:
                    if block.x == 0:
                        self.y = block.y - self.height
            self.jumping = False
            self.jump_velocity = 0
            self.health = 5



print(f'Created player object in {time.time() - initial_time} seconds')
pygame.init()
print(f'Initialized pygame in {time.time() - initial_time} seconds')
Clock = pygame.time.Clock()
screen = pygame.display.set_mode()
pygame.display.set_caption("Game Menu")
menu_items = ['Start', 'Quit']
menu = Menu(GRAY, menu_items)
selected = menu.run()
world = 0
level = 0
if selected == 1:
    sys.exit()
elif selected == 0:
    print('Starting game...')
    screen.fill(BLACK)
    player = Player()
    current_level = level_1.Level1()
    current_world = current_level.worlds[world]
    level1.level1_start()
    running = True
    while running:
        screen.fill(BLACK)
        player.check_for_new_world()
        player.check_0_health()
        keys = pygame.key.get_pressed()
        player.update_position(keys)
        player.gravity()
        player.check_if_on_block()
        player.check_dead()
        current_world.draw()
        player.draw_hearts()
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