import unittest
import random
from validator import StringValidator


class StringValidatorClassTest(unittest.TestCase):
    def setUp(self):
        self.stringValidator = StringValidator()

    def test_validate_correct1(self):
        result = self.stringValidator.validate("abcdef", "abcdefg")
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
