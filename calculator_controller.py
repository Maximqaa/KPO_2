from calculator_model import CalculatorModel
from command_handler import CommandHandler

class CalculatorController:
    def __init__(self, root, config=None):
        from calculator_view import CalculatorView
        self.model = CalculatorModel()
        self.view = CalculatorView(root, self, config)  # передаем config
        self.command_handler = CommandHandler(self.model)
        self.model.add_observer(self.view)

    def add_to_expression(self, value):
        self.command_handler.handle_add(value)

    def delete_last_character(self):
        self.command_handler.handle_delete()

    def clear(self):
        self.command_handler.handle_clear()

    def append_operator(self, operator):
        self.command_handler.handle_append_operator(operator)

    def on_button_click(self, value):
        if value == "=":
            self.command_handler.handle_evaluate()
        elif value == "C":
            self.clear()
        elif value == "←":
            self.delete_last_character()
        else:
            self.add_to_expression(value)

    def show_history(self):
        history_text = "\n".join(self.model.get_history())
        self.view.show_history_dialog(history_text)

    def run(self):
        self.view.root.mainloop()