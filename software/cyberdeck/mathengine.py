"""Wissenschaftlicher Rechenkern fuer den Rechner-Screen (Kap. 9.1).

Umfang orientiert sich an dem, was Community-Nachbauten von Grafikrechnern
(z. B. TI-84-Plus-Klone) an Kernfunktionen typischerweise abdecken:
Trigonometrie inkl. Grad/Radiant, Logarithmen, Wurzeln/Potenzen, Fakultaet/
Kombinatorik, Speicher, ANS - plus Funktionsplots (siehe screens/calculator.py,
Graph-Modus). Bewusst NICHT enthalten: Gleichungsloeser, Matrizen, komplexe
Zahlen, symbolisches Ableiten/Integrieren - das waere ein eigenes, deutlich
groesseres Projekt (vergleichbar mit dem CAS in Nachbauten wie OpenCalc).

Es wird nirgends eval()/exec() auf Nutzereingaben aufgerufen - nur ein
eingeschraenkter AST-Interpreter mit fester Funktions-/Namens-Whitelist.
"""

import ast
import math
import re


class CalculatorError(Exception):
    pass


# Fakultaet (nur auf einer nackten Zahl/ans, z.B. "5!" oder "ans!") und
# implizite Multiplikation ("2pi" -> "2*pi", "3(1+2)" -> "3*(1+2)") werden
# vor dem eigentlichen Parsen aufgeloest - Funktionsaufrufe wie "sin(" bleiben
# unangetastet, weil dort vor der Klammer ein Buchstabe steht, kein
# Ziffer/")"-Zeichen.
_FACT_RE = re.compile(r"(\d+(?:\.\d+)?|ans)!")
_IMPLICIT_MUL_RE = re.compile(r"(?<=[0-9)])(?=[a-zA-Z(])")

_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a**b,
}
_ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

_CONSTANTS = {"pi": math.pi, "e": math.e}


def _fact(n):
    n = int(n)
    if n < 0:
        raise CalculatorError("Fakultaet nur fuer n >= 0")
    return math.factorial(n)


def _npr(n, r):
    n, r = int(n), int(r)
    return math.factorial(n) // math.factorial(n - r)


def _ncr(n, r):
    return math.comb(int(n), int(r))


def _cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)


def _build_funcs(angle_mode: str):
    to_rad = math.radians if angle_mode == "deg" else (lambda v: v)
    to_out = math.degrees if angle_mode == "deg" else (lambda v: v)
    return {
        "sin": lambda v: math.sin(to_rad(v)),
        "cos": lambda v: math.cos(to_rad(v)),
        "tan": lambda v: math.tan(to_rad(v)),
        "asin": lambda v: to_out(math.asin(v)),
        "acos": lambda v: to_out(math.acos(v)),
        "atan": lambda v: to_out(math.atan(v)),
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "asinh": math.asinh,
        "acosh": math.acosh,
        "atanh": math.atanh,
        "log": math.log10,
        "ln": math.log,
        "log2": math.log2,
        "sqrt": math.sqrt,
        "cbrt": _cbrt,
        "root": lambda n, x: x ** (1 / n),
        "abs": abs,
        "fact": _fact,
        "npr": _npr,
        "ncr": _ncr,
    }


def preprocess(expr: str) -> str:
    prev = None
    while prev != expr:
        prev = expr
        expr = _FACT_RE.sub(r"fact(\1)", expr)
    return _IMPLICIT_MUL_RE.sub("*", expr)


def safe_eval(expr: str, angle_mode: str = "deg", variables: dict | None = None) -> float:
    """Wertet einen wissenschaftlichen Ausdruck aus. `variables` stellt z.B.
    `ans`/`mem` (Rechner-Modus) oder `x` (Graph-Modus) bereit."""
    variables = variables or {}
    funcs = _build_funcs(angle_mode)
    try:
        tree = ast.parse(preprocess(expr), mode="eval")
    except SyntaxError as exc:
        raise CalculatorError("Syntaxfehler") from exc
    return _eval_node(tree.body, funcs, variables)


def _eval_node(node, funcs, variables):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise CalculatorError("Ungueltiger Wert")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return _ALLOWED_BINOPS[type(node.op)](
            _eval_node(node.left, funcs, variables), _eval_node(node.right, funcs, variables)
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        return _ALLOWED_UNARYOPS[type(node.op)](_eval_node(node.operand, funcs, variables))
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in funcs
        and not node.keywords
    ):
        args = [_eval_node(a, funcs, variables) for a in node.args]
        return funcs[node.func.id](*args)
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise CalculatorError(f"Unbekannter Name: {node.id}")
    raise CalculatorError("Nicht erlaubter Ausdruck")
