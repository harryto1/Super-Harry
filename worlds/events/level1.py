
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

def world2_events(player, current_world):
    for moving_block in current_world.moving_blocks:
        if moving_block[0] == player.block_beneath:
            current_world.shake_block(moving_block[0])
            if pygame.time.get_ticks() % 1000 < 20:
                current_world.moving_blocks.remove(moving_block)

    for bonus_heart in current_world.bonus_hearts:
        if player.rect.colliderect(bonus_heart[0]):
            bonus_heart[1] = False
            player.health += 1
            text = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('+1', True, (0, 255, 0))
            text_rect = text.get_rect(center=(bonus_heart[0].centerx, bonus_heart[0].centery - 50))
            screen.blit(text, text_rect)
            current_world.bonus_hearts.remove(bonus_heart)



