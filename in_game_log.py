class InGameLog_:
    def __init__(self):
        self.messages: list[str] = []

    def add_message(self, message: str):
        self.messages.append(message)

class InGameLog:
    log = InGameLog_()

    @staticmethod
    def add_message(message: str):
        InGameLog.log.add_message(message)
