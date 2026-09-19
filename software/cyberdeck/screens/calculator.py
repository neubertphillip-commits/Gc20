import ast
import math
import operator

import pygame

from . import base
from .. import config

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_ALLOWED_FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
}
_ALLOWED_CONSTS = {"pi": math.pi, "e": math.e}


class CalculatorError(Exception):
    pass


def safe_eval(expr: str) -> float:
    """Wertet einen eingeschraenkten arithmetischen Ausdruck aus - bewusst
    kein eval()/exec() auf Nutzereingaben, sondern nur Literale, +-*/%**,
    Klammern, unaeres +/- und eine feste Funktions-/Konstanten-Whitelist."""
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError("Syntaxfehler") from exc
    return _eval_node(tree.body)


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise CalculatorError("Ungueltiger Wert")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_eval_node(node.operand))
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in _ALLOWED_FUNCS
        and not node.keywords
    ):
        args = [_eval_node(a) for a in node.args]
        return _ALLOWED_FUNCS[node.func.id](*args)
    if isinstance(node, ast.Name) and node.id in _ALLOWED_CONSTS:
        return _ALLOWED_CONSTS[node.id]
    raise CalculatorError("Nicht erlaubter Ausdruck")


class CalculatorScreen(base.Screen):
    """Reproduziert die originale Kernfunktion des Geraets (Kap. 9.1)."""

    def __init__(self, app):
        super().__init__(app)
        self.expr = ""
        self.result = None
        self.error = None
        self.font_expr = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_NORMAL)
        self.font_result = pygame.font.SysFont(
            config.FONT_NAME, config.FONT_SIZE_LARGE, bold=True
        )
        self.font_hint = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SMALL)

    def handle_key(self, event):
        if event.key == pygame.K_RETURN:
            self._evaluate()
        elif event.key == pygame.K_BACKSPACE:
            self.expr = self.expr[:-1]
            self.error = None
        elif event.key == pygame.K_DELETE:
            self.expr = ""
            self.result = None
            self.error = None
        elif event.unicode and event.unicode in "0123456789.+-*/%()^":
            self.expr += "**" if event.unicode == "^" else event.unicode
            self.error = None

    def _evaluate(self):
        if not self.expr.strip():
            return
        try:
            self.result = safe_eval(self.expr)
            self.error = None
        except ZeroDivisionError:
            self.result, self.error = None, "Division durch 0"
        except CalculatorError as exc:
            self.result, self.error = None, str(exc)

    def draw(self, surface):
        pygame.draw.rect(surface, config.DIM_COLOR, (0, 0, config.DISPLAY_WIDTH, 20), width=1)
        expr_surf = self.font_expr.render(self.expr or " ", True, config.FG_COLOR)
        surface.blit(expr_surf, (6, 4))

        if self.error:
            res_surf = self.font_result.render(self.error, True, config.ERROR_COLOR)
        elif self.result is not None:
            res_surf = self.font_result.render(f"= {self.result:g}", True, config.ACCENT_COLOR)
        else:
            res_surf = self.font_result.render("", True, config.ACCENT_COLOR)
        surface.blit(res_surf, (6, 28))

        hint = self.font_hint.render(
            "Zahlen/Operatoren tippen, ENTER=EXE, ENTF=Clear, F1=MENU",
            True,
            config.DIM_COLOR,
        )
        surface.blit(hint, (6, config.DISPLAY_HEIGHT - 14))
