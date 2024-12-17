import time
initial_time = time.time()
import sys
from menus.game_menu import Menu
from constants.constants import *
from menus.pause_menu import PauseMenu
from menus.game_over_menu import GameOverMenu
from worlds import level_1
from worlds.events import level1


print(f'Imported all modules in {time.time() - initial_time} seconds')

class Player:
    def __init__(self):
        self.block_beneath = None
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
        self.hurt_spritesheet = pygame.image.load('assets/characters/player/Soldier-Hurt.png')
        self.hurt_sprites = []
        for i in range(4):
            sprite = self.hurt_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
            self.hurt_sprites.append(sprite)
        self.death_spritesheet = pygame.image.load('assets/characters/player/Soldier-Death.png')
        self.death_sprites = []
        for i in range(4):
            sprite = self.death_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
            self.death_sprites.append(sprite)
        self.idle_frame = 0
        self.walk_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # milliseconds per frame
        self.heart = pygame.image.load('assets/characters/ui/heart_scaled_to_256x256.png')
        self.immune = False

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

    def draw_hurt_animation(self):
        if not self.hurt_sprites:
            return
        for i in range(4):
            sprite = pygame.transform.scale(self.hurt_sprites[i], (self.sprite_width, self.sprite_height))
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2, self.y - (self.sprite_height - self.height) + self.height + 45))
            pygame.display.update()
            pygame.time.wait(200)

    def draw_death_animation(self):
        if not self.death_sprites:
            return
        for i in range(4):
            screen.fill(BLACK)
            sprite = pygame.transform.scale(self.death_sprites[i], (self.sprite_width, self.sprite_height))
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2, self.y - (self.sprite_height - self.height) + self.height + 45))
            pygame.display.update()
            pygame.time.wait(200)

    def update_position(self, keys):
        global world, current_world
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
        for attr in ['blocks', 'barrier_blocks', 'visible_blocks', 'moving_blocks']:
            if hasattr(current_world, attr):
                if attr == 'moving_blocks':
                    for block in [b[0] for b in getattr(current_world, attr)]:
                        if self.rect.colliderect(block):
                            if self.rect.right > block.left and self.rect.left < block.right:
                                if self.facing_left:
                                    self.x = block.right
                                else:
                                    self.x = block.left - self.width
                else:
                    for block in getattr(current_world, attr):
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
        if world == 0:
            if player.x < 0:
                player.x = 0
        else:
            if player.x < 0:
                world -= 1
                current_world = current_level.worlds[world]
                player.x = WIDTH - 50
                for block in current_world.blocks:
                    if isinstance(block, list):
                        for b in block:
                            if b.x == player.x:
                                player.y = b.y - player.height
                    else:
                        if block.x == player.x:
                            player.y = block.y - player.height


        # Update the player's rectangle position again after collision adjustment
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_if_on_block(self):
        blocks = []
        for block_group in current_world.blocks:
            if isinstance(block_group, list):
                blocks.extend(block_group)
            else:
                blocks.append(block_group)

        if hasattr(current_world, 'visible_blocks'):
            blocks.extend(current_world.visible_blocks)

        moving_blocks = []
        if hasattr(current_world, 'moving_blocks'):
            for moving_block in current_world.moving_blocks:
                moving_blocks.append(moving_block[0])

        blocks.extend(moving_blocks)


        on_block = False
        self.block_beneath = None

        if not self.jumping:  # Only check if the player is not jumping
            for block in blocks:
                if (
                        abs(self.rect.bottom - block.top) <= self.speed  # Near or touching the block's top
                        and self.rect.right > block.left  # Horizontally overlapping
                        and self.rect.left < block.right  # Horizontally overlapping
                ):
                    on_block = True
                    self.block_beneath = block
                    break

        if on_block:
            self.jumping = False
            self.jump_velocity = 0

            if self.block_beneath in moving_blocks:
                for moving_block in current_world.moving_blocks:
                    if moving_block[0] == self.block_beneath:
                        self.y = self.block_beneath.top - self.height
                        break

        else:
            self.jumping = True  # Player starts falling if not above a block


    def gravity(self):
        blocks = []
        for block_group in current_world.blocks:
            if isinstance(block_group, list):
                blocks.extend(block_group)
            else:
                blocks.append(block_group)

        if hasattr(current_world, 'visible_blocks'):
            blocks.extend(current_world.visible_blocks)

        if hasattr(current_world, 'moving_blocks'):
            blocks += [block[0] for block in current_world.moving_blocks]


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

        if hasattr(current_world, 'moving_blocks'):
            for moving_block in current_world.moving_blocks:
                if (
                        self.rect.colliderect(moving_block[0])
                        and self.rect.bottom >= moving_block[0].top  # Ensure player is actually landing
                        and self.rect.bottom <= moving_block[0].top + self.jump_velocity + 2  # Account for overshoot
                        and self.rect.right > moving_block[0].left  # Horizontally overlapping
                        and self.rect.left < moving_block[0].right  # Horizontally overlapping
                ):
                    if moving_block[1] == 'up':
                        self.y = moving_block[0].top - self.height
                        self.jumping = False
                        self.jump_velocity = 0
                        break
                    elif moving_block[1] == 'down':
                        self.y = moving_block[0].top - self.height
                        self.jumping = False
                        self.jump_velocity = 0
                        break
                    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_dead(self):
        if self.immune:
            return
        if self.health > 1:
            self._check_collisions(self.draw_hurt_animation)
        else:
            self._check_collisions(self.draw_death_animation)

    def _check_collisions(self, animation_func):
        if self.y > HEIGHT:
            self.y = HEIGHT - self.height
            self._handle_collision(animation_func)
        for attr in ['spikes', 'special_spikes', 'inverted_spikes', 'lava', 'fireballs']:
            if hasattr(current_world, attr):
                for obj in getattr(current_world, attr):
                    if isinstance(obj, list):
                        for sub_obj in obj:
                            if self.rect.colliderect(sub_obj):
                                self._handle_collision(animation_func)
                                break # Prevent multiple collisions
                    elif self.rect.colliderect(obj):
                        self._handle_collision(animation_func)
                        break # Prevent multiple collisions

    def _handle_collision(self, animation_func):
        animation_func()
        self.y = HEIGHT // 2 + 200
        self.x = 50
        self.health -= 1
        if hasattr(current_world, 'regen'):
            current_world.regen()



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
            if world == 1:
                level1.world2_events(player, current_world)

    def check_for_new_world(self):
        global world, current_world
        if self.x > WIDTH:
            world += 1
            current_world = current_level.worlds[world]
            self.x = 25
            for block in current_world.blocks:
                if isinstance(block, list):
                    for b in block:
                        if b.x == self.x:
                            self.y = b.y - self.height + 10
                else:
                    if block.x == self.x:
                        self.y = block.y - self.height + 10
            self.jumping = False
            self.jump_velocity = 0

    def check_0_health(self):
        global level, current_level, current_world, world
        if self.health <= 0:
            options = ['Restart', 'Quit']
            game_over_menu = GameOverMenu(GRAY, options)
            selected_option = game_over_menu.run()
            if selected_option == 1:
                sys.exit()
            current_world = current_level.worlds[0]
            world = 0
            if level == 0:
                level1.level1_start()
                current_level = level_1.Level1()
                current_level.draw_background_once()

            self.events()
            current_world.draw()
            self.x = 25
            for block in current_world.blocks:
                if isinstance(block, list):
                    for b in block:
                        if b.x == self.x:
                            self.y = b.y - self.height
                else:
                    if block.x == self.x:
                        self.y = block.y - self.height
            self.jumping = False
            self.jump_velocity = 0
            self.health = 5
            if hasattr(current_world, 'moving_spike_activated'):
                current_world.moving_spike_activated = False
                if hasattr(current_world, 'inverted_spikes'):
                    current_world.inverted_spikes = [
                        pygame.Rect(WIDTH - 200, -50, 50, 50),
                        pygame.Rect(WIDTH - 150, -50, 50, 50),
                    ]



print(f'Created player object in {time.time() - initial_time} seconds')
pygame.init()
print(f'Initialized pygame in {time.time() - initial_time} seconds')
Clock = pygame.time.Clock()
screen = pygame.display.set_mode()
pygame.display.set_caption("Game Menu")
menu_items = ['Start', 'Quit']
menu = Menu(GRAY, menu_items)
selected = menu.run()
a_or_d = False # Check if the player pressed A or D
space_instructions_done = False # Check if the player pressed SPACE
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
    current_level.draw_background_once()  # Remember to change this when changing to another level
    running = True
    while running:
        current_level.draw_background()
        if level == 0 and not a_or_d:
            if level1.start_instructions(player):
                a_or_d = True
        if level == 0 and not space_instructions_done and a_or_d:
            if level1.space_instructions(player):
                space_instructions_done = True
        player.check_for_new_world()
        keys = pygame.key.get_pressed()
        player.update_position(keys)
        player.gravity()
        player.check_if_on_block()
        current_world.draw()
        player.draw_hearts()
        player.events()
        player.check_dead()
        player.check_0_health()
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

# Ideas:
# Boss Fight
# when reaching the end of world 2 add a barrier to troll the player lol
