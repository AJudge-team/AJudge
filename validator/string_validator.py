from . validator_mixin import ValidatorMixin


class StringValidator(ValidatorMixin):
    def validate(self, str1: str, str2: str) -> bool:
        return str1 == str2
