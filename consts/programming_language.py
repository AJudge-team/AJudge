from enum import Enum


class ProgrammingLanguage(Enum):
    C = 1
    CPP = 2
    JAVA = 3
    PYTHON = 4

    @staticmethod
    def get_proper_programming_language(name: str) -> 'ProgrammingLanguage':

        name = name.lower()

        prog = None

        if name == 'cpp' or name == 'c++':
            prog = ProgrammingLanguage.CPP

        elif name == 'c':
            prog = ProgrammingLanguage.C

        elif name == 'java':
            prog = ProgrammingLanguage.JAVA

        elif name == 'python':
            prog = ProgrammingLanguage.PYTHON

        return prog
