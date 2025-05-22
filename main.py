import tkinter as tk
from calculator_controller import CalculatorController


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorController(root)
    app.run()