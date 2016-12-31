class ProblemMetadata:
    def __init__(self, problem_id: str=None):
        self.__problem_id = problem_id

    @property
    def problem_id(self) -> str:
        return self.__problem_id

    @problem_id.setter
    def problem_id(self, value: str):
        self.__problem_id = value
