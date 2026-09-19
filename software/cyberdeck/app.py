import sys

import pygame

from . import config
from .screens.calculator import CalculatorScreen
from .screens.claude_chat import ClaudeChatScreen
from .screens.documents import DocumentsScreen
from .screens.gallery import GalleryScreen
from .screens.menu import MenuScreen


class CyberdeckApp:
    """Kiosk-Shell (Kap. 8 PROJEKTPLAN.md): genau ein aktiver Screen, keine
    Fensterverwaltung. F1 simuliert die feste Original-Taste "MENU" und
    bringt aus jedem Screen sofort zurueck zum Hauptmenue."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Casio-Cyberdeck (Simulation)")
        self.window = pygame.display.set_mode(
            (config.DISPLAY_WIDTH * config.SCALE, config.DISPLAY_HEIGHT * config.SCALE)
        )
        # Alles wird zuerst auf diese kleine Surface gezeichnet und danach
        # hochskaliert - so bleibt das Layout jedes Screens identisch zur
        # spaeteren echten Displayaufloesung (Kap. 5).
        self.render_surface = pygame.Surface((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()

        self.screens = {
            "menu": MenuScreen(self),
            "calculator": CalculatorScreen(self),
            "gallery": GalleryScreen(self),
            "documents": DocumentsScreen(self),
            "claude": ClaudeChatScreen(self),
        }
        self.current = self.screens["menu"]

    def go_to(self, name: str):
        self.current.on_exit()
        self.current = self.screens[name]
        self.current.on_enter()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(config.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.go_to("menu")
                    elif event.key == pygame.K_ESCAPE and self.current is self.screens["menu"]:
                        running = False
                    else:
                        self.current.handle_key(event)

            self.current.update(dt)
            self.render_surface.fill(config.BG_COLOR)
            self.current.draw(self.render_surface)

            scaled = pygame.transform.scale(
                self.render_surface,
                (config.DISPLAY_WIDTH * config.SCALE, config.DISPLAY_HEIGHT * config.SCALE),
            )
            self.window.blit(scaled, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)
