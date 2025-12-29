from abc import ABC, abstractmethod

class Figure(ABC):
    """Абстрактный класс Геометрическая фигура"""

    @abstractmethod
    def area(self):
        """Абстрактный метод для вычисления площади фигуры"""
        pass

    @property
    @abstractmethod
    def name(self):
        """Абстрактное свойство для получения названия фигуры"""
        pass

    def __repr__(self):
        return self.__str__()
