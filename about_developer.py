import json
class DeveloperInfo:
    @staticmethod
    def load_config():
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def get_developer_info():
        config = DeveloperInfo.load_config()
        dev_config = config.get('developer', {})

        return {
            "name": dev_config.get("name", "Гайданович Максим Иванович"),
            "email": dev_config.get("email", "@example.com"),
            "version": dev_config.get("version", "911"),
            "year": dev_config.get("year", "2025"),
            "credits": [
                "Использованные технологии:",
                "- Python 3.11",
                "- Tkinter для GUI",
                "- Pillow для обработки изображений",
                "- Pygame для звуковых эффектов"
            ],
            "license": "BNtу",
            "description": "Калькулятор с расширенными функциями и поддержкой тем оформления"
        }

    @staticmethod
    def get_formatted_info():
        info = DeveloperInfo.get_developer_info()
        formatted = [
            f"Разработчик: {info['name']}",
            f"Версия: {info['version']}",
            f"Год: {info['year']}",
            f"Email: {info['email']}",
            "",
            *info['credits'],
            "",
            f"Лицензия: {info['license']}",
            "",
            info['description']
        ]
        return "\n".join(formatted)