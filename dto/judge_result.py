
class JudgeResult:
    def __init__(self,
                 is_accepted: bool=None,
                 message: str=None,
                 error_type: Exception=None):
        self.__is_accepted = is_accepted
        self.__message = message

    @property
    def is_accepted(self):
        return self.__is_accepted

    @is_accepted.setter
    def is_accepted(self, is_accepted: bool):
        self.__is_accepted = is_accepted

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value

