
class JudgeResult:
    def __init__(self,
                 is_accepted: bool=None,
                 message: str=None,
                 peak_memory: int=0,
                 used_time: float=0,
                 error_type: Exception=None):
        self.__is_accepted = is_accepted
        self.__message = message
        self.__peak_memory = peak_memory
        self.__used_time = used_time

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

    @property
    def peak_memory(self):
        return self.__peak_memory

    @peak_memory.setter
    def peak_memory(self, value: int):
        self.__peak_memory = value

    @property
    def used_time(self):
        return self.__used_time

    @used_time.setter
    def used_time(self, value: int):
        self.__used_time = value