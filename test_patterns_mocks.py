"""
Тесты с использованием Mock-объектов для шаблонов проектирования.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, create_autospec
import json
import math
from equation_system import (
    Equation,
    EquationFactory,
    BiquadraticEquation,
    JSONEquationAdapter,
    EquationInputProcessor,
    SolvingStrategy,
    DirectSolvingStrategy,
    EquationSolver,
    EquationSystemFacade
)


class TestFactoryMethodWithMocks:
    """Тесты Фабричного метода с Mock-объектами."""

    def test_factory_creates_mock_equation(self):
        """Тест фабрики с моком уравнения."""
        # Создаем мок уравнения
        mock_equation = Mock(spec=Equation)
        mock_equation.get_type.return_value = "mock_equation"
        mock_equation.solve.return_value = [1.0, 2.0]

        # Мокаем фабрику
        with patch('equation_system.EquationFactory.create_equation') as mock_factory:
            mock_factory.return_value = mock_equation

            # Создаем уравнение через фабрику
            factory = EquationFactory()
            equation = factory.create_equation("biquadratic", a=1, b=2, c=3)

            # Проверяем, что фабрика была вызвана
            mock_factory.assert_called_once_with("biquadratic", a=1, b=2, c=3)

            # Проверяем мок
            assert equation.get_type() == "mock_equation"
            assert equation.solve() == [1.0, 2.0]

    def test_equation_solve_with_mock(self):
        """Тест решения уравнения с моком."""
        # Создаем автозаполненный мок для BiquadraticEquation
        mock_equation = create_autospec(BiquadraticEquation)
        mock_equation.solve.return_value = [-2.0, -1.0, 1.0, 2.0]
        mock_equation.get_type.return_value = "biquadratic"
        mock_equation.validate.return_value = True

        # Проверяем работу мока
        roots = mock_equation.solve()
        assert roots == [-2.0, -1.0, 1.0, 2.0]
        assert mock_equation.get_type() == "biquadratic"

        # Проверяем, что методы были вызваны
        mock_equation.solve.assert_called_once()
        mock_equation.get_type.assert_called_once()

    @patch('equation_system.BiquadraticEquation')
    def test_factory_creates_biquadratic_with_mock_class(self, MockBiquadratic):
        """Тест фабрики с моком класса BiquadraticEquation."""
        # Настраиваем мок
        mock_instance = MockBiquadratic.return_value
        mock_instance.solve.return_value = [1.0, 2.0]
        mock_instance.get_type.return_value = "biquadratic"

        # Создаем уравнение через фабрику
        factory = EquationFactory()
        equation = factory.create_equation("biquadratic", a=1, b=2, c=3)

        # Проверяем, что класс был вызван с правильными параметрами
        MockBiquadratic.assert_called_once_with(1, 2, 3)

        # Проверяем мок
        assert equation.solve() == [1.0, 2.0]
        assert equation.get_type() == "biquadratic"


class TestAdapterPatternWithMocks:
    """Тесты паттерна Адаптер с Mock-объектами."""

    def test_json_adapter_with_mock_json(self):
        """Тест JSON адаптера с моком json.loads."""
        with patch('equation_system.json.loads') as mock_json_loads:
            # Настраиваем мок
            mock_json_loads.return_value = {
                'type': 'biquadratic',
                'coefficients': {'a': 1, 'b': -5, 'c': 4}
            }

            # Создаем адаптер
            adapter = JSONEquationAdapter()
            data = adapter.parse('{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}')

            # Проверяем вызов json.loads
            mock_json_loads.assert_called_once_with(
                '{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}'
            )

            # Проверяем результат
            assert data.equation_type == 'biquadratic'
            assert data.coefficients == {'a': 1, 'b': -5, 'c': 4}

    def test_input_processor_with_mock_adapter(self):
        """Тест процессора ввода с моком адаптера."""
        # Создаем мок адаптера
        mock_adapter = Mock(spec=JSONEquationAdapter)
        mock_adapter.parse.return_value = Mock(
            equation_type='biquadratic',
            coefficients={'a': 1, 'b': -5, 'c': 4}
        )

        # Создаем мок фабрики
        mock_equation = Mock(spec=BiquadraticEquation)
        mock_equation.solve.return_value = [-2.0, -1.0, 1.0, 2.0]

        with patch('equation_system.EquationFactory.create_equation') as mock_factory:
            mock_factory.return_value = mock_equation

            # Создаем процессор с моком адаптера
            processor = EquationInputProcessor()
            processor._adapters['json'] = mock_adapter

            # Обрабатываем ввод
            equation, equation_data = processor.process_input('json', 'test data')

            # Проверяем вызовы
            mock_adapter.parse.assert_called_once_with('test data')
            mock_factory.assert_called_once_with(
                'biquadratic', a=1, b=-5, c=4
            )

    @patch('equation_system.JSONEquationAdapter')
    @patch('equation_system.EquationFactory')
    def test_input_processor_integration_mock(self, MockFactory, MockAdapter):
        """Интеграционный тест процессора ввода с моками."""
        # Настраиваем моки
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.parse.return_value = Mock(
            equation_type='quadratic',
            coefficients={'a': 1, 'b': -3, 'c': 2}
        )

        mock_equation_instance = Mock()
        mock_equation_instance.solve.return_value = [1.0, 2.0]

        mock_factory_instance = MockFactory.return_value
        mock_factory_instance.create_equation.return_value = mock_equation_instance

        # Создаем и используем процессор
        processor = EquationInputProcessor()
        equation, equation_data = processor.process_input('json', 'test data')

        # Проверяем вызовы
        mock_adapter_instance.parse.assert_called_once_with('test data')
        mock_factory_instance.create_equation.assert_called_once_with(
            'quadratic', a=1, b=-3, c=2
        )


class TestStrategyPatternWithMocks:
    """Тесты паттерна Стратегия с Mock-объектами."""

    def test_direct_strategy_with_mock_equation(self):
        """Тест прямой стратегии с моком уравнения."""
        # Создаем мок уравнения
        mock_equation = Mock(spec=Equation)
        mock_equation.solve.return_value = [1.0, 2.0, 3.0]

        # Создаем стратегию
        strategy = DirectSolvingStrategy()
        roots = strategy.solve(mock_equation)

        # Проверяем, что solve был вызван у уравнения
        mock_equation.solve.assert_called_once()

        # Проверяем результат
        assert roots == [1.0, 2.0, 3.0]
        assert strategy.get_name() == "direct"

    def test_equation_solver_with_mock_strategy(self):
        """Тест решателя уравнений с моком стратегии."""
        # Создаем мок стратегии
        mock_strategy = Mock(spec=SolvingStrategy)
        mock_strategy.solve.return_value = [-2.0, -1.0, 1.0, 2.0]
        mock_strategy.get_name.return_value = "mock_strategy"

        # Создаем мок уравнения
        mock_equation = Mock(spec=Equation)

        # Создаем решатель с моком стратегии
        solver = EquationSolver(mock_strategy)
        roots, strategy_name = solver.solve(mock_equation)

        # Проверяем вызовы
        mock_strategy.solve.assert_called_once_with(mock_equation)
        mock_strategy.get_name.assert_called_once()

        # Проверяем результаты
        assert roots == [-2.0, -1.0, 1.0, 2.0]
        assert strategy_name == "mock_strategy"

    @patch('equation_system.math.sqrt')
    def test_iterative_strategy_with_mock_math(self, mock_sqrt):
        """Тест итеративной стратегии с моком math.sqrt."""
        # Настраиваем мок
        mock_sqrt.side_effect = [3.0, 2.0, 1.0]  # Для sqrt(9), sqrt(4), sqrt(1)

        # Создаем уравнение
        from equation_system import BiquadraticEquation
        equation = BiquadraticEquation(1, -5, 4)

        # Создаем стратегию
        strategy = IterativeSolvingStrategy(tolerance=1e-6, max_iterations=10)

        # Пытаемся решить (может не найти все корни из-за ограничения итераций)
        roots = strategy.solve(equation)

        # Проверяем, что sqrt вызывался
        assert mock_sqrt.call_count >= 1


class TestFacadePatternWithMocks:
    """Тесты паттерна Фасад с Mock-объектами."""

    @patch('equation_system.EquationInputProcessor')
    @patch('equation_system.EquationSolver')
    def test_facade_solve_from_json_with_mocks(self, MockSolver, MockProcessor):
        """Тест фасада с моками процессора и решателя."""
        # Настраиваем моки
        mock_processor_instance = MockProcessor.return_value
        mock_solver_instance = MockSolver.return_value

        # Настраиваем возвращаемые значения
        mock_equation = Mock()
        mock_equation.__str__ = Mock(return_value="x^4 - 5x^2 + 4 = 0")
        mock_equation.get_type = Mock(return_value="biquadratic")

        mock_equation_data = Mock()
        mock_equation_data.coefficients = {'a': 1, 'b': -5, 'c': 4}

        mock_processor_instance.process_input.return_value = (
            mock_equation, mock_equation_data
        )

        mock_solver_instance.solve.return_value = (
            [-2.0, -1.0, 1.0, 2.0], "direct"
        )

        # Создаем и используем фасад
        facade = EquationSystemFacade()
        result = facade.solve_from_json('{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}')

        # Проверяем вызовы
        mock_processor_instance.process_input.assert_called_once_with(
            'json', '{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}'
        )
        mock_solver_instance.solve.assert_called_once_with(mock_equation)

        # Проверяем результат
        assert result['equation'] == "x^4 - 5x^2 + 4 = 0"
        assert result['equation_type'] == "biquadratic"
        assert result['coefficients'] == {'a': 1, 'b': -5, 'c': 4}
        assert result['roots'] == [-2.0, -1.0, 1.0, 2.0]
        assert result['strategy'] == "direct"
        assert result['root_count'] == 4

    def test_facade_with_mock_factory(self):
        """Тест фасада с моком фабрики."""
        with patch('equation_system.EquationFactory.create_equation') as mock_factory:
            # Настраиваем мок
            mock_equation = Mock()
            mock_equation.solve = Mock(return_value=[2.0])
            mock_equation.__str__ = Mock(return_value="2x - 4 = 0")
            mock_equation.get_type = Mock(return_value="linear")

            mock_factory.return_value = mock_equation

            # Создаем фасад
            facade = EquationSystemFacade()

            # Мокаем решатель в фасаде
            mock_solver = Mock()
            mock_solver.solve = Mock(return_value=([2.0], "direct"))
            mock_solver.solve_with_strategy = Mock(return_value=([2.0], "iterative"))
            facade.solver = mock_solver

            # Тестируем solve_directly
            result = facade.solve_directly("linear", a=2, b=-4)

            # Проверяем вызовы
            mock_factory.assert_called_once_with("linear", a=2, b=-4)
            mock_solver.solve.assert_called_once_with(mock_equation)

            # Проверяем результат
            assert result['equation_type'] == "linear"
            assert result['roots'] == [2.0]


class TestIntegrationWithMocks:
    """Интеграционные тесты с моками."""

    def test_complete_workflow_with_mocks(self):
        """Тест полного рабочего процесса с моками."""
        # Создаем моки всех компонентов
        mock_json_adapter = Mock()
        mock_json_adapter.parse.return_value = Mock(
            equation_type='biquadratic',
            coefficients={'a': 1, 'b': -5, 'c': 4}
        )

        mock_equation = Mock()
        mock_equation.solve.return_value = [-2.0, -1.0, 1.0, 2.0]
        mock_equation.__str__ = Mock(return_value="x^4 - 5x^2 + 4 = 0")
        mock_equation.get_type = Mock(return_value="biquadratic")

        mock_factory = Mock()
        mock_factory.create_equation.return_value = mock_equation

        mock_strategy = Mock()
        mock_strategy.solve.return_value = [-2.0, -1.0, 1.0, 2.0]
        mock_strategy.get_name.return_value = "mock_strategy"

        # Используем патчи для замены реальных компонентов
        with patch('equation_system.EquationInputProcessor._adapters',
                  {'json': mock_json_adapter}):
            with patch('equation_system.EquationFactory', return_value=mock_factory):
                with patch('equation_system.EquationSolver') as MockSolver:
                    mock_solver_instance = MockSolver.return_value
                    mock_solver_instance.solve.return_value = (
                        [-2.0, -1.0, 1.0, 2.0], "mock_strategy"
                    )

                    # Создаем и используем фасад
                    facade = EquationSystemFacade()
                    result = facade.solve_from_json(
                        '{"type": "biquadratic", "coefficients": {"a": 1, "b": -5, "c": 4}}'
                    )

                    # Проверяем результат
                    assert result['equation_type'] == 'biquadratic'
                    assert result['roots'] == [-2.0, -1.0, 1.0, 2.0]
                    assert result['strategy'] == 'mock_strategy'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
