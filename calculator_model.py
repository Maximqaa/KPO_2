class CalculatorModel:
    def __init__(self):
        self.total_expression = ""
        self.current_expression = ""
        self.history = []
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

    def add_to_expression(self, value):
        if value == '.' and '.' in self.current_expression:
            return
        self.current_expression += str(value)
        self.notify_observers()

    def delete_last_character(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
        self.notify_observers()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.notify_observers()

    def append_operator(self, operator):
        if self.current_expression == "" and self.total_expression == "":
            return
        if self.current_expression == "" and self.total_expression[-1] in {"+", "-", "*", "/"}:
            return
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.notify_observers()

    def evaluate(self):
        try:
            if "/0" in self.total_expression:
                raise ZeroDivisionError("Деление на ноль невозможно")
            self.total_expression += self.current_expression
            result = str(eval(self.total_expression))
            self.history.append(f"{self.total_expression} = {result}")
            self.total_expression = ""
            self.current_expression = result
            self.notify_observers()
            return result
        except ZeroDivisionError:
            return "Ошибка: деление на 0"
        except Exception:
            return "Ошибка"

    def get_current_expression(self):
        return self.current_expression

    def get_total_expression(self):
        return self.current_expression

    def get_history(self):
        return self.history