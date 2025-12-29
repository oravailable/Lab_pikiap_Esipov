"""
BDD-тесты для шаблонов проектирования.
Для работы необходимо: pip install pytest pytest-bdd
"""

import pytest
import json
from pytest_bdd import scenarios, given, when, then, parsers
from equation_system import (
    EquationFactory,
    EquationInputProcessor,
    EquationSolver,
    DirectSolvingStrategy,
    IterativeSolvingStrategy,
    AnalyticalSolvingStrategy
)

# Загружаем сценарии из feature-файлов
scenarios('../features/equation_system.feature')


# Контекст для хранения состояния между шагами
@pytest.fixture
def context():
    return {}


# ============================================================================
# Шаги для Фабричного метода
# ============================================================================

@given(parsers.parse('я хочу создать уравнение типа "{equation_type}"'))
def step_create_equation_type(context, equation_type):
    context['equation_type'] = equation_type


@given(parsers.parse('с коэффициентами a={a}, b={b}, c={c}'))
def step_with_coefficients_abc(context, a, b, c):
    context['a'] = float(a)
    context['b'] = float(b)
    context['c'] = float(c)


@given(parsers.parse('с коэффициентами a={a}, b={b}'))
def step_with_coefficients_ab(context, a, b):
    context['a'] = float(a)
    context['b'] = float(b)


@when('я создаю уравнение с помощью фабрики')
def step_create_equation_with_factory(context):
    factory = EquationFactory()

    if context['equation_type'] == 'linear':
        context['equation'] = factory.create_equation(
            context['equation_type'],
            a=context['a'],
            b=context['b']
        )
    else:
        context['equation'] = factory.create_equation(
            context['equation_type'],
            a=context['a'],
            b=context['b'],
            c=context['c']
        )


@then(parsers.parse('уравнение должно быть типа "{expected_type}"'))
def step_equation_should_have_type(context, expected_type):
    assert context['equation'].get_type() == expected_type


@then(parsers.parse('уравнение должно иметь {count:d} корня(ей)'))
def step_equation_should_have_roots_count(context, count):
    roots = context['equation'].solve()
    assert len(roots) == count


# ============================================================================
# Шаги для Адаптера
# ============================================================================

@given(parsers.parse('у меня есть JSON данные для уравнения типа "{equation_type}"'))
def step_have_json_data_for_equation(context, equation_type):
    context['equation_type'] = equation_type


@given(parsers.parse('с коэффициентами в JSON: {json_coeffs}'))
def step_with_json_coefficients(context, json_coeffs):
    coeffs_dict = json.loads(json_coeffs)
    context['json_data'] = json.dumps({
        'type': context['equation_type'],
        'coefficients': coeffs_dict
    })


@when('я обрабатываю JSON данные через адаптер')
def step_process_json_through_adapter(context):
    processor = EquationInputProcessor()
    context['equation'], context['equation_data'] = processor.process_input(
        'json', context['json_data']
    )


@then(parsers.parse('коэффициент "{coeff}" должен быть равен {value}'))
def step_coefficient_should_equal(context, coeff, value):
    assert context['equation_data'].coefficients[coeff] == float(value)


# ============================================================================
# Шаги для Стратегии
# ============================================================================

@given(parsers.parse('я выбрал стратегию решения "{strategy_name}"'))
def step_select_solving_strategy(context, strategy_name):
    if strategy_name == 'direct':
        context['strategy'] = DirectSolvingStrategy()
    elif strategy_name == 'iterative':
        context['strategy'] = IterativeSolvingStrategy()
    elif strategy_name == 'analytical':
        context['strategy'] = AnalyticalSolvingStrategy()
    else:
        raise ValueError(f"Неизвестная стратегия: {strategy_name}")


@given('у меня есть биквадратное уравнение x^4 - 5x^2 + 4 = 0')
def step_have_biquadratic_equation(context):
    factory = EquationFactory()
    context['equation'] = factory.create_equation(
        'biquadratic', a=1, b=-5, c=4
    )


@when('я решаю уравнение с выбранной стратегией')
def step_solve_with_selected_strategy(context):
    solver = EquationSolver(context['strategy'])
    context['roots'], context['strategy_name'] = solver.solve(context['equation'])


@then(parsers.parse('должно быть найдено {count:d} корня(ей)'))
def step_should_find_roots_count(context, count):
    assert len(context['roots']) == count


@then(parsers.parse('использованная стратегия должна быть "{expected_strategy}"'))
def step_strategy_should_be(context, expected_strategy):
    assert context['strategy_name'] == expected_strategy


# ============================================================================
# Комплексные сценарии
# ============================================================================

@given('у меня есть система уравнений')
def step_have_equation_system(context):
    factory = EquationFactory()
    context['equations'] = [
        factory.create_equation('biquadratic', a=1, b=-5, c=4),
        factory.create_equation('quadratic', a=1, b=-3, c=2),
        factory.create_equation('linear', a=2, b=-4)
    ]


@when('я решаю все уравнения с прямой стратегией')
def step_solve_all_with_direct_strategy(context):
    solver = EquationSolver(DirectSolvingStrategy())
    context['results'] = []

    for equation in context['equations']:
        roots, strategy_name = solver.solve(equation)
        context['results'].append({
            'equation': str(equation),
            'type': equation.get_type(),
            'roots': roots,
            'root_count': len(roots)
        })


@then('должны быть получены правильные результаты')
def step_should_get_correct_results(context):
    # Проверяем результаты для каждого уравнения
    assert len(context['results']) == 3

    # Проверяем биквадратное уравнение
    biquad_result = context['results'][0]
    assert biquad_result['type'] == 'biquadratic'
    assert biquad_result['root_count'] == 4

    # Проверяем квадратное уравнение
    quad_result = context['results'][1]
    assert quad_result['type'] == 'quadratic'
    assert quad_result['root_count'] == 2

    # Проверяем линейное уравнение
    linear_result = context['results'][2]
    assert linear_result['type'] == 'linear'
    assert linear_result['root_count'] == 1
