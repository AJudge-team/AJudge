from consts import ProgrammingLanguage
from . problem_metadata import ProblemMetadata


class RuntimeContext:
    def __init__(self,
                 programming_language: ProgrammingLanguage=None,
                 source_code: str=None,
                 problem_metadata: ProblemMetadata=None):
        self.__programming_language = programming_language
        self.__source_code = source_code
        self.__problem_metadata = problem_metadata

    @property
    def programming_language(self) -> ProgrammingLanguage:
        return self.__programming_language

    @programming_language.setter
    def programming_language(self, value: ProgrammingLanguage):
        self.__programming_language = value

    @property
    def source_code(self) -> str:
        return self.__source_code

    @source_code.setter
    def source_code(self, value: str):
        self.__source_code = value

    @property
    def problem_metadata(self) -> ProblemMetadata:
        return self.__problem_metadata

    @problem_metadata.setter
    def problem_metadata(self, value: ProblemMetadata):
        self.__problem_metadata = value

