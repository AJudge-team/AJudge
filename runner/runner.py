from abc import ABC, abstractmethod
from dto import RuntimeContext
from sandbox import SandboxMixin


class Runner(ABC):
    @abstractmethod
    def prepare(self, runtime_context: RuntimeContext) -> SandboxMixin:
        pass

    @abstractmethod
    def run(self, runtime_context: RuntimeContext, sandbox: SandboxMixin):
        pass
