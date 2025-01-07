import random

import pygame.time

from constants.constants import *

class Level2:
    block_sprites = []
    spikes_sprites = []
    lava_sprites = []
    fireball_sprites = []
    door_sprite = []
    unlocked_door_sprite = []
    key_sprites = [
        pygame.transform.scale(pygame.image.load('assets/worlds/objects/door_key_1.png'), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/worlds/objects/door_key_1(2).png'), (50, 50))
        ]
    bonus_hearts_sprite = pygame.transform.scale(pygame.image.load('assets/characters/ui/heart_scaled_to_256x256.png'), (35, 35))

    def __init__(self, player):
        self.bg_color = (0, 0, 0)
        self.worlds = [self.World1(player)]
        self.background_surface = pygame.Surface((WIDTH, HEIGHT))
        self.background_spritesheet = pygame.image.load('assets/worlds/background/Dungeon_brick_wall_blue.png.png')
        self.background_sprite = pygame.transform.scale(self.background_spritesheet.subsurface(pygame.Rect(0, 0, 1920, 1080)), (WIDTH, HEIGHT))
        self.block_spritesheet = pygame.image.load('assets/worlds/blocks/blocks.png')
        self.spikes_spritesheet = pygame.image.load('assets/worlds/enemies/16-bit-spike-Sheet.png')
        self.lava_spritesheet = pygame.image.load('assets/worlds/enemies/spritesheet-burninglava.png')
        self.fireball_spritesheet = pygame.image.load('assets/worlds/enemies/Firebolt SpriteSheet.png')
        self.door_spritesheet = pygame.image.load('assets/worlds/background/Tiles.png')
        for i in range(5):
            sprite = self.block_spritesheet.subsurface(pygame.Rect(i * 32, 0, 32, 32))
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.block_sprites.append(sprite)
        for i in range(4):
            sprite = self.spikes_spritesheet.subsurface(pygame.Rect(i * 16, 0, 16, 16))
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.spikes_sprites.append(sprite)
        for i in range(49):
            if 2 < i % 7 < 6:
                sprite = self.lava_spritesheet.subsurface(pygame.Rect(i * 16, 32, 16, 16))
                sprite = pygame.transform.scale(sprite, (50, 50))
                self.lava_sprites.append(sprite)
        for i in range(4):
            sprite = self.fireball_spritesheet.subsurface(pygame.Rect(i * 48, 0, 48, 48))
            sprite = pygame.transform.rotate(sprite, 90)
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.fireball_sprites.append(sprite)
        door_sprite = self.door_spritesheet.subsurface(pygame.Rect(0, 115, 32, 44))
        door_sprite = pygame.transform.scale(door_sprite, (50, 100))
        self.door_sprite.append(door_sprite)
        unlocked_door_sprite = self.door_spritesheet.subsurface(pygame.Rect(0, 159, 32, 44))
        unlocked_door_sprite = pygame.transform.scale(unlocked_door_sprite, (50, 100))
        self.unlocked_door_sprite.append(unlocked_door_sprite)


    def draw_background_once(self):
        self.background_surface.blit(self.background_sprite, (0, 0))
        self.background_surface.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)

    def draw_background(self):
        screen.blit(self.background_surface, (0, 0))

    class Enemy:
        def __init__(self, x, y, speed, idle_spritesheet, motion_spritesheet, death_spritesheet, attack_spritesheet, player, current_world):
            self.x = x
            self.y = y
            self.player = player
            self.width = 35
            self.height = 40
            self.sprite_width = 200
            self.sprite_height = 200
            self.speed = speed
            self.moving = False
            self.facing_left = False
            self.jumping = False
            self.attacking = False
            self.safe = True # To be set to False when Enemy detects a void beneath it
            self.jump_velocity = 0
            self.gravity_force = 1
            self.idle_spritesheet = idle_spritesheet
            self.motion_spritesheet = motion_spritesheet
            self.death_spritesheet = death_spritesheet
            self.attack_spritesheet = attack_spritesheet
            self.idle_frame = 0
            self.motion_frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100
            self.current_world = current_world
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        def draw_idle(self):
            pass
            # To override in subclasses

        def draw_motion(self):
            pass
            # To override in subclasses

        def draw_death(self):
            pass
            # To override in subclasses

        def update_position(self):
            pass

        def check_if_on_block(self):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            moving_blocks = []
            if hasattr(self.current_world, 'moving_blocks'):
                for moving_block in self.current_world.moving_blocks:
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
                    for moving_block in self.current_world.moving_blocks:
                        if moving_block[0] == self.block_beneath:
                            self.y = self.block_beneath.top - self.height
                            break

            else:
                self.jumping = True  # Player starts falling if not above a block


            if hasattr(self.current_world, 'moving_blocks'):
               if self.block_beneath in moving_blocks:
                   for moving_block in self.current_world.moving_blocks:
                       if moving_block[0] == self.block_beneath:
                           if moving_block[1] == 'left':
                               self.x -= 3
                               break
                           elif moving_block[1] == 'right':
                               self.x += 3
                               break

        def gravity(self):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            if hasattr(self.current_world, 'moving_blocks'):
                blocks += [block[0] for block in self.current_world.moving_blocks]

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

            if hasattr(self.current_world, 'moving_blocks'):
                for moving_block in self.current_world.moving_blocks:
                    if (
                            self.rect.colliderect(moving_block[0])
                            and self.rect.bottom >= moving_block[0].top  # Ensure player is actually landing
                            and self.rect.bottom <= moving_block[
                        0].top + self.jump_velocity + 2  # Account for overshoot
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

        def _check_if_on_void(self, rect):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            moving_blocks = []
            if hasattr(self.current_world, 'moving_blocks'):
                for moving_block in self.current_world.moving_blocks:
                    moving_blocks.append(moving_block[0])

            blocks.extend(moving_blocks)

            on_block = False
            block_beneath = None

            if not self.jumping:
                for block in blocks:
                    if (
                            abs(rect.bottom - block.top) <= self.speed  # Near or touching the block's top
                            and rect.right > block.left  # Horizontally overlapping
                            and rect.left < block.right  # Horizontally overlapping
                    ):
                        on_block = True
                        block_beneath = block
                        break

            return on_block, block_beneath


        def _check_if_moving_y_is_safe(self, y):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            moving_blocks = []
            if hasattr(self.current_world, 'moving_blocks'):
                for moving_block in self.current_world.moving_blocks:
                    moving_blocks.append(moving_block[0])

            blocks.extend(moving_blocks)

            self.safe = True
            self.y += y
            next_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            on_block, block_beneath = self._check_if_on_void(next_rect)
            self.y -= y
            if not on_block:
                self.safe = False
            return self.safe



        def check_if_moving_is_safe(self):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            moving_blocks = []
            if hasattr(self.current_world, 'moving_blocks'):
                for moving_block in self.current_world.moving_blocks:
                    moving_blocks.append(moving_block[0])

            blocks.extend(moving_blocks)

            self.safe = True
            if self.facing_left:
                self.x -= 40
            else:
                self.x += 40
            next_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            on_block, block_beneath = self._check_if_on_void(next_rect)
            if not on_block:
                self.safe = False
                for temp_y in range(50, 300):
                    if self._check_if_moving_y_is_safe(temp_y):
                        break
            if self.facing_left:
                self.x += 40
            else:
                self.x -= 40



    class Orc(Enemy):
        idle_spritesheet = pygame.image.load('assets/worlds/enemies/orc/Orc-Idle.png')
        motion_spritesheet = pygame.image.load('assets/worlds/enemies/orc/Orc-Walk.png')
        death_spritesheet = pygame.image.load('assets/worlds/enemies/orc/Orc-Death.png')
        attack_spritesheet = pygame.image.load('assets/worlds/enemies/orc/Orc-Attack01.png')

        def __init__(self, x, y, speed, player, current_world):
            super().__init__(x, y, speed, self.idle_spritesheet, self.motion_spritesheet, self.death_spritesheet, self.attack_spritesheet, player, current_world)
            self.idle_sprites = [self.idle_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100)) for i in range(6)]
            self.motion_sprites = [self.motion_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100)) for i in
                                   range(8)]
            self.death_sprites = [self.death_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100)) for i in
                                  range(4)]
            self.attack_sprites = [self.attack_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100)) for i in
                                   range(6)]

            self.initial_x = x # Initial x position
            self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 200 + (self.width * 2), self.height)
            self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)

            self.following_player = False

            self.attack_frame = 0
            self.attack_last_update = pygame.time.get_ticks()
            self.attack_frame_rate = 50

            self.destination_x = random.randint(self.initial_x - 100, self.initial_x + 100)

            self.player_died = False # To be set to True when the player is hit by the enemy

        def draw_hitbox(self):
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

        def draw_idle(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.idle_frame = (self.idle_frame + 1) % len(self.idle_sprites)
            sprite = pygame.transform.scale(self.idle_sprites[self.idle_frame], (self.sprite_width, self.sprite_height))
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2,
                                 self.y - (self.sprite_height - self.height) + self.height + 45))
            self.draw_hitbox()

        def draw_motion(self):
            if not self.motion_sprites:
                return
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.motion_frame = (self.motion_frame + 1) % len(self.motion_sprites)
            sprite = pygame.transform.scale(self.motion_sprites[self.motion_frame], (self.sprite_width, self.sprite_height))
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2,
                                 self.y - (self.sprite_height - self.height) + self.height + 45))
            self.draw_hitbox()

        def draw_death(self):
            if not self.death_sprites:
                return
            for i in range(4):
                screen.fill(BLACK)
                sprite = pygame.transform.scale(self.death_sprites[i], (self.sprite_width, self.sprite_height))
                if self.facing_left:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2,
                                     self.y - (self.sprite_height - self.height) + self.height + 45))
                pygame.display.update()
                pygame.time.wait(200)

        def draw_attack(self):
            now = pygame.time.get_ticks()
            if now - self.attack_last_update > self.attack_frame_rate:
                self.attack_last_update = now
                self.attack_frame = (self.attack_frame + 1) % len(self.attack_sprites)
                if self.attack_frame == 0:
                    self.attacking = False  # Attack animation finished
                    if self.player_died:
                        if self.player.health > 1:
                            self.player._handle_collision(self.player.draw_hurt_animation)
                            self.player_died = False # Reset player death state after attack animation completes
                        else:
                            self.player._handle_collision(self.player.draw_death_animation)
                            self.player_died = False # Reset player death state after attack animation completes

            # Check if player is within attack range during the entire attack animation
            if abs(self.x - self.player.x) < 35 and abs(self.y - self.player.y) < 50:
                self.player_died = True

            sprite = pygame.transform.scale(self.attack_sprites[self.attack_frame],
                                            (self.sprite_width, self.sprite_height))
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2,
                                 self.y - (self.sprite_height - self.height) + self.height + 45))

        def get_random_path(self):
            self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 200 + (self.width * 2), self.height)
            return random.randint(self.initial_x - 100, self.initial_x + 100)

        def get_random_path_away_from_player(self):
            if self.x - self.player.x > 0:
                self.behavior_zone = pygame.Rect(self.initial_x, self.y, 100 + (self.width * 2), self.height)
                return random.randint(self.initial_x, self.initial_x + 100)
            else:
                self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 100 + (self.width * 2), self.height)
                return random.randint(self.initial_x - 100, self.initial_x)

        def _draw_behavior_zone(self):
            pygame.draw.rect(screen, (0, 0, 255), self.behavior_zone, 2)

        def _draw_attack_zone(self):
            pygame.draw.rect(screen, (128, 0, 128), self.attack_zone, 2)

        def behavior(self):
            if abs(self.x - self.player.x) < 250 and abs(self.y - self.player.y) < 50:
                self.destination_x = self.player.x
                self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)
                self.following_player = True
            elif abs(self.x - self.destination_x) > 150 and self.following_player:
                self.initial_x = self.x
                self.destination_x = self.get_random_path_away_from_player()
                self.following_player = False
            elif random.randint(0, 100) == 0 and not self.moving and not self.attacking:
                self.destination_x = self.get_random_path()
            self._draw_behavior_zone()
            self._draw_attack_zone()

        def update_position(self):
            if self.attacking:
                self.draw_attack()
                return

            if abs(self.x - self.player.x) < 35 and abs(self.y - self.player.y) < 50:
                self.attacking = True
                self.attack_frame = 0
                self.attack_last_update = pygame.time.get_ticks()
                if self.x - self.player.x > 0:
                    self.facing_left = True
                else:
                    self.facing_left = False
                self.moving = False
                self.draw_attack()
                return

            # Wander
            if not self.attacking:
                if abs(self.x - self.destination_x) < self.speed:
                    self.moving = False
                elif self.x < self.destination_x:
                    self.facing_left = False
                    if self.safe:
                        self.x += self.speed
                        self.moving = True
                    else:
                        self.moving = False
                elif self.x > self.destination_x:
                    self.facing_left = True
                    if self.safe:
                        self.x -= self.speed
                        self.moving = True
                    else:
                        self.moving = False
                else:
                    self.moving = False
            self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # Horizontal collision handling
            for attr in ['blocks', 'barrier_blocks', 'visible_blocks', 'moving_blocks',
                         'doors']:  # Remove moving_blocks if bug gets too annoying
                if hasattr(self.current_world, attr):
                    for block in getattr(self.current_world, attr):
                        if attr == 'moving_blocks':
                            block = block[0]
                        if attr == 'doors':
                            if block[1] == 'locked':
                                block = block[0]
                            else:
                                continue  # Prevent collision with unlocked doors
                        if isinstance(block, list):
                            for b in block:
                                if self.rect.colliderect(b):
                                    if self.rect.bottom > b.top and self.rect.top < b.bottom:
                                        if self.facing_left and self.rect.left < b.right and self.rect.right > b.left:
                                            self.x = b.right
                                        elif not self.facing_left and self.rect.right > b.left and self.rect.left < b.right:
                                            self.x = b.left - self.width
                        else:
                            if self.rect.colliderect(block):
                                if self.rect.bottom > block.top and self.rect.top < block.bottom:
                                    if self.facing_left and self.rect.left < block.right and self.rect.right > block.left:
                                        self.x = block.right
                                    elif not self.facing_left and self.rect.right > block.left and self.rect.left < block.right:
                                        self.x = block.left - self.width

            # Update the player's rectangle position after horizontal collision adjustments
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # Vertical collision handling
            for attr in ['blocks', 'barrier_blocks', 'visible_blocks', 'moving_blocks', 'doors']:
                if hasattr(self.current_world, attr):
                    for block in getattr(self.current_world, attr):
                        if attr == 'moving_blocks':
                            block = block[0]
                        if attr == 'doors':
                            if block[1] == 'locked':
                                block = block[0]
                            else:
                                continue  # Prevent collision with unlocked doors
                        if isinstance(block, list):
                            for b in block:
                                if self.rect.colliderect(b):
                                    if self.rect.top < b.bottom and self.rect.bottom > b.top and self.jump_velocity < 0:
                                        self.y = b.bottom
                                        self.jump_velocity = 0
                        else:
                            if self.rect.colliderect(block):
                                if self.rect.top < block.bottom and self.rect.bottom > block.top and self.jump_velocity < 0:
                                    self.y = block.bottom
                                    self.jump_velocity = 0

            # Update the player's rectangle position after vertical collision adjustments
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


        def run(self):
            self.gravity()
            self.check_if_on_block()
            self.check_if_moving_is_safe()
            self.behavior()
            self.update_position()
            if self.moving:
                self.draw_motion()
            elif self.attacking:
                self.draw_attack()
            else:
                self.draw_idle()








    class World1:
        def __init__(self, player):
            self.start_y = HEIGHT - 240
            self.end_y = HEIGHT - 240
            self.player = player
            self.player_died = False # To be set to True when the player is hit by the enemy

            self.blocks = [
                [pygame.Rect(x, y, 50, 50) for x in range(0, WIDTH - 300, 50) for y in range(HEIGHT - 200, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH - 225, WIDTH, 50) for y in range(HEIGHT - 200, HEIGHT, 50)],
                [pygame.Rect(x, HEIGHT // 2 + 150, 50, 50) for x in range(WIDTH // 2 - 100, WIDTH // 2 + 100, 50)]
            ]

            self.enemies = [
                Level2.Orc(WIDTH // 2 + 200, HEIGHT - 240, 2, self.player, self),
                Level2.Orc(WIDTH // 2 - 100, 0, 2, self.player, self)
            ]

        def draw(self):
            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        pygame.draw.rect(screen, (0, 255, 0), b)
                        screen.blit(Level2.block_sprites[0], (b.x, b.y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), block)
                    screen.blit(Level2.block_sprites[0], (block.x, block.y))
            for enemy in self.enemies:
                enemy.run()
                if isinstance(enemy, Level2.Orc):
                    self.player_died = any(enemy.player_died for enemy in self.enemies)


        def regen(self):
            self.enemies = [
                Level2.Orc(WIDTH // 2 + 200, HEIGHT - 240, 2, self.player, self)
            ]
