"""
Модуль для решения биквадратного уравнения Ax^4 + Bx^2 + C = 0.
"""

import math
from typing import List, Tuple, Optional


def solve_biquadratic(a: float, b: float, c: float) -> Tuple[List[float], float]:
    """
    Решает биквадратное уравнение ax^4 + bx^2 + c = 0.

    Args:
        a: Коэффициент при x^4
        b: Коэффициент при x^2
        c: Свободный член

    Returns:
        Кортеж (список корней, дискриминант)

    Raises:
        ValueError: Если коэффициент a равен 0
    """
    if a == 0:
        raise ValueError("Коэффициент A не может быть равен 0 для биквадратного уравнения.")

    # Вычисляем дискриминант
    discriminant = b * b - 4 * a * c
    roots = []

    if discriminant < 0:
        return roots, discriminant

    if discriminant == 0:
        t = -b / (2 * a)
        _add_roots_from_t(t, roots)
    else:
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        _add_roots_from_t(t1, roots)
        _add_roots_from_t(t2, roots)

    return sorted(list(set(roots))), discriminant


def _add_roots_from_t(t: float, roots: List[float]) -> None:
    """
    Внутренняя функция для добавления корней из t = x^2.

    Args:
        t: Значение t = x^2
        roots: Список для добавления корней
    """
    if t > 0:
        x1 = math.sqrt(t)
        x2 = -math.sqrt(t)
        roots.extend([x1, x2])
    elif t == 0 and 0 not in roots:
        roots.append(0.0)


def validate_input(value: str) -> Optional[float]:
    """
    Валидация входных данных.

    Args:
        value: Строка для валидации

    Returns:
        Число или None, если строка невалидна
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def get_coefficient_from_args(args: List[str], index: int) -> Optional[float]:
    """
    Получение коэффициента из аргументов командной строки.

    Args:
        args: Список аргументов
        index: Индекс коэффициента

    Returns:
        Значение коэффициента или None
    """
    if len(args) > index:
        return validate_input(args[index])
    return None
