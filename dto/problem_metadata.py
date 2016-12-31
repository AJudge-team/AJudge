from typing import List


class ProblemMetadata:
    def __init__(self,
                 problem_id: str=None,
                 inputs: List[str]=None,
                 outputs: List[str]=None):
        self.__problem_id = problem_id
        self.__inputs = inputs
        self.__outputs = outputs

    @property
    def problem_id(self) -> str:
        return self.__problem_id

    @problem_id.setter
    def problem_id(self, value: str):
        self.__problem_id = value

    @property
    def inputs(self):
        return self.__inputs

    @inputs.setter
    def inputs(self, value: List[str]):
        self.__inputs = value

    @property
    def outputs(self):
        return self.__outputs

    @outputs.setter
    def outputs(self, value: List[str]):
        self.__outputs = value
