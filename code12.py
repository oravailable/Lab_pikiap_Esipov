import sys
import math


class InputValidator:
    """Класс для валидации ввода данных."""

    @staticmethod
    def is_valid_number(value):
        """Проверяет, можно ли преобразовать строку в действительное число."""
        try:
            float(value)
            return True
        except ValueError:
            return False


class CoefficientReader:
    """Класс для чтения коэффициентов из различных источников."""

    def __init__(self, command_line_args):
        self.args = command_line_args

    def get_coefficient(self, coefficient_name, index):
        """Получает коэффициент по указанному индексу."""
        prompt = coefficient_name

        # Пробуем получить из аргументов командной строки
        if len(self.args) > index and InputValidator.is_valid_number(self.args[index]):
            return float(self.args[index])
        elif len(self.args) > index:
            print(f"Некорректное значение коэффициента {prompt} в аргументах. ", end="")

        # Запрашиваем с клавиатуры
        return self._read_from_keyboard(prompt)

    def _read_from_keyboard(self, prompt):
        """Читает коэффициент с клавиатуры с проверкой корректности."""
        while True:
            try:
                value = input(f"Введите коэффициент {prompt}: ")
                return float(value)
            except ValueError:
                print("Некорректное значение. Пожалуйста, введите действительное число.")


class BiquadraticEquation:
    """Класс для представления и решения биквадратного уравнения."""

    def __init__(self, a, b, c):
        if a == 0:
            raise ValueError("Коэффициент A не может быть равен 0 для биквадратного уравнения.")
        self.a = a
        self.b = b
        self.c = c
        self.roots = []
        self.discriminant = None

    def solve(self):
        """Решает биквадратное уравнение ax^4 + bx^2 + c = 0."""
        # Вычисляем дискриминант квадратного уравнения относительно t = x^2
        self.discriminant = self.b * self.b - 4 * self.a * self.c
        self.roots = []

        if self.discriminant < 0:
            return self.roots

        if self.discriminant == 0:
            t = -self.b / (2 * self.a)
            self._add_roots_from_t(t)
        else:
            t1 = (-self.b + math.sqrt(self.discriminant)) / (2 * self.a)
            t2 = (-self.b - math.sqrt(self.discriminant)) / (2 * self.a)
            self._add_roots_from_t(t1)
            self._add_roots_from_t(t2)

        return self.roots

    def _add_roots_from_t(self, t):
        """Добавляет корни из значения t = x^2."""
        if t > 0:
            x1 = math.sqrt(t)
            x2 = -math.sqrt(t)
            self.roots.extend([x1, x2])
        elif t == 0 and 0 not in self.roots:
            self.roots.append(0.0)

    def get_discriminant(self):
        """Возвращает значение дискриминанта."""
        return self.discriminant

    def get_formatted_equation(self):
        """Возвращает строковое представление уравнения."""
        return f"{self.a}x^4 + {self.b}x^2 + {self.c} = 0"


class EquationSolverApp:
    """Основной класс приложения для решения уравнения."""

    def __init__(self):
        self.equation = None
        self.coefficient_reader = None

    def run(self):
        """Запускает приложение."""
        self._print_header()

        # Создаем читатель коэффициентов
        args = sys.argv[1:]
        self.coefficient_reader = CoefficientReader(args)

        # Получаем коэффициенты
        a = self._get_coefficient_with_retry("A", 0)
        b = self.coefficient_reader.get_coefficient("B", 1)
        c = self.coefficient_reader.get_coefficient("C", 2)

        # Создаем и решаем уравнение
        try:
            self.equation = BiquadraticEquation(a, b, c)
            self._solve_and_display()
        except ValueError as e:
            print(f"Ошибка: {e}")
            print("Пожалуйста, запустите программу снова с корректными коэффициентами.")

        input("\nНажмите Enter для выхода...")

    def _print_header(self):
        """Выводит заголовок программы."""
        print("Решение биквадратного уравнения: Ax^4 + Bx^2 + C = 0")
        print("=" * 50)

    def _get_coefficient_with_retry(self, coefficient_name, index):
        """Получает коэффициент A с повторной попыткой при некорректном вводе."""
        while True:
            try:
                value = self.coefficient_reader.get_coefficient(coefficient_name, index)
                if value == 0 and coefficient_name == "A":
                    print("Коэффициент A не может быть равен 0. Пожалуйста, введите другое значение.")
                    continue
                return value
            except ValueError:
                print("Некорректное значение. Пожалуйста, попробуйте еще раз.")

    def _solve_and_display(self):
        """Решает уравнение и отображает результаты."""
        print(f"\nУравнение: {self.equation.get_formatted_equation()}")
        print("=" * 50)

        roots = self.equation.solve()
        discriminant = self.equation.get_discriminant()

        print(f"Дискриминант D = {discriminant:.3f}")

        if discriminant is not None:
            if discriminant < 0:
                print("Действительных корней нет.")
            else:
                if roots:
                    print(f"Найдено {len(roots)} действительных корня(ей):")
                    for i, root in enumerate(sorted(set(roots)), 1):
                        print(f"Корень {i}: x = {root:.6f}")
                else:
                    print("Действительных корней нет.")

        print("=" * 50)


def main():
    """Точка входа в программу."""
    app = EquationSolverApp()
    app.run()


if __name__ == "__main__":
    main()
