class JudgeSyntaxError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(JudgeSyntaxError, self).__init__(message)

        self.message = message

