"""
TDD-тесты для шаблонов проектирования.
"""

import unittest
import json
from equation_system import (
    EquationFactory,
    BiquadraticEquation,
    QuadraticEquation,
    LinearEquation,
    JSONEquationAdapter,
    XMLEquationAdapter,
    DirectSolvingStrategy,
    IterativeSolvingStrategy,
    AnalyticalSolvingStrategy,
    EquationSolver,
    EquationSystemFacade
)


class TestFactoryMethodTDD(unittest.TestCase):
    """TDD-тесты для Фабричного метода."""

    def test_create_biquadratic_equation(self):
        """Тест создания биквадратного уравнения."""
        factory = EquationFactory()
        equation = factory.create_equation("biquadratic", a=1, b=-5, c=4)

        self.assertIsInstance(equation, BiquadraticEquation)
        self.assertEqual(equation.a, 1)
        self.assertEqual(equation.b, -5)
        self.assertEqual(equation.c, 4)
        self.assertEqual(equation.get_type(), "biquadratic")

    def test_create_quadratic_equation(self):
        """Тест создания квадратного уравнения."""
        factory = EquationFactory()
        equation = factory.create_equation("quadratic", a=1, b=-3, c=2)

        self.assertIsInstance(equation, QuadraticEquation)
        self.assertEqual(equation.a, 1)
        self.assertEqual(equation.b, -3)
        self.assertEqual(equation.c, 2)
        self.assertEqual(equation.get_type(), "quadratic")

    def test_create_linear_equation(self):
        """Тест создания линейного уравнения."""
        factory = EquationFactory()
        equation = factory.create_equation("linear", a=2, b=-4)

        self.assertIsInstance(equation, LinearEquation)
        self.assertEqual(equation.a, 2)
        self.assertEqual(equation.b, -4)
        self.assertEqual(equation.get_type(), "linear")

    def test_create_equation_invalid_type(self):
        """Тест создания уравнения с неверным типом."""
        factory = EquationFactory()

        with self.assertRaises(ValueError) as context:
            factory.create_equation("invalid_type", a=1, b=2, c=3)

        self.assertIn("Неизвестный тип уравнения", str(context.exception))

    def test_biquadratic_solve_four_roots(self):
        """Тест решения биквадратного уравнения с 4 корнями."""
        equation = BiquadraticEquation(1, -5, 4)  # x^4 - 5x^2 + 4 = 0
        roots = equation.solve()

        self.assertEqual(len(roots), 4)
        self.assertAlmostEqual(roots[0], -2.0)
        self.assertAlmostEqual(roots[1], -1.0)
        self.assertAlmostEqual(roots[2], 1.0)
        self.assertAlmostEqual(roots[3], 2.0)

    def test_biquadratic_solve_no_roots(self):
        """Тест решения биквадратного уравнения без корней."""
        equation = BiquadraticEquation(1, 1, 1)  # x^4 + x^2 + 1 = 0
        roots = equation.solve()

        self.assertEqual(len(roots), 0)

    def test_quadratic_solve_two_roots(self):
        """Тест решения квадратного уравнения с 2 корнями."""
        equation = QuadraticEquation(1, -3, 2)  # x^2 - 3x + 2 = 0
        roots = equation.solve()

        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], 1.0)
        self.assertAlmostEqual(roots[1], 2.0)

    def test_linear_solve_one_root(self):
        """Тест решения линейного уравнения."""
        equation = LinearEquation(2, -4)  # 2x - 4 = 0
        roots = equation.solve()

        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 2.0)


class TestAdapterPatternTDD(unittest.TestCase):
    """TDD-тесты для паттерна Адаптер."""

    def test_json_adapter_valid_data(self):
        """Тест JSON адаптера с корректными данными."""
        adapter = JSONEquationAdapter()
        json_data = '{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}'

        equation_data = adapter.parse(json_data)

        self.assertEqual(equation_data.equation_type, "biquadratic")
        self.assertEqual(equation_data.coefficients["a"], 1)
        self.assertEqual(equation_data.coefficients["b"], -5)
        self.assertEqual(equation_data.coefficients["c"], 4)

    def test_json_adapter_invalid_json(self):
        """Тест JSON адаптера с некорректным JSON."""
        adapter = JSONEquationAdapter()
        invalid_json = '{"type": "biquadratic", "coefficients": {'

        with self.assertRaises(ValueError) as context:
            adapter.parse(invalid_json)

        self.assertIn("Ошибка парсинга JSON", str(context.exception))

    def test_json_adapter_missing_fields(self):
        """Тест JSON адаптера с отсутствующими полями."""
        adapter = JSONEquationAdapter()
        json_data = '{"type": "biquadratic"}'

        equation_data = adapter.parse(json_data)

        self.assertEqual(equation_data.equation_type, "biquadratic")
        self.assertEqual(equation_data.coefficients, {})

    def test_xml_adapter_valid_data(self):
        """Тест XML адаптера с корректными данными."""
        adapter = XMLEquationAdapter()
        xml_data = '''
        <equation>
            <type>biquadratic</type>
            <coefficients>
                <a>1</a>
                <b>-5</b>
                <c>4</c>
            </coefficients>
        </equation>
        '''

        equation_data = adapter.parse(xml_data)

        self.assertEqual(equation_data.equation_type, "biquadratic")
        self.assertEqual(equation_data.coefficients["a"], 1.0)
        self.assertEqual(equation_data.coefficients["b"], -5.0)
        self.assertEqual(equation_data.coefficients["c"], 4.0)

    def test_xml_adapter_invalid_xml(self):
        """Тест XML адаптера с некорректным XML."""
        adapter = XMLEquationAdapter()
        invalid_xml = '<equation><type>biquadratic</type>'

        with self.assertRaises(ValueError) as context:
            adapter.parse(invalid_xml)

        self.assertIn("Ошибка парсинга XML", str(context.exception))


class TestStrategyPatternTDD(unittest.TestCase):
    """TDD-тесты для паттерна Стратегия."""

    def test_direct_strategy_biquadratic(self):
        """Тест прямой стратегии для биквадратного уравнения."""
        strategy = DirectSolvingStrategy()
        equation = BiquadraticEquation(1, -5, 4)

        roots = strategy.solve(equation)

        self.assertEqual(len(roots), 4)
        self.assertEqual(strategy.get_name(), "direct")

    def test_iterative_strategy_biquadratic(self):
        """Тест итеративной стратегии для биквадратного уравнения."""
        strategy = IterativeSolvingStrategy(tolerance=1e-6)
        equation = BiquadraticEquation(1, -5, 4)

        roots = strategy.solve(equation)

        # Итеративный метод может найти не все корни
        self.assertGreaterEqual(len(roots), 2)
        self.assertIn("iterative", strategy.get_name())

    def test_analytical_strategy_biquadratic(self):
        """Тест аналитической стратегии для биквадратного уравнения."""
        strategy = AnalyticalSolvingStrategy()
        equation = BiquadraticEquation(1, -5, 4)

        roots = strategy.solve(equation)

        self.assertEqual(len(roots), 4)
        self.assertEqual(strategy.get_name(), "analytical")

    def test_equation_solver_with_different_strategies(self):
        """Тест решателя уравнений с разными стратегиями."""
        solver = EquationSolver()
        equation = BiquadraticEquation(1, -5, 4)

        # Тест с прямой стратегией
        roots1, name1 = solver.solve(equation)
        self.assertEqual(name1, "direct")

        # Смена стратегии на итеративную
        solver.set_strategy(IterativeSolvingStrategy())
        roots2, name2 = solver.solve(equation)
        self.assertIn("iterative", name2)

        # Смена стратегии на аналитическую
        solver.set_strategy(AnalyticalSolvingStrategy())
        roots3, name3 = solver.solve(equation)
        self.assertEqual(name3, "analytical")

    def test_solve_with_strategy_method(self):
        """Тест метода solve_with_strategy."""
        solver = EquationSolver()
        equation = BiquadraticEquation(1, -5, 4)

        strategy = IterativeSolvingStrategy()
        roots, strategy_name = solver.solve_with_strategy(equation, strategy)

        self.assertIn("iterative", strategy_name)
        self.assertGreaterEqual(len(roots), 2)


class TestFacadePatternTDD(unittest.TestCase):
    """TDD-тесты для паттерна Фасад."""

    def test_facade_solve_directly(self):
        """Тест фасада для прямого решения."""
        facade = EquationSystemFacade()

        result = facade.solve_directly("biquadratic", a=1, b=-5, c=4)

        self.assertEqual(result["equation_type"], "biquadratic")
        self.assertEqual(result["coefficients"]["a"], 1)
        self.assertEqual(result["coefficients"]["b"], -5)
        self.assertEqual(result["coefficients"]["c"], 4)
        self.assertEqual(result["strategy"], "direct")
        self.assertEqual(result["root_count"], 4)
        self.assertIn("x^4 - 5x^2 + 4 = 0", result["equation"])

    def test_facade_solve_with_strategy(self):
        """Тест фасада с указанием стратегии."""
        facade = EquationSystemFacade()
        strategy = IterativeSolvingStrategy()

        result = facade.solve_with_strategy(
            "biquadratic", strategy, a=1, b=-5, c=4
        )

        self.assertEqual(result["equation_type"], "biquadratic")
        self.assertIn("iterative", result["strategy"])

    def test_facade_solve_from_json(self):
        """Тест фасада для решения из JSON."""
        facade = EquationSystemFacade()
        json_data = '{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}'

        result = facade.solve_from_json(json_data)

        self.assertEqual(result["equation_type"], "biquadratic")
        self.assertEqual(result["root_count"], 4)

    def test_facade_solve_from_xml(self):
        """Тест фасада для решения из XML."""
        facade = EquationSystemFacade()
        xml_data = '''
        <equation>
            <type>biquadratic</type>
            <coefficients>
                <a>1</a>
                <b>-5</b>
                <c>4</c>
            </coefficients>
        </equation>
        '''

        result = facade.solve_from_xml(xml_data)

        self.assertEqual(result["equation_type"], "biquadratic")
        self.assertEqual(result["coefficients"]["a"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
