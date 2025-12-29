import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.LinkedHashSet;
import java.util.Collections;

public class BiquadraticEquationSolver {

    // Класс для представления биквадратного уравнения
    static class BiquadraticEquation {
        private double a;
        private double b;
        private double c;
        private List<Double> roots;
        private Double discriminant;

        public BiquadraticEquation(double a, double b, double c) {
            if (a == 0) {
                throw new IllegalArgumentException("Коэффициент A не может быть равен 0 для биквадратного уравнения.");
            }
            this.a = a;
            this.b = b;
            this.c = c;
            this.roots = new ArrayList<>();
            this.discriminant = null;
        }

        public List<Double> solve() {
            // Вычисляем дискриминант для t = x^2
            discriminant = b * b - 4 * a * c;
            roots.clear();

            if (discriminant < 0) {
                return roots;
            }

            if (discriminant == 0) {
                double t = -b / (2 * a);
                addRootsFromT(t);
            } else {
                double t1 = (-b + Math.sqrt(discriminant)) / (2 * a);
                double t2 = (-b - Math.sqrt(discriminant)) / (2 * a);
                addRootsFromT(t1);
                addRootsFromT(t2);
            }

            return roots;
        }

        private void addRootsFromT(double t) {
            if (t > 0) {
                double x1 = Math.sqrt(t);
                double x2 = -Math.sqrt(t);
                roots.add(x1);
                roots.add(x2);
            } else if (t == 0 && !roots.contains(0.0)) {
                roots.add(0.0);
            }
        }

        public Double getDiscriminant() {
            return discriminant;
        }

        public String getFormattedEquation() {
            return String.format("%.2fx^4 + %.2fx^2 + %.2f = 0", a, b, c);
        }

        public List<Double> getRoots() {
            return new ArrayList<>(roots);
        }
    }

    // Метод для проверки, является ли строка числом
    public static boolean isValidNumber(String str) {
        try {
            Double.parseDouble(str);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    // Метод для получения коэффициента
    public static double getCoefficient(Scanner scanner, String coefficientName,
                                      String[] args, int index) {
        // Пробуем получить из аргументов командной строки
        if (args != null && args.length > index && isValidNumber(args[index])) {
            return Double.parseDouble(args[index]);
        } else if (args != null && args.length > index) {
            System.out.printf("Некорректное значение коэффициента %s в аргументах. ", coefficientName);
        }

        // Запрашиваем с клавиатуры
        while (true) {
            System.out.printf("Введите коэффициент %s: ", coefficientName);
            String input = scanner.nextLine();

            if (isValidNumber(input)) {
                double value = Double.parseDouble(input);

                // Проверка для коэффициента A
                if (coefficientName.equals("A") && value == 0) {
                    System.out.println("Коэффициент A не может быть равен 0. Пожалуйста, введите другое значение.");
                    continue;
                }

                return value;
            } else {
                System.out.println("Некорректное значение. Пожалуйста, введите действительное число.");
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Решение биквадратного уравнения: Ax^4 + Bx^2 + C = 0");
        System.out.println("=".repeat(50));

        try {
            // Получаем коэффициенты
            double a = getCoefficient(scanner, "A", args, 0);
            double b = getCoefficient(scanner, "B", args, 1);
            double c = getCoefficient(scanner, "C", args, 2);

            // Создаем и решаем уравнение
            BiquadraticEquation equation = new BiquadraticEquation(a, b, c);

            System.out.printf("\nУравнение: %s\n", equation.getFormattedEquation());
            System.out.println("=".repeat(50));

            List<Double> roots = equation.solve();
            Double discriminant = equation.getDiscriminant();

            System.out.printf("Дискриминант D = %.3f\n", discriminant);

            if (discriminant != null) {
                if (discriminant < 0) {
                    System.out.println("Действительных корней нет.");
                } else {
                    if (!roots.isEmpty()) {
                        // Убираем дубликаты и сортируем
                        LinkedHashSet<Double> uniqueRoots = new LinkedHashSet<>(roots);
                        List<Double> sortedRoots = new ArrayList<>(uniqueRoots);
                        Collections.sort(sortedRoots);

                        System.out.printf("Найдено %d действительных корня(ей):\n", sortedRoots.size());
                        for (int i = 0; i < sortedRoots.size(); i++) {
                            System.out.printf("Корень %d: x = %.6f\n", i + 1, sortedRoots.get(i));
                        }
                    } else {
                        System.out.println("Действительных корней нет.");
                    }
                }
            }

            System.out.println("=".repeat(50));

        } catch (IllegalArgumentException e) {
            System.out.println("Ошибка: " + e.getMessage());
            System.out.println("Пожалуйста, запустите программу снова с корректными коэффициентами.");
        }

        System.out.print("\nНажмите Enter для выхода...");
        scanner.nextLine();
        scanner.close();
    }
}
