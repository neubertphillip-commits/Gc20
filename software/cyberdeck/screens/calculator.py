import math

import pygame

from . import base
from .. import config
from ..mathengine import CalculatorError, safe_eval

_INPUT_CHARS = set("0123456789.+-*/%()^,!")


class CalculatorScreen(base.Screen):
    """Wissenschaftlicher Rechner + einfacher Funktionsplot (Kap. 9.1).

    Drei Modi: normale Berechnung ("calc"), Eingabe einer Funktion f(x)
    ("graph_input") und deren Plot mit Pan/Zoom ("graph_view")."""

    def __init__(self, app):
        super().__init__(app)
        self.mode = "calc"
        self.expr = ""
        self.result = None
        self.error = None
        self.angle_mode = "deg"
        self.ans = 0.0
        self.memory = 0.0

        self.graph_expr = "sin(x)"
        self.x_min, self.x_max = -10.0, 10.0
        self.y_min, self.y_max = -10.0, 10.0

        self.font_expr = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_NORMAL)
        self.font_result = pygame.font.SysFont(
            config.FONT_NAME, config.FONT_SIZE_LARGE, bold=True
        )
        self.font_hint = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SMALL)

    # -- Eingabe -----------------------------------------------------

    def handle_key(self, event):
        if self.mode == "graph_input":
            self._handle_graph_input_key(event)
        elif self.mode == "graph_view":
            self._handle_graph_view_key(event)
        else:
            self._handle_calc_key(event)

    def _type_char(self, buf, event):
        if event.unicode and (event.unicode.isalpha() or event.unicode in _INPUT_CHARS):
            return buf + event.unicode.lower()
        return buf

    def _handle_calc_key(self, event):
        if event.key == pygame.K_RETURN:
            self._evaluate()
        elif event.key == pygame.K_BACKSPACE:
            self.expr = self.expr[:-1]
            self.error = None
        elif event.key == pygame.K_DELETE:
            self.expr, self.result, self.error = "", None, None
        elif event.key == pygame.K_F2:
            self.angle_mode = "rad" if self.angle_mode == "deg" else "deg"
        elif event.key == pygame.K_F3:
            self.expr += "ans"
        elif event.key == pygame.K_F4:
            if self.result is not None:
                self.memory += self.result
        elif event.key == pygame.K_F5:
            self.expr += "mem"
        elif event.key == pygame.K_F6:
            self.memory = 0.0
        elif event.key == pygame.K_F7:
            self.mode = "graph_input"
        else:
            self.expr = self._type_char(self.expr, event)
            self.error = None

    def _handle_graph_input_key(self, event):
        if event.key == pygame.K_RETURN and self.graph_expr.strip():
            self.mode = "graph_view"
        elif event.key == pygame.K_BACKSPACE:
            self.graph_expr = self.graph_expr[:-1]
        elif event.key in (pygame.K_ESCAPE, pygame.K_F7):
            self.mode = "calc"
        elif event.key == pygame.K_DELETE:
            self.graph_expr = ""
        else:
            self.graph_expr = self._type_char(self.graph_expr, event)

    def _handle_graph_view_key(self, event):
        span_x = self.x_max - self.x_min
        span_y = self.y_max - self.y_min
        if event.key == pygame.K_LEFT:
            self.x_min -= span_x * 0.2
            self.x_max -= span_x * 0.2
        elif event.key == pygame.K_RIGHT:
            self.x_min += span_x * 0.2
            self.x_max += span_x * 0.2
        elif event.key == pygame.K_UP:
            self.y_min += span_y * 0.2
            self.y_max += span_y * 0.2
        elif event.key == pygame.K_DOWN:
            self.y_min -= span_y * 0.2
            self.y_max -= span_y * 0.2
        elif event.unicode == "+":
            self._zoom(0.8)
        elif event.unicode == "-":
            self._zoom(1.25)
        elif event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_F7):
            self.mode = "graph_input"

    def _zoom(self, factor):
        cx = (self.x_min + self.x_max) / 2
        cy = (self.y_min + self.y_max) / 2
        hw = (self.x_max - self.x_min) / 2 * factor
        hh = (self.y_max - self.y_min) / 2 * factor
        self.x_min, self.x_max = cx - hw, cx + hw
        self.y_min, self.y_max = cy - hh, cy + hh

    def _evaluate(self):
        if not self.expr.strip():
            return
        try:
            value = safe_eval(
                self.expr,
                angle_mode=self.angle_mode,
                variables={"ans": self.ans, "mem": self.memory},
            )
        except ZeroDivisionError:
            self.result, self.error = None, "Division durch 0"
        except (CalculatorError, ValueError, OverflowError) as exc:
            self.result, self.error = None, str(exc) or "Rechenfehler"
        else:
            self.result, self.error = value, None
            self.ans = value

    # -- Darstellung ---------------------------------------------------

    def draw(self, surface):
        if self.mode == "graph_input":
            self._draw_graph_input(surface)
        elif self.mode == "graph_view":
            self._draw_graph_view(surface)
        else:
            self._draw_calc(surface)

    def _draw_calc(self, surface):
        pygame.draw.rect(surface, config.DIM_COLOR, (0, 0, config.DISPLAY_WIDTH, 20), width=1)

        expr_surf = self.font_expr.render(self.expr or " ", True, config.FG_COLOR)
        surface.blit(expr_surf, (6, 4))

        status = self.angle_mode.upper() + (" M" if self.memory else "")
        status_surf = self.font_hint.render(status, True, config.ACCENT_COLOR)
        surface.blit(status_surf, (config.DISPLAY_WIDTH - status_surf.get_width() - 6, 4))

        if self.error:
            res_surf = self.font_result.render(self.error, True, config.ERROR_COLOR)
        elif self.result is not None:
            res_surf = self.font_result.render(f"= {self.result:g}", True, config.ACCENT_COLOR)
        else:
            res_surf = self.font_result.render("", True, config.ACCENT_COLOR)
        surface.blit(res_surf, (6, 28))

        hint1 = self.font_hint.render(
            "sin cos tan asin..atanh log ln sqrt cbrt fact npr ncr root",
            True,
            config.DIM_COLOR,
        )
        surface.blit(hint1, (6, config.DISPLAY_HEIGHT - 28))
        hint2 = self.font_hint.render(
            "ENTER=EXE ENTF=Clear F2=Grad/Rad F3=ANS F4=M+ F5=MR F6=MC F7=Graph",
            True,
            config.DIM_COLOR,
        )
        surface.blit(hint2, (6, config.DISPLAY_HEIGHT - 14))

    def _draw_graph_input(self, surface):
        title = self.font_hint.render("GRAPH-MODUS: y = f(x)", True, config.ACCENT_COLOR)
        surface.blit(title, (6, 6))
        expr_surf = self.font_expr.render(self.graph_expr or " ", True, config.FG_COLOR)
        surface.blit(expr_surf, (6, 24))
        hint = self.font_hint.render(
            "ENTER=Plotten  ENTF=Clear  ESC/F7=zurueck  F1=MENU", True, config.DIM_COLOR
        )
        surface.blit(hint, (6, config.DISPLAY_HEIGHT - 14))

    def _draw_graph_view(self, surface):
        plot_height = config.DISPLAY_HEIGHT - 28
        plot_width = config.DISPLAY_WIDTH

        def to_px(x, y):
            sx = (x - self.x_min) / (self.x_max - self.x_min) * plot_width
            sy = (1 - (y - self.y_min) / (self.y_max - self.y_min)) * plot_height
            return sx, sy

        if self.y_min < 0 < self.y_max:
            _, y0 = to_px(0, 0)
            pygame.draw.line(surface, config.DIM_COLOR, (0, y0), (plot_width, y0))
        if self.x_min < 0 < self.x_max:
            x0, _ = to_px(0, 0)
            pygame.draw.line(surface, config.DIM_COLOR, (x0, 0), (x0, plot_height))

        variables = {"ans": self.ans, "mem": self.memory}
        last_point = None
        for px in range(plot_width):
            x = self.x_min + (px / plot_width) * (self.x_max - self.x_min)
            variables["x"] = x
            try:
                y = safe_eval(self.graph_expr, angle_mode=self.angle_mode, variables=variables)
                point = to_px(x, y) if math.isfinite(y) else None
            except (CalculatorError, ValueError, ZeroDivisionError, OverflowError):
                point = None

            if point is not None and last_point is not None:
                # Grosse Spruenge (z.B. an Polstellen wie tan(x)) nicht verbinden
                if abs(point[1] - last_point[1]) < plot_height * 1.5:
                    pygame.draw.line(surface, config.ACCENT_COLOR, last_point, point, 1)
            last_point = point

        label = self.font_hint.render(f"y = {self.graph_expr}", True, config.FG_COLOR)
        surface.blit(label, (4, plot_height + 1))
        hint = self.font_hint.render(
            "Pfeile=Pan +/-=Zoom ESC/F7=Eingabe", True, config.DIM_COLOR
        )
        surface.blit(hint, (4, plot_height + 14))
