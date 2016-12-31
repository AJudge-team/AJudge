import unittest
from os import path
from dto import *
from consts import *


class TestJudgeContext(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    """
        @description: Test for correct source code
    """
    def test_set_source_code(self):
        dir = path.join(path.dirname(__file__), "../samples/01/solution.cc")
        file = open(dir, "r")

        source_code = ''.join(file.readlines())

        judge_context = JudgeContext()
        judge_context.source_code = source_code

        self.assertIs(source_code, judge_context.source_code)

        file.close()

    """
        @description: Test for correct problem id
    """
    def test_set_problem_id(self):
        problem_id = "123456"

        judge_context = JudgeContext()
        judge_context.problem_id = problem_id

        self.assertIs(problem_id, judge_context.problem_id)

    """
        @description: Test for correct programming language
    """
    def test_set_programming_language(self):
        programming_language = ProgrammingLanguage.CPP

        judge_context = JudgeContext()
        judge_context.programming_language = programming_language

        self.assertIs(programming_language, judge_context.programming_language)

    """
        @description: Test for incorrect source code
    """
    def test_set_incorrect_source_code(self):
        source_code = 123456789

        judge_context = JudgeContext()

        with self.assertRaises(TypeError):
            judge_context.source_code = source_code

    """
        @description: Test for incorrect problem id
    """
    def test_set_incorrect_problem_id(self):
        problem_id = 123456

        judge_context = JudgeContext()

        with self.assertRaises(TypeError):
            judge_context.problem_id = problem_id

    """
        @description: Test for incorrect programming language
    """
    def test_set_incorrect_programming_language(self):
        programming_language = 'cpp'

        judge_context = JudgeContext()

        with self.assertRaises(TypeError):
            judge_context.programming_language = programming_language

