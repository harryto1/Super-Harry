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
        def __init__(self, x, y, speed, idle_spritesheet, motion_spritesheet, death_spritesheet, attack_spritesheet, player):
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


    class Orc(Enemy):
        def __init__(self, x, y, speed, idle_spritesheet, motion_spritesheet, death_spritesheet, attack_spritesheet, player):
            super().__init__(x, y, speed, idle_spritesheet, motion_spritesheet, death_spritesheet, attack_spritesheet, player)
            self.idle_sprites = []
            for i in range(6):
                sprite = idle_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
                self.idle_sprites.append(sprite)
            self.motion_sprites = []
            for i in range(8):
                sprite = motion_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
                self.motion_sprites.append(sprite)
            self.death_sprites = []
            for i in range(4):
                sprite = death_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
                self.death_sprites.append(sprite)
            self.attack_sprites = []
            for i in range(6):
                sprite = attack_spritesheet.subsurface(pygame.Rect(i * 100, 0, 100, 100))
                self.attack_sprites.append(sprite)

            self.initial_x = x # Initial x position
            self.behavior_zone = pygame.Rect(self.initial_x - 100, self.y, 200 + (self.width * 2), self.height)
            self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)

            self.following_player = False

            self.attack_frame = 0
            self.attack_last_update = pygame.time.get_ticks()
            self.attack_frame_rate = 50

            self.destination_x = random.randint(self.initial_x - 100, self.initial_x + 100)

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
                    if self.facing_left:
                        if self.x - self.player.x > 10:
                            if self.player.health > 1:
                                self.player._handle_collision(self.player.draw_hurt_animation)
                            else:
                                self.player._handle_collision(self.player.draw_death_animation)
                    else:
                        if self.x - self.player.x < 10:
                            if self.player.health > 1:
                                self.player._handle_collision(self.player.draw_hurt_animation)
                            else:
                                self.player._handle_collision(self.player.draw_death_animation)
                    self.attacking = False  # Attack animation finished
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

            if abs(self.x - self.player.x) < 50 and abs(self.y - self.player.y) < 50:
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
                    self.x += self.speed
                elif self.x > self.destination_x:
                    self.facing_left = True
                    self.x -= self.speed
                else:
                    self.moving = False
            self.attack_zone = pygame.Rect(self.x - 200, self.y, 450, self.height)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


        def run(self):
            self.update_position()
            self.behavior()
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

            self.blocks = [
                [pygame.Rect(x, y, 50, 50) for x in range(0, WIDTH, 50) for y in range(HEIGHT - 200, HEIGHT, 50)]
            ]

            self.enemies = [
                Level2.Orc(WIDTH // 2 + 200, HEIGHT - 240, 2, pygame.image.load('assets/worlds/enemies/orc/Orc-Idle.png'), pygame.image.load('assets/worlds/enemies/orc/Orc-Walk.png'), pygame.image.load('assets/worlds/enemies/orc/Orc-Death.png'), pygame.image.load('assets/worlds/enemies/orc/Orc-Attack01.png'), self.player)
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

        def regen(self):
            self.enemies = [
                Level2.Orc(WIDTH // 2 + 200, HEIGHT - 240, 2, pygame.image.load('assets/worlds/enemies/orc/Orc-Idle.png'), pygame.image.load('assets/worlds/enemies/orc/Orc-Walk.png'), pygame.image.load('assets/worlds/enemies/orc/Orc-Death.png'), pygame.image.load('assets/worlds/enemies/orc/Orc-Attack01.png'), self.player)
            ]