import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
import pygame
import threading
from about_developer import DeveloperInfo

# Глобальная переменная для хранения текущего звука
current_sound = None
sound_lock = threading.Lock()


def play_sound():
    global current_sound

    def _play():
        global current_sound
        try:
            with sound_lock:
                if current_sound:
                    current_sound.stop()
                sound_path = "button_hover.wav"
                if os.path.exists(sound_path):
                    pygame.mixer.init()
                    current_sound = pygame.mixer.Sound(sound_path)
                    current_sound.play()
        except Exception as e:
            print("Ошибка воспроизведения звука:", e)

    threading.Thread(target=_play, daemon=True).start()


class CalculatorView:
    def __init__(self, root, controller, config=None):
        self.root = root
        self.controller = controller
        self.config = config or {}

        # Загрузка текущей темы
        self.theme = self._load_theme()

        # Применение стилей
        self.root.configure(bg=self.theme["background"])
        self.create_menu()

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (2, 0), 8: (2, 1), 9: (2, 2),
            4: (3, 0), 5: (3, 1), 6: (3, 2),
            1: (4, 0), 2: (4, 1), 3: (4, 2),
            0: (5, 2), '.': (5, 0)
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

    def _load_theme(self):
        theme_name = self.config.get("theme", "light")
        themes = self.config.get("themes", {})

        if theme_name in themes:
            return themes[theme_name]
        else:
            print(f"Тема '{theme_name}' не найдена. Используется светлая тема.")
            return themes.get("light", {
                "background": "#f0f0f0",
                "button_background": "#ffffff",
                "text_color": "#000000",
                "font": "Arial",
                "font_size": 18
            })

    def update(self):
        current_exp = self.controller.model.get_current_expression()
        total_exp = self.controller.model.get_total_expression()
        self.label.config(text=current_exp)
        self.total_label.config(text=total_exp)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="История", command=self.controller.show_history)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="О программе", command=self.show_about)
        helpmenu.add_command(label="Настройки", command=self.show_settings)
        menubar.add_cascade(label="Помощь", menu=helpmenu)

        self.root.config(menu=menubar)

    def show_about(self):
        info = DeveloperInfo.get_formatted_info()
        messagebox.showinfo("О разработчике", info)

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")

        tk.Label(settings_window, text="Введите имя пользователя:").pack(pady=5)
        entry = tk.Entry(settings_window)
        entry.pack(pady=5)

        def save_name():
            name = entry.get()
            messagebox.showinfo("Сохранено", f"Имя сохранено: {name}")
            settings_window.destroy()

        tk.Button(settings_window, text="Сохранить", command=save_name).pack(pady=10)

    def show_history_dialog(self, history_text):
        dialog = tk.Toplevel(self.root)
        dialog.title("История вычислений")

        bg_image = Image.open("dialog_bg.png")
        bg_image = bg_image.resize((400, 300), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        canvas = tk.Canvas(dialog, width=400, height=300)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=bg_photo)

        label = tk.Label(dialog, text=history_text, justify="left", bg="white", font=("Arial", 12))
        canvas.create_window(200, 150, window=label)

        dialog.mainloop()

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.controller.on_button_click("="))
        for key in self.digits:
            self.root.bind(str(key), lambda e, d=key: [self.controller.add_to_expression(d), play_sound()])
        for key in self.operations:
            self.root.bind(key, lambda e, o=key: [self.controller.append_operator(o), play_sound()])
        self.root.bind("(", lambda e: [self.controller.add_to_expression("("), play_sound()])
        self.root.bind(")", lambda e: [self.controller.add_to_expression(")"), play_sound()])
        self.root.bind("<BackSpace>", lambda e: [self.controller.delete_last_character(), play_sound()])

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
        bg = self.theme["button_background"]
        fg = self.theme["text_color"]
        font_name = self.theme["font"]
        font_size = self.theme["font_size"]
        from button_factory import create_button
        for digit, grid_value in self.digits.items():
            create_button(
                frame=self.buttons_frame,
                text=str(digit),
                bg=bg,
                fg=fg,
                font=(font_name, font_size),
                command=partial(self.controller.add_to_expression, digit),
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
                command=partial(self.controller.append_operator, operator),
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
            command=lambda: [self.controller.add_to_expression("("), play_sound()],
            grid_args={"row": 1, "column": 0,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )
        create_button(
            frame=self.buttons_frame,
            text=")",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: [self.controller.add_to_expression(")"), play_sound()],
            grid_args={"row": 1, "column": 1,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_history_button()
        self.create_exit_button()
        self.create_backspace_button()
        self.create_about_button()

    def create_about_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="О разработчике",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 12),
            command=lambda: [self.show_about(), play_sound()],
            grid_args={"row": 0, "column": 0, "columnspan": 2,
                      "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )

    def create_clear_button(self):
        from button_factory import create_button
        create_button(
            frame=self.buttons_frame,
            text="C",
            bg="#ff6666",
            fg="#000000",
            font=("Arial", 18),
            command=lambda: [self.controller.clear(), play_sound()],
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
            command=lambda: [self.controller.on_button_click("="), play_sound()],
            grid_args={"row": 5, "column": 3, "columnspan": 1,
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
            command=lambda: [self.controller.show_history(), play_sound()],
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
            command=lambda: [self.controller.delete_last_character(), play_sound()],
            grid_args={"row": 0, "column": 2,
                       "sticky": tk.NSEW, "padx": 5, "pady": 5}
        )