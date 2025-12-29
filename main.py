from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square

# Импортируем установленный пакет colorama
from colorama import init, Fore, Back, Style

# Инициализируем colorama
init(autoreset=True)

def main():
    # Ваш вариант N (замените на ваш номер)
    N = 5  # Пример: 5 вариант

    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + "Демонстрация работы с геометрическими фигурами")
    print(Fore.CYAN + "=" * 50)

    # 1. Прямоугольник синего цвета шириной N и высотой N
    rect = Rectangle(N, N, "синего")
    print(Fore.GREEN + "1. " + str(rect))

    # 2. Круг зеленого цвета радиусом N
    circle = Circle(N, "зеленого")
    print(Fore.GREEN + "2. " + str(circle))

    # 3. Квадрат красного цвета со стороной N
    square = Square(N, "красного")
    print(Fore.GREEN + "3. " + str(square))

    print(Fore.CYAN + "=" * 50)

    # Демонстрация работы с установленным пакетом colorama
    print(Fore.MAGENTA + "\nДемонстрация работы с пакетом colorama:")
    print(Fore.RED + "Этот текст красного цвета")
    print(Back.GREEN + Fore.BLACK + "Этот текст на зеленом фоне")
    print(Style.BRIGHT + Fore.BLUE + "Этот текст яркий и синий")

    # Вызов методов из установленного пакета
    print(Fore.MAGENTA + "\nЦвета в colorama:")
    print(f"Fore.RED: {Fore.RED}красный текст{Fore.RESET}")
    print(f"Fore.GREEN: {Fore.GREEN}зеленый текст{Fore.RESET}")
    print(f"Fore.BLUE: {Fore.BLUE}синий текст{Fore.RESET}")

    print(Fore.CYAN + "\n" + "=" * 50)
    print(Fore.YELLOW + "Программа завершена успешно!")
    print(Fore.CYAN + "=" * 50)

if __name__ == "__main__":
    main()
