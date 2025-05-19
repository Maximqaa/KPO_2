class CalculatorLogic:
    def __init__(self):
        """
        Инициализация логики калькулятора.
        """
        self.total_expression = ""  # Полное выражение (история ввода)
        self.current_expression = ""  # Текущее выражение (отображается на экране)
        self.history = []  # История вычислений

    def add_to_expression(self, value):
        """
        Добавление символа в текущее выражение.
        """
        if value == '.' and '.' in self.current_expression:
            return
        self.current_expression += str(value)

    def delete_last_character(self):
        """
        Удаление последнего символа из текущего выражения.
        """
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]

    def clear(self):
        """
        Очистка текущего и полного выражения.
        """
        self.current_expression = ""
        self.total_expression = ""

    def append_operator(self, operator):
        """
        Добавление оператора в выражение.
        Оператор (+, -, *, /).
        """
        if self.current_expression == "" and self.total_expression == "":
            return
        if self.current_expression == "" and self.total_expression[-1] in {"+", "-", "*", "/"}:
            return
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""

    def evaluate(self):
        """
        Вычисление результата выражения.
        """
        try:
            if "/0" in self.total_expression:
                raise ZeroDivisionError("Деление на ноль невозможно")
            self.total_expression += self.current_expression
            result = str(eval(self.total_expression))
            self.history.append(f"{self.total_expression} = {result}")
            self.total_expression = ""
            self.current_expression = result
            return result
        except ZeroDivisionError:
            return "Ошибка: деление на 0"
        except Exception:
            return "Ошибка"

    def get_current_expression(self):
        """
        Получение текущего выражения.
        """
        return self.current_expression

    def get_total_expression(self):
        """
        Получение полного выражения.
        """
        return self.total_expression

    def get_history(self):
        """
        Получение истории вычислений.
        """
        return self.history