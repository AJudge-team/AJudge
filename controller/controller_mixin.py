from abc import ABC, abstractmethod
from dto import JudgeContext, JudgeResult, RuntimeContext
from sandbox import SandboxMixin


class ControllerMixin(ABC):

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
    def choose_sandbox(self, judge_context: JudgeContext) -> SandboxMixin:
        pass
