class Color:
    """Класс Цвет фигуры"""

    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        """Свойство для получения цвета"""
        return self._color

    @color.setter
    def color(self, value):
        """Сеттер для цвета"""
        self._color = value

    def __str__(self):
        return self._color
