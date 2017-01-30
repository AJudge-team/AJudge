import unittest
import random
from validator import StringValidator


class StringValidatorClassTest(unittest.TestCase):
    def setUp(self):
        self.stringValidator = StringValidator()

    def test_validate_correct1(self):
        result = self.stringValidator.validate("abcdefg", "abcdefg")
        self.assertTrue(result)

    def test_validate_correct2(self):
        mpt = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        str1 = ""
        for i in range(0, 15):
            str1 += mpt[random.randint(0, 25)]

        str2 = (str1 + '.')[:-1]

        self.assertTrue(str1 is not str2)

        result = self.stringValidator.validate(str1, str2)
        self.assertTrue(result)

    def test_validate_incorrect1(self):
        result = self.stringValidator.validate("abc", "bca")
        self.assertFalse(result)

    def test_validate_incorrect2(self):
        result = self.stringValidator.validate("abc", " abc")
        self.assertFalse(result)

    def test_validate_incorrect3(self):
        result = self.stringValidator.validate("abc", "abc ")
        self.assertFalse(result)

    def test_validate_incorrect_type(self):
        self.assertRaises(TypeError, self.stringValidator.validate("123", 123))

    def test_validate_erasing_all_spaces(self):
        self.assertTrue(self.stringValidator.validate_with_erasing_all_spaces("1 2 3\n 4 \t 5", "1 2 3 4 5"))

    def test_validate_erasing_all_spaces2(self):
        self.assertTrue(self.stringValidator.validate_with_erasing_all_spaces("1 2 3\n 4 \t 5", "1 2 3 4 5            "))

    def test_validate_erasing_trailing_spaces(self):
        self.assertTrue(self.stringValidator.validate_with_erasing_trailing_spaces("1 \n2  \n3\n", "1\n2\n3\n"))

    def test_validate_erasing_trailing_spaces2(self):
        self.assertTrue(self.stringValidator.validate_with_erasing_trailing_spaces("1 \n2  \n3\n", "1\n2\n3\n\n"))
