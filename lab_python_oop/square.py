from .rectangle import Rectangle

class Square(Rectangle):
    """Класс Квадрат (наследуется от Прямоугольника)"""

    NAME = "Квадрат"

    def __init__(self, side, color):
        # Вызываем конструктор родительского класса
        super().__init__(side, side, color)

    @property
    def name(self):
        return self.NAME

    def __str__(self):
        return "{} {} цвета со стороной {} площадью {}.".format(
            self.name,
            self.color.color,
            self.width,  # или self.height - они равны
            self.area()
        )
