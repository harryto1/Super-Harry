import sys
from constants.constants import *
from menus.pause_menu import PauseMenu

class GameOverMenu:
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

    def draw(self):
        self.screen.fill(self.bg_color)
        title = self.title_font.render('Game Over', 1, (255, 0, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        for i, item in enumerate(self.menu_items):
            if i == self.selected_item:
                label = self.font.render(item, 1, (255, 255, 255))
            else:
                label = self.font.render(item, 1, self.font_color)
            label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 75))
            self.screen.blit(label, label_rect)
        pygame.display.flip()

    def run(self):
        while self.menu_loop:
            self.clock.tick(60)
            self.draw()
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
        return self.selected_item