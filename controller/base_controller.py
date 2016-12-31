from . controller_mixin import ControllerMixin
from dto import JudgeContext, RuntimeContext, JudgeResult
from sandbox import SandboxMixin


# class implementation for controller interface
class BaseController(ControllerMixin):
    def analyze(self, judge_context: JudgeContext) -> RuntimeContext:
        pass

    def choose_sandbox(self, runtime_context: RuntimeContext) -> SandboxMixin:
        pass

    def handle(self, judge_context: JudgeContext) -> JudgeResult:
        pass
