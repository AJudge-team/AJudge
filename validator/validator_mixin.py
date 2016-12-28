from abc import ABC, abstractmethod


class ValidatorMixin(ABC):

    @abstractmethod
    def validate(self, some1: any, some2: any) -> bool:
        pass
