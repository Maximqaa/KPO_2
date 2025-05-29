from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddToExpressionCommand(Command):
    def __init__(self, model, value):
        self.model = model
        self.value = value

    def execute(self):
        self.model.add_to_expression(self.value)

class DeleteLastCharacterCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self):
        self.model.delete_last_character()

class ClearCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self):
        self.model.clear()

class AppendOperatorCommand(Command):
    def __init__(self, model, operator):
        self.model = model
        self.operator = operator

    def execute(self):
        self.model.append_operator(self.operator)

class EvaluateCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self):
        return self.model.evaluate()