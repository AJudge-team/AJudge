from abc import ABC, abstractmethod
from dto import JudgeContext, JudgeResult, RuntimeContext
from runner import Runner
from validator import ValidatorMixin
from provider import ProblemProvider


class ControllerMixin(ABC):

    # a method to insert runner to controller
    @abstractmethod
    def add_runner(self, runner_name: str, runner: Runner) -> 'ControllerMixin':
        pass

    # a setter for validator
    @abstractmethod
    def set_validator(self, validator: ValidatorMixin) -> 'ControllerMixin':
        pass

    # a setter for problem provider
    @abstractmethod
    def set_problem_provider(self, problem_provider: ProblemProvider) -> 'ControllerMixin':
        pass

    # entry point for outer module to pass JudgeContext
    @abstractmethod
    def handle(self, judge_context: JudgeContext) -> JudgeResult:
        pass

    # a method to analyze given judge_context and generate runtime_context
    @abstractmethod
    def analyze(self, judge_context: JudgeContext) -> RuntimeContext:
        pass

    # a method to choose sandbox according to runtime_context
    @abstractmethod
    def choose_runner(self, judge_context: JudgeContext) -> Runner:
        pass
