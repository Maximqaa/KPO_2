import tkinter as tk
from tkinter import messagebox
from calculator_logic import CalculatorLogic
from button_factory import ButtonFactory


class CalculatorUI:
    def __init__(self, root):
        """
        Инициализация пользовательского интерфейса.
        """
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.calculator_logic = CalculatorLogic()  # Создаем экземпляр логики
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        self.total_label, self.label = self.create_display_labels()  # Метки для отображения

        self.digits = {
            7: (2, 0), 8: (2, 1), 9: (2, 2),
            4: (3, 0), 5: (3, 1), 6: (3, 2),
            1: (4, 0), 2: (4, 1), 3: (4, 2),
            0: (5, 1), '.': (5, 0)
        }
        # Словарь для операторов (символы Unicode для красивого отображения)
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        # Словарь для скобок
        self.brackets = {"(": "(", ")": ")"}
        # Создание кнопок
        self.create_digit_buttons()  # Цифровые кнопки
        self.create_operator_buttons()  # Кнопки операторов
        self.create_bracket_buttons()  # Кнопки скобок
        self.create_special_buttons()  # Специальные кнопки (C, =, История, Выход, ←)
        self.bind_keys()

        for i in range(6):  # Настройка строк
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):  # Настройка столбцов
            self.buttons_frame.grid_columnconfigure(j, weight=1)

    def bind_keys(self):
        """
        Привязка клавиш клавиатуры к функциям калькулятора.
        """
        self.root.bind("<Return>", lambda event: self.on_button_click("="))
        for key in self.digits:
            self.root.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.root.bind(key, lambda event, operator=key: self.append_operator(operator))
        self.root.bind("(", lambda event: self.add_to_expression("("))
        self.root.bind(")", lambda event: self.add_to_expression(")"))
        self.root.bind("<BackSpace>", lambda event: self.delete_last_character())

    def create_display_labels(self):
        """
        Создание меток для отображения ввода и результата.
        """
        total_label = tk.Label(self.display_frame, text=self.calculator_logic.get_total_expression(), anchor=tk.E,
                               bg="#f0f0f0",
                               fg="#666666", padx=24, font=("Arial", 16))
        total_label.pack(expand=True, fill='both')
        label = tk.Label(self.display_frame, text=self.calculator_logic.get_current_expression(), anchor=tk.E,
                         bg="#f0f0f0",
                         fg="#000000", padx=24, font=("Arial", 40, "bold"))
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_display_frame(self):
        """
        Создание фрейма для отображения ввода и результата.
        """
        frame = tk.Frame(self.root, height=221, bg="#f0f0f0")
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        """
        Создание фрейма для кнопок.
        """
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        """
        Добавление символа в текущее выражение.
        """
        self.calculator_logic.add_to_expression(value)
        self.update_display()

    def delete_last_character(self):
        """
        Удаление последнего символа из текущего выражения.
        """
        self.calculator_logic.delete_last_character()
        self.update_display()

    def create_digit_buttons(self):
        """
        Создание кнопок для цифр и точки.
        """
        for digit, grid_value in self.digits.items():
            ButtonFactory.create_button(
                frame=self.buttons_frame,
                text=str(digit),
                bg="#ffffff",
                fg="#000000",
                font=("Arial", 18),
                command=lambda x=digit: self.add_to_expression(x),
                grid_args={"row": grid_value[0], "column": grid_value[1], "sticky": tk.NSEW, "padx": 5, "pady": 5}
            )

    def append_operator(self, operator):
        """
        Добавление оператора в выражение.
        """
        self.calculator_logic.append_operator(operator)
        self.update_display()

    def create_operator_buttons(self):
        """
        Создание кнопок для операторов (+, -, *, /).
        """
        i = 1
        for operator, symbol in self.operations.items():
            ButtonFactory.create_button(
                frame=self.buttons_frame,
                text=symbol,
                bg="#f0f0f0",
                fg="#000000",
                font=("Arial", 18),
                command=lambda x=operator: self.append_operator(x),
                grid_args={"row": i, "column": 3, "sticky": tk.NSEW, "padx": 5, "pady": 5}
            )
            i += 1

    def create_bracket_buttons(self):
        """
        Создание кнопок для скобок.
        """
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text="(",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: self.add_to_expression("("),
            grid_args={"row": 1, "column": 0, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text=")",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: self.add_to_expression(")"),
            grid_args={"row": 1, "column": 1, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def clear(self):
        """
        Очистка текущего и полного выражения.
        """
        self.calculator_logic.clear()
        self.update_display()

    def create_special_buttons(self):
        """
        Создание специальных кнопок (C, =, История, Выход, ←).
        """
        self.create_clear_button()
        self.create_equals_button()
        self.create_history_button()
        self.create_exit_button()
        self.create_backspace_button()

    def create_clear_button(self):
        """
        Создание кнопки "C" для очистки выражения.
        """
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text="C",
            bg="#ff6666",
            fg="#000000",
            font=("Arial", 18),
            command=self.clear,
            grid_args={"row": 1, "column": 2, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_equals_button(self):
        """
        Создание кнопки "=" для вычисления результата.
        """
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text="=",
            bg="#66ff66",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: self.on_button_click("="),
            grid_args={"row": 5, "column": 2, "columnspan": 2, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_history_button(self):
        """
        Создание кнопки "История" для отображения истории вычислений.
        """
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text="История",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=self.show_history,
            grid_args={"row": 0, "column": 3, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_exit_button(self):
        """
        Создание кнопки "Выход" для закрытия приложения.
        """
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text="Выход",
            bg="#ff6666",
            fg="#000000",
            font=("Arial", 18),
            command=self.root.quit,
            grid_args={"row": 5, "column": 0, "columnspan": 2, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_backspace_button(self):
        """
        Создание кнопки "←" для удаления последнего символа.
        """
        ButtonFactory.create_button(
            frame=self.buttons_frame,
            text="←",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=self.delete_last_character,
            grid_args={"row": 0, "column": 2, "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def on_button_click(self, value):
        """
        Обработка нажатия кнопки.
        :param value: Значение кнопки.
        """
        if value == "=":
            result = self.calculator_logic.evaluate()
            self.label.config(text=result)
        elif value == "C":
            self.clear()
        elif value == "←":
            self.delete_last_character()
        else:
            self.add_to_expression(value)

    def update_display(self):
        """
        Обновление отображения текущего выражения.
        """
        self.label.config(text=self.calculator_logic.get_current_expression())
        self.total_label.config(text=self.calculator_logic.get_total_expression())

    def show_history(self):
        """
        Отображение истории вычислений в виде всплывающего окна.
        """
        history_text = "\n".join(self.calculator_logic.get_history())
        messagebox.showinfo("История вычислений", history_text)

    def run(self):
        """
        Запуск приложения.
        """
        self.root.mainloop()


# Точка входа в программу
if __name__ == "__main__":
    root = tk.Tk()  # Создание главного окна
    app = CalculatorUI(root)  # Создание экземпляра калькулятора
    app.run()  # Запуск приложения