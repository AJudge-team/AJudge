from abc import ABC, abstractmethod
from dto import RuntimeContext
from sandbox import Sandbox


class Runner(ABC):
    @abstractmethod
    def prepare(self, runtime_context: RuntimeContext) -> Sandbox:
        pass

    @abstractmethod
    def run(self, runtime_context: RuntimeContext, sandbox: Sandbox):
        pass
