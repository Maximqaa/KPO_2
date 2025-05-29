import tkinter as tk
import json
import os
import sys
from calculator_controller import CalculatorController


def resource_path(relative_path):
    """ Для работы с ресурсами при компиляции в .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_config():
    config_path = resource_path("config.json")
    if not os.path.exists(config_path):
        print(f"Файл конфигурации не найден: {config_path}")
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Ошибка: файл конфигурации содержит неверный JSON.")
        return None
    except Exception as e:
        print(f"Не удалось загрузить конфигурацию: {e}")
        return None


if __name__ == "__main__":
    config = load_config()

    root = tk.Tk()
    root.title("Калькулятор")

    # Настройки окна из конфига
    window = config.get("window", {})
    theme_name = config.get("theme", "light")
    themes = config.get("themes", {})
    theme = themes.get(theme_name, themes.get("light"))

    width = window.get("width", 400)
    height = window.get("height", 550)
    resizable = window.get("resizable", False)
    root.geometry(f"{width}x{height}")
    root.resizable(resizable, resizable)

    # Установка иконки
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

    # Передаем конфиг в контроллер
    app = CalculatorController(root, config)
    app.run()