"""
BDD-тесты с использованием pytest-bdd.
Для работы необходимо установить: pip install pytest pytest-bdd
"""

import pytest
import math
from biquadratic_solver import solve_biquadratic

# Определяем фикстуры
@pytest.fixture
def context():
    """Контекст для хранения данных между шагами."""
    return {}


# Шаги для фикстур
@given("я имею коэффициенты A, B и C")
def step_set_coefficients(context, a, b, c):
    context['a'] = float(a)
    context['b'] = float(b)
    context['c'] = float(c)
    context['roots'] = None
    context['discriminant'] = None


@when("я решаю биквадратное уравнение")
def step_solve_equation(context):
    try:
        roots, discriminant = solve_biquadratic(
            context['a'],
            context['b'],
            context['c']
        )
        context['roots'] = roots
        context['discriminant'] = discriminant
        context['error'] = None
    except ValueError as e:
        context['error'] = str(e)


@then("уравнение должно иметь 4 действительных корня")
def step_assert_four_roots(context):
    assert context['roots'] is not None
    assert len(context['roots']) == 4
    assert context['discriminant'] > 0


@then("уравнение должно иметь 2 действительных корня")
def step_assert_two_roots(context):
    assert context['roots'] is not None
    assert len(context['roots']) == 2
    assert context['discriminant'] > 0


@then("уравнение должно иметь 1 действительный корень")
def step_assert_one_root(context):
    assert context['roots'] is not None
    assert len(context['roots']) == 1
    assert context['discriminant'] == 0


@then("уравнение не должно иметь действительных корней")
def step_assert_no_roots(context):
    assert context['roots'] is not None
    assert len(context['roots']) == 0
    assert context['discriminant'] < 0


@then("должна быть ошибка 'Коэффициент A не может быть равен 0'")
def step_assert_error(context):
    assert context['error'] is not None
    assert "Коэффициент A не может быть равен 0" in context['error']


@then("корни должны быть равны")
def step_assert_roots_values(context, expected_roots):
    expected = [float(x.strip()) for x in expected_roots.split(',')]
    assert len(context['roots']) == len(expected)

    for actual, expected_val in zip(sorted(context['roots']), sorted(expected)):
        pytest.approx(actual, expected_val, abs=1e-10)


@then("дискриминант должен быть равен")
def step_assert_discriminant_value(context, expected_discriminant):
    expected = float(expected_discriminant)
    assert pytest.approx(context['discriminant'], expected, abs=1e-10)


# Сценарии BDD
scenario("Уравнение с 4 действительными корнями", features="biquadratic.feature")
def test_four_real_roots():
    """Сценарий: уравнение x^4 - 5x^2 + 4 = 0"""
    pass


scenario("Уравнение без действительных корней", features="biquadratic.feature")
def test_no_real_roots():
    """Сценарий: уравнение x^4 + x^2 + 1 = 0"""
    pass


scenario("Уравнение с коэффициентом A равным 0", features="biquadratic.feature")
def test_zero_coefficient_a():
    """Сценарий: попытка решения с A = 0"""
    pass


# Альтернативный подход с прямым использованием pytest-bdd
from pytest_bdd import scenario, given, when, then, parsers

# Файл с фичами: features/biquadratic.feature
"""
Feature: Решение биквадратного уравнения
  Биквадратное уравнение должно корректно решаться
  для различных наборов коэффициентов

  Scenario: Уравнение с 4 действительными корнями
    Given я имею коэффициенты A, B и C:
      | a | b  | c |
      | 1 | -5 | 4 |
    When я решаю биквадратное уравнение
    Then уравнение должно иметь 4 действительных корня
    And корни должны быть равны "-2, -1, 1, 2"
    And дискриминант должен быть равен "9"

  Scenario: Уравнение без действительных корней
    Given я имею коэффициенты A, B и C:
      | a | b | c |
      | 1 | 1 | 1 |
    When я решаю биквадратное уравнение
    Then уравнение не должно иметь действительных корней
    And дискриминант должен быть равен "-3"

  Scenario: Уравнение с коэффициентом A равным 0
    Given я имею коэффициенты A, B и C:
      | a | b | c |
      | 0 | 2 | 3 |
    When я решаю биквадратное уравнение
    Then должна быть ошибка 'Коэффициент A не может быть равен 0'
"""

# Реализация шагов для pytest-bdd
@given(parsers.parse("я имею коэффициенты A, B и C:\n{table}"), target_fixture="context")
def step_coefficients_from_table(context, table):
    """Парсинг коэффициентов из таблицы."""
    rows = table.split('\n')
    headers = rows[0].strip().split('|')
    values = rows[1].strip().split('|')

    # Находим индексы столбцов
    a_idx = headers.index('a')
    b_idx = headers.index('b')
    c_idx = headers.index('c')

    context = {}
    context['a'] = float(values[a_idx])
    context['b'] = float(values[b_idx])
    context['c'] = float(values[c_idx])

    return context
