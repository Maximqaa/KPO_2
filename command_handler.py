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
        command = AddToExpressionCommand(self.model, value)
        command.execute()

    def handle_delete(self):
        command = DeleteLastCharacterCommand(self.model)
        command.execute()

    def handle_clear(self):
        command = ClearCommand(self.model)
        command.execute()

    def handle_append_operator(self, operator):
        command = AppendOperatorCommand(self.model, operator)
        command.execute()

    def handle_evaluate(self):
        command = EvaluateCommand(self.model)
        return command.execute()
