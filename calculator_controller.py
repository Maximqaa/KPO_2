from calculator_model import CalculatorModel
from calculator_view import CalculatorView


class CalculatorController:
    def __init__(self, root):
        """
        Инициализация контроллера калькулятора.
        """
        self.model = CalculatorModel()
        self.view = CalculatorView(root, self)

        # Инициализация отображения
        self.update_view()

    def add_to_expression(self, value):
        """
        Добавление символа в текущее выражение.
        """
        self.model.add_to_expression(value)
        self.update_view()

    def delete_last_character(self):
        """
        Удаление последнего символа из текущего выражения.
        """
        self.model.delete_last_character()
        self.update_view()

    def clear(self):
        """
        Очистка текущего и полного выражения.
        """
        self.model.clear()
        self.update_view()

    def append_operator(self, operator):
        """
        Добавление оператора в выражение.
        """
        self.model.append_operator(operator)
        self.update_view()

    def on_button_click(self, value):
        """
        Обработка нажатия кнопки.
        """
        if value == "=":
            result = self.model.evaluate()
            self.update_view()
        elif value == "C":
            self.clear()
        elif value == "←":
            self.delete_last_character()
        else:
            self.add_to_expression(value)

    def show_history(self):
        """
        Отображение истории вычислений.
        """
        history_text = "\n".join(self.model.get_history())
        self.view.show_history_dialog(history_text)

    def update_view(self):
        """
        Обновление отображения на основе данных модели.
        """
        self.view.update_display(
            self.model.get_current_expression(),
            self.model.get_total_expression()
        )

    def run(self):
        """
        Запуск приложения.
        """
        self.view.root.mainloop()