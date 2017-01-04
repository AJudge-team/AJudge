
class JudgeContext:
    def __init__(self,
                 problem_id: str=None,
                 source_code: str=None,
                 programming_language: str=None):
        self.__problem_id = problem_id
        self.__source_code = source_code
        self.__programming_language = programming_language

    @property
    def problem_id(self) -> str:
        return self.__problem_id

    @problem_id.setter
    def problem_id(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError

        self.__problem_id = value

    @property
    def source_code(self) -> str:
        return self.__source_code

    @source_code.setter
    def source_code(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError

        self.__source_code = value

    @property
    def programming_language(self) -> str:
        return self.__programming_language

    @programming_language.setter
    def programming_language(self, value: str):
        if type(value) is not str:
            raise TypeError

        self.__programming_language = value

