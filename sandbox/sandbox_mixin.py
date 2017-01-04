from abc import ABC, abstractmethod


class SandboxMixin(ABC):

    @abstractmethod
    def exec(self, cmd: str):
        pass
