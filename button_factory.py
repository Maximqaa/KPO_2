import tkinter as tk


class ButtonFactory:
    @staticmethod
    def create_button(frame, text, bg, fg, font, command, grid_args):
        button = tk.Button(frame, text=text, bg=bg, fg=fg, font=font, borderwidth=0, command=command)
        button.grid(**grid_args)
        return button