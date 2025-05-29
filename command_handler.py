from commands import (
    AddToExpressionCommand,
    DeleteLastCharacterCommand,
    ClearCommand,
    AppendOperatorCommand,
    EvaluateCommand
)

class CommandHandler:
    def __init__(self, model):
        self.model = model

    def handle_add(self, value):
        AddToExpressionCommand(self.model, value).execute()

    def handle_delete(self):
        DeleteLastCharacterCommand(self.model).execute()

    def handle_clear(self):
        ClearCommand(self.model).execute()

    def handle_append_operator(self, operator):
        AppendOperatorCommand(self.model, operator).execute()

    def handle_evaluate(self):
        return EvaluateCommand(self.model).execute()