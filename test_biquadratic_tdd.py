"""
Модульные тесты с использованием TDD-подхода (unittest).
"""

import unittest
import math
from biquadratic_solver import solve_biquadratic, validate_input, get_coefficient_from_args


class TestBiquadraticSolverTDD(unittest.TestCase):
    """Тесты для решения биквадратного уравнения."""

    def test_solve_biquadratic_four_real_roots(self):
        """Тест: уравнение имеет 4 действительных корня."""
        # x^4 - 5x^2 + 4 = 0 -> корни: ±1, ±2
        roots, discriminant = solve_biquadratic(1, -5, 4)

        self.assertAlmostEqual(discriminant, 9.0)
        self.assertEqual(len(roots), 4)
        self.assertAlmostEqual(roots[0], -2.0)
        self.assertAlmostEqual(roots[1], -1.0)
        self.assertAlmostEqual(roots[2], 1.0)
        self.assertAlmostEqual(roots[3], 2.0)

    def test_solve_biquadratic_no_real_roots(self):
        """Тест: уравнение не имеет действительных корней."""
        # x^4 + x^2 + 1 = 0 -> нет действительных корней
        roots, discriminant = solve_biquadratic(1, 1, 1)

        self.assertLess(discriminant, 0)
        self.assertEqual(len(roots), 0)

    def test_solve_biquadratic_single_root(self):
        """Тест: уравнение имеет один корень."""
        # x^4 = 0 -> корень: 0
        roots, discriminant = solve_biquadratic(1, 0, 0)

        self.assertAlmostEqual(discriminant, 0.0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 0.0)

    def test_solve_biquadratic_two_real_roots(self):
        """Тест: уравнение имеет 2 действительных корня."""
        # x^4 - 9 = 0 -> корни: ±√3
        roots, discriminant = solve_biquadratic(1, 0, -9)

        self.assertAlmostEqual(discriminant, 36.0)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], -math.sqrt(3))
        self.assertAlmostEqual(roots[1], math.sqrt(3))

    def test_solve_biquadratic_a_zero_raises_error(self):
        """Тест: коэффициент A не может быть 0."""
        with self.assertRaises(ValueError) as context:
            solve_biquadratic(0, 2, 3)

        self.assertEqual(str(context.exception),
                        "Коэффициент A не может быть равен 0 для биквадратного уравнения.")


class TestInputValidationTDD(unittest.TestCase):
    """Тесты для валидации ввода."""

    def test_validate_input_valid_numbers(self):
        """Тест: валидация корректных чисел."""
        test_cases = [
            ("123", 123.0),
            ("-45.67", -45.67),
            ("0", 0.0),
            ("3.14", 3.14),
            ("1e-5", 1e-5),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                result = validate_input(input_str)
                self.assertIsNotNone(result)
                self.assertAlmostEqual(result, expected)

    def test_validate_input_invalid_values(self):
        """Тест: валидация некорректных значений."""
        invalid_inputs = ["abc", "12a34", "", " ", "1.2.3", None]

        for input_str in invalid_inputs:
            with self.subTest(input=input_str):
                result = validate_input(input_str)
                self.assertIsNone(result)

    def test_get_coefficient_from_args(self):
        """Тест: получение коэффициентов из аргументов."""
        args = ["1", "-5", "4", "extra"]

        # Тест корректных индексов
        self.assertAlmostEqual(get_coefficient_from_args(args, 0), 1.0)
        self.assertAlmostEqual(get_coefficient_from_args(args, 1), -5.0)
        self.assertAlmostEqual(get_coefficient_from_args(args, 2), 4.0)

        # Тест индекса за пределами массива
        self.assertIsNone(get_coefficient_from_args(args, 5))

        # Тест некорректного значения
        args_invalid = ["abc", "123"]
        self.assertIsNone(get_coefficient_from_args(args_invalid, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
