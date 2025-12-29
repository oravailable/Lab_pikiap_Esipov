from .figure import Figure
from .color import Color
import math

class Circle(Figure):
    """Класс Круг"""

    NAME = "Круг"

    def __init__(self, radius, color):
        self.radius = radius
        self.color = Color(color)

    @property
    def name(self):
        return self.NAME

    def area(self):
        """Вычисление площади круга"""
        return math.pi * self.radius ** 2

    def __str__(self):
        return "{} {} цвета радиусом {} площадью {:.2f}.".format(
            self.name,
            self.color.color,
            self.radius,
            self.area()
        )
