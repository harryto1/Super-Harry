import random

import pygame.time

from constants.constants import *
from worlds.objects.sword import Sword

class Level2:
    block_sprites = []
    spikes_sprites = []
    lava_sprites = []
    fireball_sprites = []
    door_sprite = []
    unlocked_door_sprite = []
    sword_sprite = pygame.transform.scale(pygame.image.load('assets/worlds/objects/sword_asset.png'), (50, 50))
    key_sprites = [
        pygame.transform.scale(pygame.image.load('assets/worlds/objects/door_key_1.png'), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/worlds/objects/door_key_1(2).png'), (50, 50))
        ]
    bonus_hearts_sprite = pygame.transform.scale(pygame.image.load('assets/characters/ui/heart_scaled_to_256x256.png'), (35, 35))

    def __init__(self, player):
        self.bg_color = (0, 0, 0)
        self.worlds = [self.World1(player), self.World2(player)]
        self.background_surface = pygame.Surface((WIDTH, HEIGHT))
        self.background_spritesheets = ['assets/worlds/background/plx-1.png', 'assets/worlds/background/plx-2.png', 'assets/worlds/background/plx-3.png', 'assets/worlds/background/plx-4.png', 'assets/worlds/background/plx-5.png']
        self.background_sprites = [pygame.transform.scale(pygame.image.load(sheet).subsurface(pygame.Rect(0, 0, 384, 216)), (WIDTH, HEIGHT)) for sheet in self.background_spritesheets]
        self.block_spritesheet = pygame.image.load('assets/worlds/blocks/world_tileset.png')
        self.spikes_spritesheet = pygame.image.load('assets/worlds/enemies/16-bit-spike-Sheet.png')
        self.lava_spritesheet = pygame.image.load('assets/worlds/enemies/spritesheet-burninglava.png')
        self.fireball_spritesheet = pygame.image.load('assets/worlds/enemies/Firebolt SpriteSheet.png')
        self.door_spritesheet = pygame.image.load('assets/worlds/background/Tiles.png')
        for i in range(3):
            sprite = self.block_spritesheet.subsurface(pygame.Rect(0, i * 16, 16, 16))
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
        for sprite in self.background_sprites:
            self.background_surface.blit(sprite, (0, 0))
        self.background_surface.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_MULT)

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
            self.should_I_jump = False # To be set to True when Enemy detects he can jump lol
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

            self.initial_x = x # Initial x position
            self.destination_x = random.randint(self.initial_x - 100, self.initial_x + 100)
            self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 200 + (self.width * 2), self.height)




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

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

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

        def get_random_path(self):
            self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 200 + (self.width * 2), self.height)
            return random.randint(self.initial_x - 100, self.initial_x + 100)


        def gravity(self):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

            if hasattr(self.current_world, 'moving_blocks'):
                blocks.extend([block[0] for block in self.current_world.moving_blocks])

            if self.jumping:
                # Calculate new vertical position
                new_y = self.y + self.jump_velocity
                # Calculate new horizontal position based on facing direction
                new_x = self.x - self.speed if self.facing_left else self.x + self.speed

                self.jump_velocity += self.gravity_force

                # First check vertical collision
                vertical_collision = False
                test_rect_vertical = pygame.Rect(self.x, new_y, self.width, self.height)

                for block in blocks:
                    if test_rect_vertical.colliderect(block):
                        if self.jump_velocity < 0 and test_rect_vertical.top <= block.bottom:  # Hitting ceiling
                            self.y = block.bottom
                            self.jump_velocity = 0
                            vertical_collision = True
                            break
                        elif self.jump_velocity > 0 and test_rect_vertical.bottom >= block.top:  # Landing
                            self.y = block.top - self.height
                            self.jumping = False
                            self.jump_velocity = 0
                            vertical_collision = True
                            break

                if not vertical_collision:
                    self.y = new_y

                # Then check horizontal collision
                horizontal_collision = False
                test_rect_horizontal = pygame.Rect(new_x, self.y, self.width, self.height)

                for block in blocks:
                    if test_rect_horizontal.colliderect(block):
                        horizontal_collision = True
                        # If we hit a wall while jumping, stop horizontal movement but continue vertical
                        if self.facing_left:
                            self.x = block.right
                            self.destination_x = self.get_random_path()
                        else:
                            self.x = block.left - self.width
                            self.destination_x = self.get_random_path()
                        break

                if not horizontal_collision:
                    self.x = new_x

            # Update rectangle position
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


        def has_line_of_sight(self):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

            if hasattr(self.current_world, 'moving_blocks'):
                blocks.extend([block[0] for block in self.current_world.moving_blocks])

            player_center = (
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2
            )
            orc_center = (
                self.x + self.width // 2,
                self.y + self.height // 2
            )

            # Check if any block intersects the line between orc and player
            for block in blocks:
                if block.clipline(orc_center, player_center):
                    return False

            return True

        def _check_if_on_void(self, rect):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

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

        def check_if_I_should_jump(self, y):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

            moving_blocks = []
            if hasattr(self.current_world, 'moving_blocks'):
                for moving_block in self.current_world.moving_blocks:
                    moving_blocks.append(moving_block[0])

            blocks.extend(moving_blocks)

            self.should_I_jump = False
            self.y -= y
            if self.facing_left:
                self.x -= 40
            else:
                self.x += 40
            next_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            on_block, block_beneath = self._check_if_on_void(next_rect)
            self.y += y
            if self.facing_left:
                self.x += 40
            else:
                self.x -= 40
            if on_block:
                if not self.jumping:
                    self.should_I_jump = True


        def _check_if_moving_y_is_safe(self, y):
            blocks = []
            for block_group in self.current_world.blocks:
                if isinstance(block_group, list):
                    blocks.extend(block_group)
                else:
                    blocks.append(block_group)

            if hasattr(self.current_world, 'visible_blocks'):
                blocks.extend(self.current_world.visible_blocks)

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

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

            if hasattr(self.current_world, 'grass_blocks'):
                for grass_block in self.current_world.grass_blocks:
                    blocks.extend(grass_block)

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

            self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 200 + (self.width * 2), self.height)
            self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)

            self.following_player = False

            self.attack_frame = 0
            self.attack_last_update = pygame.time.get_ticks()
            self.attack_frame_rate = 50

            self.death_frame = 0
            self.death_last_update = pygame.time.get_ticks()
            self.death_frame_rate = 50

            self.player_died = False # To be set to True when the player is hit by the enemy
            self.orc_died = False # To be set to True when orc is hit by the player
            self.orc_dn_exist = False

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
            if not self.orc_died:
                return
            now = pygame.time.get_ticks()
            if now - self.death_last_update > self.death_frame_rate:
                self.death_last_update = now
                self.death_frame = (self.death_frame + 1) % len(self.death_sprites)
                if self.death_frame == 0:
                    self.orc_dn_exist = True

            sprite = pygame.transform.scale(self.death_sprites[self.death_frame],
                                            (self.sprite_width, self.sprite_height))
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.x - (self.sprite_width - self.width) // 2,
                                 self.y - (self.sprite_height - self.height) + self.height + 45))

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
            if abs(self.x - self.player.x) < 250 and abs(self.y - self.player.y) < 50 and self.has_line_of_sight():
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
            if self.orc_died:
                self.draw_death()
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

            # Wander behavior
            if not self.attacking:
                if abs(self.x - self.destination_x) < self.speed:
                    self.moving = False
                elif self.x < self.destination_x:
                    if not self.jumping:
                        self.facing_left = False
                    if self.safe:
                        self.x += self.speed
                        self.moving = True
                        if self.should_I_jump and not self.jumping:
                            self.jump_velocity = -15
                            self.jumping = True
                    else:
                        self.moving = False
                elif self.x > self.destination_x:
                    if not self.jumping:
                        self.facing_left = True
                    if self.safe:
                        self.x -= self.speed
                        self.moving = True
                        if self.should_I_jump and not self.jumping:
                            self.jump_velocity = -15
                            self.jumping = True
                    else:
                        self.moving = False
                else:
                    self.moving = False

            self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # Horizontal collision handling
            for attr in ['blocks', 'barrier_blocks', 'visible_blocks', 'moving_blocks', 'doors', 'grass_blocks']:
                if hasattr(self.current_world, attr):
                    blocks = getattr(self.current_world, attr)
                    if not isinstance(blocks, list):
                        blocks = [blocks]

                    for block in blocks:
                        if attr == 'moving_blocks':
                            block = block[0]
                        if attr == 'doors':
                            if block[1] == 'locked':
                                block = block[0]
                            else:
                                continue

                        if isinstance(block, list):
                            collision_blocks = block
                        else:
                            collision_blocks = [block]

                        for b in collision_blocks:
                            if self.rect.colliderect(b):
                                if self.rect.bottom > b.top and self.rect.top < b.bottom:
                                    if self.facing_left and self.rect.left < b.right:
                                        self.x = b.right
                                    elif not self.facing_left and self.rect.right > b.left:
                                        self.x = b.left - self.width

            # Update rectangle after horizontal collisions
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

            # Vertical collision handling (revised)
            for attr in ['blocks', 'barrier_blocks', 'visible_blocks', 'moving_blocks', 'doors' 'grass_blocks']:
                if hasattr(self.current_world, attr):
                    blocks = getattr(self.current_world, attr)
                    if not isinstance(blocks, list):
                        blocks = [blocks]

                    for block in blocks:
                        if attr == 'moving_blocks':
                            block = block[0]
                        if attr == 'doors':
                            if block[1] == 'locked':
                                block = block[0]
                            else:
                                continue

                        if isinstance(block, list):
                            collision_blocks = block
                        else:
                            collision_blocks = [block]

                        for b in collision_blocks:
                            if self.rect.colliderect(b):
                                # Handle collision with block top (falling)
                                if self.jump_velocity > 0 and self.rect.bottom >= b.top and self.rect.top < b.top:
                                    self.y = b.top - self.height
                                    self.jumping = False
                                    self.jump_velocity = 0
                                # Handle collision with block bottom (jumping)
                                elif self.jump_velocity < 0 and self.rect.top <= b.bottom and self.rect.bottom > b.bottom:
                                    self.y = b.bottom
                                    self.jump_velocity = 0

            # Final rectangle update
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


        def run(self):
            self.gravity()
            self.check_if_on_block()
            self.check_if_moving_is_safe()
            self.check_if_I_should_jump(50)
            self.behavior()
            self.update_position()
            if self.orc_died:
                self.draw_death()
            elif self.moving:
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

            self.grass_blocks = [
                [pygame.Rect(x, HEIGHT - 200, 50, 50) for x in range(0, 500, 50)],
                [pygame.Rect(x, HEIGHT - 250, 50, 50) for x in range(500, WIDTH // 3 + 100, 50)],
                [pygame.Rect(x, HEIGHT - 300, 50, 50) for x in range(WIDTH // 3 + 110, WIDTH // 2, 50)],
                [pygame.Rect(x, HEIGHT - 350, 50, 50) for x in range(WIDTH // 2 + 40, WIDTH // 2 + 200, 50)],
                [pygame.Rect(x, HEIGHT - 450, 50, 50) for x in range(WIDTH // 2 + 240, WIDTH // 2 + 350, 50)],
                [pygame.Rect(x, HEIGHT - 350, 50, 50) for x in range(WIDTH // 2 + 390, WIDTH * 2//3 + 200, 50)],
                [pygame.Rect(x, HEIGHT - 250, 50, 50) for x in range(WIDTH * 2//3 + 220, WIDTH - 240, 50)],
                [pygame.Rect(x, HEIGHT - 200, 50, 50) for x in range(WIDTH - 220, WIDTH, 50)],
            ]

            self.blocks = [
                [pygame.Rect(x, y, 50, 50) for x in range(0, 500, 50) for y in range(HEIGHT - 150, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(500, WIDTH // 3 + 100, 50) for y in range(HEIGHT - 200, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH // 3 + 110, WIDTH // 2, 50) for y in range(HEIGHT - 250, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH // 2 + 40, WIDTH // 2 + 200, 50) for y in range(HEIGHT - 300, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH // 2 + 240, WIDTH // 2 + 350, 50) for y in range(HEIGHT - 400, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH // 2 + 390, WIDTH * 2//3 + 200, 50) for y in range(HEIGHT - 300, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH * 2//3 + 220, WIDTH - 240, 50) for y in range(HEIGHT - 200, HEIGHT, 50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH - 220, WIDTH, 50) for y in range(HEIGHT - 150, HEIGHT, 50)],
                [pygame.Rect(x, HEIGHT - 565, 50, 50) for x in range(WIDTH // 3 + 260, WIDTH // 2 + 150, 50)],
                [pygame.Rect(x, HEIGHT - 615, 50, 50) for x in range(WIDTH // 3 - 150, WIDTH // 3 + 100, 50)]

            ]

            self.enemies = [
                Level2.Orc(WIDTH // 3, HEIGHT - 300, 2, self.player, self),
                Level2.Orc(WIDTH // 2 - 100, HEIGHT - 350, 2, self.player, self),
                Level2.Orc(WIDTH * 2//3 + 165 , HEIGHT - 350, 2, self.player, self)
            ]

            self.bonus_hearts = [
                [pygame.Rect(WIDTH // 3 - 50, HEIGHT - 665, 50, 50), True]
            ]

            self.objects = [
                Sword('sword', Level2.sword_sprite, pygame.Rect(WIDTH - 100, HEIGHT - 250, 50, 50))
            ]

        def draw(self):
            for grass_block in self.grass_blocks:
                if isinstance(grass_block, list):
                    for block in grass_block:
                        screen.blit(Level2.block_sprites[0], (block.x, block.y))
                else:
                    screen.blit(Level2.block_sprites[0], (grass_block.x, grass_block.y))

            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        screen.blit(Level2.block_sprites[1], (b.x, b.y))
                else:
                    screen.blit(Level2.block_sprites[1], (block.x, block.y))

            for enemy in self.enemies:
                enemy.run()
                if isinstance(enemy, Level2.Orc):
                    self.player_died = any(enemy.player_died for enemy in self.enemies)
                if isinstance(enemy, Level2.Orc):
                    if enemy.orc_dn_exist:
                        self.enemies.remove(enemy)

            for obj in self.objects:
                if not obj.in_inventory:
                    obj.draw()

            for heart in self.bonus_hearts:
                if heart[1]:
                    pygame.draw.rect(screen, (255, 0, 0), heart[0], 2)
                    screen.blit(Level2.bonus_hearts_sprite, (
                    heart[0].x + (heart[0].width - Level2.bonus_hearts_sprite.get_width()) // 2,
                    heart[0].y + (heart[0].height - Level2.bonus_hearts_sprite.get_height()) // 2))

        def regen(self):
            self.enemies = [
                Level2.Orc(WIDTH // 3, HEIGHT - 300, 2, self.player, self),
                Level2.Orc(WIDTH // 2 - 100, HEIGHT - 350, 2, self.player, self),
                Level2.Orc(WIDTH * 2 // 3 + 165, HEIGHT - 350, 2, self.player, self)

            ]

    class World2:
        def __init__(self, player):
            self.start_y = HEIGHT - 240
            self.end_y = HEIGHT - 240
            self.player = player
            self.player_died = False # To be set to True when the player is hit by the enemy

            self.grass_blocks = [
                [pygame.Rect(x, HEIGHT - 200, 50, 50) for x in range(0, 400, 50)],
                [pygame.Rect(x, HEIGHT - 200, 50, 50) for x in range(450, 750, 50)],
                [pygame.Rect(x, HEIGHT - 250, 50, 50) for x in range(WIDTH // 2 - 100, WIDTH // 2 + 100, 50)]
            ]

            self.blocks = [
                [pygame.Rect(x, y, 50, 50) for x in range(0, 400, 50) for y in range(HEIGHT - 150, HEIGHT, 50)],
                pygame.Rect(200, HEIGHT - 250, 50, 50),
                [pygame.Rect(250, y, 50, 50) for y in range(HEIGHT - 250, HEIGHT - 350, -50)],
                [pygame.Rect(300, y, 50, 50) for y in range(HEIGHT - 250, HEIGHT - 400, -50)],
                [pygame.Rect(350, y, 50, 50) for y in range(HEIGHT- 250, HEIGHT - 450, -50)],
                [pygame.Rect(x, y, 50, 50) for x in range(450, 750, 50) for y in range(HEIGHT - 150, HEIGHT, 50)],
                [pygame.Rect(450, y, 50, 50) for y in range(HEIGHT - 250, HEIGHT - 450, -50)],
                [pygame.Rect(500, y, 50, 50) for y in range(HEIGHT - 250, HEIGHT - 400, -50)],
                [pygame.Rect(550, y, 50, 50) for y in range(HEIGHT - 250, HEIGHT- 350, -50)],
                [pygame.Rect(600, y, 50, 50) for y in range(HEIGHT- 250, HEIGHT - 300, -50)],
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH // 2 - 100, WIDTH // 2 + 100, 50) for y in range(HEIGHT - 200, HEIGHT, 50)]


            ]

            self.enemies = [
                Level2.Orc(300, HEIGHT - 450, 2, self.player, self),
                Level2.Orc(450, HEIGHT - 450, 2, self.player, self)
            ]

        def draw(self):
            for grass_block in self.grass_blocks:
                if isinstance(grass_block, list):
                    for block in grass_block:
                        screen.blit(Level2.block_sprites[0], (block.x, block.y))
                else:
                    screen.blit(Level2.block_sprites[0], (grass_block.x, grass_block.y))

            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        screen.blit(Level2.block_sprites[1], (b.x, b.y))
                else:
                    screen.blit(Level2.block_sprites[1], (block.x, block.y))

            for enemy in self.enemies:
                enemy.run()
                if isinstance(enemy, Level2.Orc):
                    self.player_died = any(enemy.player_died for enemy in self.enemies)
                if isinstance(enemy, Level2.Orc):
                    if enemy.orc_dn_exist:
                        self.enemies.remove(enemy)

        def regen(self):
            self.enemies = [
                Level2.Orc(300, HEIGHT - 450, 2, self.player, self),
                Level2.Orc(450, HEIGHT - 450, 2, self.player, self)

            ]