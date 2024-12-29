
from constants.constants import *
static_alpha = 255
started_fading = False

def level1_start():
    screen.fill(BLACK)
    title = pygame.font.Font('assets/font/Monocraft.ttf', 72).render('Level 1', 1, (255, 255, 255))
    subtitle = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('The Beginning', 1, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def start_instructions(player):
    global static_alpha, started_fading
    fade_speed = 10  # Adjust the fade speed for faster/slower fading
    title_font = pygame.font.Font(None, 36)  # Font for text
    title_text = 'Use A or D to move!'  # Instruction text

    # Create the text surface
    title = title_font.render(title_text, True, GRAY)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    title_surface = pygame.Surface(title.get_size(), pygame.SRCALPHA)
    title_surface.blit(title, (0, 0))
    title_surface.set_alpha(static_alpha)

    # Update fading only when the player hasn't moved
    if player.x == 100 and not started_fading:  # Player hasn't moved yet
        screen.blit(title_surface, title_rect)
    else:
        started_fading = True
        if static_alpha > 0:
            # Reduce alpha for fading effect
            static_alpha -= fade_speed
            screen.blit(title_surface, title_rect)
        else:
            # Fading completed, return True to indicate movement can proceed
            return True

    return False

def space_instructions(player):
    fade_speed = 5  # Adjust the fade speed for faster/slower fading
    title_font = pygame.font.Font(None, 36)  # Font for text
    title_text = 'Press SPACE to jump!'  # Instruction text

    # Static variables
    if not hasattr(space_instructions, "static_alpha"):
        space_instructions.static_alpha = 255
    if not hasattr(space_instructions, "started_fading"):
        space_instructions.started_fading = False

    # Create the text surface
    title = title_font.render(title_text, True, GRAY)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    title_surface = pygame.Surface(title.get_size(), pygame.SRCALPHA)
    title_surface.blit(title, (0, 0))
    title_surface.set_alpha(space_instructions.static_alpha)

    # Show the instructions if the player hasn't jumped
    if player.y == HEIGHT // 2 + 200 and not space_instructions.started_fading:
        screen.blit(title_surface, title_rect)
    else:
        space_instructions.started_fading = True
        if space_instructions.static_alpha > 0:
            # Reduce alpha for fading effect
            space_instructions.static_alpha -= fade_speed
            screen.blit(title_surface, title_rect)
        else:
            # Fading completed, return True to indicate instructions are done
            return True

    return False


def world1_events(player, current_world):
    if player.rect.x < 0:
        player.rect.x = 0
    if player.rect.x > 250:
        current_world.draw_special_spike(0)
    if player.rect.x < 450:
        current_world.draw_special_spike(1)
    if player.rect.x > 500:
        current_world.special_spikes.pop()
        current_world.special_spikes.append(pygame.Rect(0, HEIGHT // 2 + 190, 50, 50))
    if WIDTH - 300 < player.rect.x < WIDTH - 280:
        if hasattr(current_world, 'moving_spike_activated'):
            current_world.moving_spike_activated = True


disappearing_blocks_2 = []


def world2_events(player, current_world):
    current_time = pygame.time.get_ticks()

    for moving_block in current_world.moving_blocks:
        if moving_block[0] == player.block_beneath:
            current_world.shake_block(moving_block[0])
            if current_time % 1000 < 20:
                current_world.moving_blocks.remove(moving_block)

    global disappearing_blocks_2
    disappearing_blocks_2.clear()  # Clear the list at the start of each call

    for disappearing_block in current_world.disappearing_blocks:
        for i, block in enumerate(disappearing_block):
            if (current_time // 1000) % 2 == 0:
                if i % 2 == 0:
                    disappearing_blocks_2.append(block)
            else:
                if i % 2 != 0:
                    disappearing_blocks_2.append(block)

    current_world.visible_blocks = [block for block in current_world.disappearing_blocks[0] if block not in disappearing_blocks_2]

    for bonus_heart in current_world.bonus_hearts:
        if player.rect.colliderect(bonus_heart[0]):
            bonus_heart[1] = False
            player.health += 1
            text = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('+1', True, (0, 255, 0))
            text_rect = text.get_rect(center=(bonus_heart[0].centerx, bonus_heart[0].centery - 50))
            screen.blit(text, text_rect)
            current_world.bonus_hearts.remove(bonus_heart)

door_unlocked = False # This will be set to True when the player unlocks the door
troll_spike_1_activated = False # This will be set to True when the player reaches a certain point
falling_spike_1_activated = False # This will be set to True when the player reaches a certain point
falling_spike_2_activated = False # This will be set to True when the player reaches a certain point
falling_spike_3_activated = False # This will be set to True when the player reaches a certain point
def world3_events(player, current_world, current_level):
    if player.x > WIDTH - 200:
        global door_unlocked
        if len(player.inventory) == 0 and not door_unlocked:
            text = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('You need a key to unlock this door!', True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(text, text_rect)
        for obj in player.inventory:
            if 'door_key_1' == obj.id:
                text = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('Press E to unlock the door!', True, (0, 255, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                screen.blit(text, text_rect)
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_e]:
                    current_world.doors[0][1] = 'unlocked'
                    player.inventory.remove(obj)
                    door_unlocked = True


    for bonus_heart in current_world.bonus_hearts:
        if player.rect.colliderect(bonus_heart[0]):
            bonus_heart[1] = False
            player.health += 1
            text = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('+1', True, (0, 255, 0))
            text_rect = text.get_rect(center=(bonus_heart[0].centerx, bonus_heart[0].centery - 50))
            screen.blit(text, text_rect)
            current_world.bonus_hearts.remove(bonus_heart)
    if player.x > 450:
        for i in range(len(current_world.moving_blocks)):
            pygame.draw.rect(screen, (0, 0, 255), current_world.moving_blocks[i][0])
            screen.blit(current_level.block_sprites[0], (current_world.moving_blocks[i][0].x, current_world.moving_blocks[i][0].y))
            match i:
                case 3 | 4 | 5:
                    if current_world.moving_blocks[i][1] == 'right':
                        current_world.moving_blocks[i][0].x += 3
                    if current_world.moving_blocks[i][0].x > WIDTH - 250:
                        current_world.moving_blocks[i][1] = 'left'
                    if current_world.moving_blocks[i][1] == 'left':
                        current_world.moving_blocks[i][0].x -= 3
                    if current_world.moving_blocks[i][0].x < 400:
                        current_world.moving_blocks[i][1] = 'right'
    else:
        for i in range(len(current_world.moving_blocks)):
            pygame.draw.rect(screen, (0, 0, 255), current_world.moving_blocks[i][0])
            screen.blit(current_level.block_sprites[0], (current_world.moving_blocks[i][0].x, current_world.moving_blocks[i][0].y))
            match i:
                case 3:
                    if current_world.moving_blocks[i][0].x > 400:
                        current_world.moving_blocks[i][0].x -= 6
                case 4:
                    if current_world.moving_blocks[i][0].x > 450:
                        current_world.moving_blocks[i][0].x -= 6
                case 5:
                    if current_world.moving_blocks[i][0].x > 500:
                        current_world.moving_blocks[i][0].x -= 6

    global troll_spike_1_activated
    if player.x > WIDTH // 3 + WIDTH // 3 + 50:
        troll_spike_1_activated = True
    if troll_spike_1_activated:
        for inverted_spike in current_world.inverted_spikes:
            if isinstance(inverted_spike, list):
                if inverted_spike[1] == 'troll_1':
                    if inverted_spike[0].y < HEIGHT + 100:
                        inverted_spike[0].y += 15

    if player.x > WIDTH - 410:
        for i in range(len(current_world.moving_blocks)):
            pygame.draw.rect(screen, (0, 0, 255), current_world.moving_blocks[i][0])
            screen.blit(current_level.block_sprites[0], (current_world.moving_blocks[i][0].x, current_world.moving_blocks[i][0].y))
            match i:
                case 6 | 7 | 8:
                    if current_world.moving_blocks[i][1] == 'up':
                        current_world.moving_blocks[i][0].y -= 3
                    if current_world.moving_blocks[i][0].y < 75:
                        current_world.moving_blocks[i][1] = 'down'
                    if current_world.moving_blocks[i][1] == 'down':
                        current_world.moving_blocks[i][0].y += 3
                    if current_world.moving_blocks[i][0].y > HEIGHT - 50:
                        current_world.moving_blocks[i][1] = 'up'
    else:
        for i in range(len(current_world.moving_blocks)):
            pygame.draw.rect(screen, (0, 0, 255), current_world.moving_blocks[i][0])
            screen.blit(current_level.block_sprites[0], (current_world.moving_blocks[i][0].x, current_world.moving_blocks[i][0].y))
            match i:
                case 6:
                    if current_world.moving_blocks[i][0].y < HEIGHT - 100:
                        current_world.moving_blocks[i][0].y += 3
                case 7:
                    if current_world.moving_blocks[i][0].y < HEIGHT - 100:
                        current_world.moving_blocks[i][0].y += 3
                case 8:
                    if current_world.moving_blocks[i][0].y < HEIGHT - 100:
                        current_world.moving_blocks[i][0].y += 3

    global falling_spike_1_activated, falling_spike_2_activated, falling_spike_3_activated
    if falling_spike_1_activated:
        for inverted_spike in current_world.inverted_spikes:
            if isinstance(inverted_spike, list):
                if inverted_spike[1] == 'falling_spike_1':
                    if inverted_spike[0].y < HEIGHT + 100:
                        inverted_spike[0].y += 15

    if falling_spike_2_activated:
        for inverted_spike in current_world.inverted_spikes:
            if isinstance(inverted_spike, list):
                if inverted_spike[1] == 'falling_spike_2':
                    if inverted_spike[0].y < HEIGHT + 100:
                        inverted_spike[0].y += 15

    if falling_spike_3_activated:
        for inverted_spike in current_world.inverted_spikes:
            if isinstance(inverted_spike, list):
                if inverted_spike[1] == 'falling_spike_3':
                    if inverted_spike[0].y < HEIGHT + 100:
                        inverted_spike[0].y += 15

    if player.x > WIDTH - 400 and player.y < HEIGHT - 500:
        falling_spike_1_activated = True

    if player.x > WIDTH - 400 and player.y < HEIGHT - 600:
        falling_spike_2_activated = True

    if player.x > WIDTH - 400 and player.y < HEIGHT - 700:
        falling_spike_3_activated = True

RAINBOW_COLORS = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]
def level1_end(current_level):
    screen.fill(BLACK)
    current_level.draw_background_once()

    def cycle_colors(colors):
        return colors[1:] + [colors[0]]

    def animate_text():
        font = pygame.font.Font('assets/font/Monocraft.ttf', 72)
        text = 'Congratulations!'
        text_surfaces = [font.render(char, True, RAINBOW_COLORS[i % len(RAINBOW_COLORS)]) for i, char in enumerate(text)]
        text_rects = [surface.get_rect() for surface in text_surfaces]
        total_width = sum(rect.width for rect in text_rects)
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 - 50

        initial_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - initial_time < 3000:
            current_level.draw_background()
            x = start_x
            for surface, rect in zip(text_surfaces, text_rects):
                rect.topleft = (x, y)
                screen.blit(surface, rect)
                x += rect.width
            pygame.display.flip()
            global RAINBOW_COLORS
            RAINBOW_COLORS = cycle_colors(RAINBOW_COLORS)
            text_surfaces = [font.render(char, True, RAINBOW_COLORS[i % len(RAINBOW_COLORS)]) for i, char in enumerate(text)]
            pygame.time.wait(50)

    animate_text()












