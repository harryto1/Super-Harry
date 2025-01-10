from constants.constants import *
from worlds.objects.sword import Sword

static_alpha = 255
started_fading = False

def level2_start():
    screen.fill(BLACK)
    title = pygame.font.Font('assets/font/Monocraft.ttf', 72).render('Level 2', 1, (255, 255, 255))
    subtitle = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('Placeholder for a level description', 1, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def sword_instructions(player, keys):
    fade_speed = 3  # Adjust the fade speed for faster/slower fading
    title_font = pygame.font.Font(None, 36)  # Font for text
    title_text = 'Press F to attack!'  # Instruction text

    # Static variables
    if not hasattr(sword_instructions, "static_alpha"):
        sword_instructions.static_alpha = 255
    if not hasattr(sword_instructions, "started_fading"):
        sword_instructions.started_fading = False

    # Create the text surface
    title = title_font.render(title_text, True, DARK_RED)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    title_surface = pygame.Surface(title.get_size(), pygame.SRCALPHA)
    title_surface.blit(title, (0, 0))
    title_surface.set_alpha(sword_instructions.static_alpha)

    # Show the instructions if the player hasn't jumped
    if any(isinstance(obj, Sword) for obj in player.inventory) and not sword_instructions.started_fading:
        if not keys[pygame.K_f]:
            screen.blit(title_surface, title_rect)
        else:
            sword_instructions.started_fading = True

    if sword_instructions.started_fading:
        if sword_instructions.static_alpha > 0:
            # Reduce alpha for fading effect
            sword_instructions.static_alpha -= fade_speed
            title_surface.set_alpha(sword_instructions.static_alpha)
            screen.blit(title_surface, title_rect)
        else:
            # Fading completed, return True to indicate instructions are done
            return True

    return False
