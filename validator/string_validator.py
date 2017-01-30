from . validator_mixin import ValidatorMixin


class StringValidator(ValidatorMixin):

    def validate(self, str1: str, str2: str) -> bool:
        return str1 == str2

    def validate_with_erasing_all_spaces(self, str1: str, str2: str) -> bool:
        return self.validate(str1.split(), str2.split())

    def validate_with_erasing_trailing_spaces(self, str1: str, str2: str) -> bool:
        list1 = self.__erase_empty_lines_in_list(str1.split('\n'))
        list2 = self.__erase_empty_lines_in_list(str2.split('\n'))

        if len(list1) == len(list2):
            ed = len(list1)
            for i in range(ed):
                list1[i] = self.__erase_trailing_spaces_in_str(list1[i])
                list2[i] = self.__erase_trailing_spaces_in_str(list2[i])
                if self.validate(list1[i], list2[i]) is False:
                        return False
            return True
        else:
            return False

    @classmethod
    def __erase_empty_lines_in_list(cls, target: list) -> list:
        ed = len(target)-1
        for i in range(ed, 0, -1):
            if target[i] == '':
                target.pop(i)
        return target

    @classmethod
    def __erase_trailing_spaces_in_str(cls, target: str) -> str:
        sp = len(target)
        ed = sp-1
        for i in range(ed, 0, -1):
            if target[i] == ' ':
                sp = i
            else:
                break
        return target[:sp]

