import tkinter as tk
from tkinter import messagebox

class CalculatorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Калькулятор")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (2, 0), 8: (2, 1), 9: (2, 2),
            4: (3, 0), 5: (3, 1), 6: (3, 2),
            1: (4, 0), 2: (4, 1), 3: (4, 2),
            0: (5, 1), '.': (5, 0)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.brackets = {"(": "(", ")": ")"}

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_bracket_buttons()
        self.create_special_buttons()
        self.bind_keys()

        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.buttons_frame.grid_columnconfigure(j, weight=1)

    def update(self):
        current_exp = self.controller.model.get_current_expression()
        total_exp = self.controller.model.get_total_expression()
        self.label.config(text=current_exp)
        self.total_label.config(text=total_exp)

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.controller.on_button_click("="))
        for key in self.digits:
            self.root.bind(str(key), lambda event, digit=key: self.controller.add_to_expression(digit))
        for key in self.operations:
            self.root.bind(key, lambda event, operator=key: self.controller.append_operator(operator))
        self.root.bind("(", lambda event: self.controller.add_to_expression("("))
        self.root.bind(")", lambda event: self.controller.add_to_expression(")"))
        self.root.bind("<BackSpace>", lambda event: self.controller.delete_last_character())

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text="", anchor=tk.E,
                               bg="#f0f0f0", fg="#666666",
                               padx=24, font=("Arial", 16))
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text="", anchor=tk.E,
                         bg="#f0f0f0", fg="#000000",
                         padx=24, font=("Arial", 40, "bold"))
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.root, height=221, bg="#f0f0f0")
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")
        return frame

    def create_digit_buttons(self):
        from button_factory import create_button
        for digit, grid_value in self.digits.items():
            create_button(
                frame=self.buttons_frame,
                text=str(digit),
                bg="#ffffff",
                fg="#000000",
                font=("Arial", 18),
                command=lambda x=digit: self.controller.add_to_expression(x),
                grid_args={"row": grid_value[0], "column": grid_value[1],
                           "sticky": tk.NSEW, "padx": 5, "pady": 5}
            )

    def create_operator_buttons(self):
        from button_factory import create_button
        i = 1
        for operator, symbol in self.operations.items():
            create_button(
                frame=self.buttons_frame,
                text=symbol,
                bg="#f0f0f0",
                fg="#000000",
                font=("Arial", 18),
                command=lambda x=operator: self.controller.append_operator(x),
                grid_args={"row": i, "column": 3,
                           "sticky": tk.NSEW, "padx": 5, "pady": 5}
            )
            i += 1

    def create_bracket_buttons(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="(",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: self.controller.add_to_expression("("),
            grid_args={"row": 1, "column": 0,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )
        create_button(
            frame=self.buttons_frame,
            text=")",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: self.controller.add_to_expression(")"),
            grid_args={"row": 1, "column": 1,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_history_button()
        self.create_exit_button()
        self.create_backspace_button()

    def create_clear_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="C",
            bg="#ff6666",
            fg="#000000",
            font=("Arial", 18),
            command=self.controller.clear,
            grid_args={"row": 1, "column": 2,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_equals_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="=",
            bg="#66ff66",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: self.controller.on_button_click("="),
            grid_args={"row": 5, "column": 2, "columnspan": 2,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_history_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="История",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=self.controller.show_history,
            grid_args={"row": 0, "column": 3,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_exit_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="Выход",
            bg="#ff6666",
            fg="#000000",
            font=("Arial", 18),
            command=self.root.quit,
            grid_args={"row": 5, "column": 0, "columnspan": 2,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_backspace_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="←",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=self.controller.delete_last_character,
            grid_args={"row": 0, "column": 2,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def show_history_dialog(self, history_text):
        messagebox.showinfo("История вычислений", history_text)