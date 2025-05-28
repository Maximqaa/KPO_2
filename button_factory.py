import tkinter as tk

def create_button(frame, text, bg, fg, font, command, grid_args):
    button = tk.Button(frame, text=text, bg=bg, fg=fg, font=font, borderwidth=0, command=command)
    button.bind("<Enter>", lambda e: button.config(cursor="hand2"))
    button.bind("<Leave>", lambda e: button.config(cursor=""))
    button.grid(**grid_args)
    return button