from .figure import Figure
from .color import Color
import math

class Rectangle(Figure):
    """Класс Прямоугольник"""

    NAME = "Прямоугольник"

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = Color(color)

    @property
    def name(self):
        return self.NAME

    def area(self):
        """Вычисление площади прямоугольника"""
        return self.width * self.height

    def __str__(self):
        return "{} {} цвета шириной {} и высотой {} площадью {}.".format(
            self.name,
            self.color.color,
            self.width,
            self.height,
            self.area()
        )
