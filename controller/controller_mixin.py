from abc import ABC, abstractmethod
from dto import JudgeContext, RuntimeContext


class ControllerMixin(ABC):

    @abstractmethod
    def handle_judge_context(self, judge_context: JudgeContext) -> RuntimeContext:
        pass
