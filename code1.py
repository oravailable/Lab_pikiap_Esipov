import sys
import math


def is_valid_number(value):
    """Проверяет, можно ли преобразовать строку в действительное число."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_coefficient(prompt, args, index):
    """Получает коэффициент из аргументов командной строки или с клавиатуры."""
    if len(args) > index:
        if is_valid_number(args[index]):
            return float(args[index])
        print(f"Некорректное значение коэффициента {prompt}. ", end="")

    while True:
        try:
            value = input(f"Введите коэффициент {prompt}: ")
            return float(value)
        except ValueError:
            print("Некорректное значение. Пожалуйста, введите действительное число.")


def solve_biquadratic(a, b, c):
    """Решает биквадратное уравнение ax^4 + bx^2 + c = 0."""
    if a == 0:
        print("Коэффициент A не может быть равен 0 для биквадратного уравнения.")
        return []

    # Решаем как квадратное уравнение относительно t = x^2
    discriminant = b * b - 4 * a * c
    roots = []

    if discriminant < 0:
        print(f"Дискриминант D = {discriminant:.3f} < 0")
        print("Действительных корней нет.")
        return roots

    print(f"Дискриминант D = {discriminant:.3f}")

    if discriminant == 0:
        t = -b / (2 * a)
        print(f"t = x^2 = {t:.3f}")
        if t > 0:
            x1 = math.sqrt(t)
            x2 = -math.sqrt(t)
            roots.extend([x1, x2])
            print(f"Корни: x1 = {x1:.3f}, x2 = {x2:.3f}")
        elif t == 0:
            roots.append(0.0)
            print(f"Корень: x = 0")
        else:
            print("Действительных корней нет.")
    else:
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        print(f"t1 = x^2 = {t1:.3f}, t2 = x^2 = {t2:.3f}")

        if t1 > 0:
            x1 = math.sqrt(t1)
            x2 = -math.sqrt(t1)
            roots.extend([x1, x2])
            print(f"Корни из t1: x1 = {x1:.3f}, x2 = {x2:.3f}")
        elif t1 == 0:
            roots.append(0.0)
            print(f"Корень из t1: x = 0")

        if t2 > 0:
            x3 = math.sqrt(t2)
            x4 = -math.sqrt(t2)
            roots.extend([x3, x4])
            print(f"Корни из t2: x3 = {x3:.3f}, x4 = {x4:.3f}")
        elif t2 == 0 and t1 != 0:  # t1 = 0 уже обработано выше
            roots.append(0.0)
            print(f"Корень из t2: x = 0")

    if not roots:
        print("Действительных корней нет.")

    return roots


def main():
    """Основная функция программы."""
    print("Решение биквадратного уравнения: Ax^4 + Bx^2 + C = 0")
    print("=" * 50)

    # Получаем коэффициенты из аргументов командной строки или с клавиатуры
    args = sys.argv[1:]  # Исключаем имя программы

    a = get_coefficient("A", args, 0)
    b = get_coefficient("B", args, 1)
    c = get_coefficient("C", args, 2)

    print(f"\nКоэффициенты: A = {a}, B = {b}, C = {c}")
    print("=" * 50)

    # Решаем уравнение
    roots = solve_biquadratic(a, b, c)

    print("=" * 50)
    if roots:
        print(f"Найдено {len(roots)} действительных корня(ей).")
        for i, root in enumerate(sorted(set(roots)), 1):
            print(f"Корень {i}: x = {root:.6f}")

    input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()
