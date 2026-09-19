import pygame

from . import base
from .. import config

MENU_ITEMS = [
    ("calculator", "RECHNER"),
    ("gallery", "GALERIE"),
    ("documents", "DATEIEN"),
    ("claude", "CLAUDE"),
]


class MenuScreen(base.Screen):
    """Original-artiges Hauptmenue (Kap. 8): Pfeiltasten + EXE, sonst nichts."""

    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_NORMAL)
        self.font_title = pygame.font.SysFont(
            config.FONT_NAME, config.FONT_SIZE_LARGE, bold=True
        )

    def handle_key(self, event):
        if event.key in (pygame.K_UP, pygame.K_LEFT):
            self.selected = (self.selected - 1) % len(MENU_ITEMS)
        elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
            self.selected = (self.selected + 1) % len(MENU_ITEMS)
        elif event.key == pygame.K_RETURN:
            target, _ = MENU_ITEMS[self.selected]
            self.app.go_to(target)

    def draw(self, surface):
        title = self.font_title.render("CASIO-DECK", True, config.ACCENT_COLOR)
        surface.blit(title, (10, 8))

        start_y = 40
        row_h = 28
        for i, (_, label) in enumerate(MENU_ITEMS):
            y = start_y + i * row_h
            rect = pygame.Rect(10, y, config.DISPLAY_WIDTH - 20, row_h - 6)
            if i == self.selected:
                pygame.draw.rect(surface, config.ACCENT_COLOR, rect, border_radius=2)
                text_color = config.BG_COLOR
            else:
                pygame.draw.rect(surface, config.DIM_COLOR, rect, width=1, border_radius=2)
                text_color = config.FG_COLOR
            text = self.font.render(label, True, text_color)
            surface.blit(text, (rect.x + 8, rect.y + 5))

        hint = self.font.render(
            "Pfeiltasten + ENTER  |  F1=MENU  |  ESC=Beenden", True, config.DIM_COLOR
        )
        surface.blit(hint, (10, config.DISPLAY_HEIGHT - 16))
