import unittest
from dto import *
from os import path
from controller import BaseController
from consts import *
from provider import *
from runner import *
from sandbox import *


class MockCppRunner(Runner):
    def prepare(self, runtime_context: RuntimeContext) -> SandboxMixin:
        print("Prepare CPP")
        return MockSandbox()

    def run(self, runtime_context: RuntimeContext, sandbox: SandboxMixin):
        print("Run CPP")


class MockSandbox(SandboxMixin):
    def exec(self, cmd: str):
        print("Execute")


class TestBaseController(unittest.TestCase):
    def setUp(self):
        problem_provider = ProblemProvider()
        base_controller = BaseController(problem_provider=problem_provider)

        self.base_controller = base_controller

    def tearDown(self):
        del self.base_controller

    def get_source_code_by_id(self, file_id: str) -> str:
        file_path = path.join(path.dirname(__file__), "../samples/"+file_id+"/solution.cc")

        file = open(file_path, "r")

        content = "".join(file.readlines())

        file.close()

        return content

    def test_analyze_judge_context1(self):
        judge_context = JudgeContext()

        problem_id = "01"

        judge_context.problem_id = problem_id
        judge_context.programming_language = "CPP"
        judge_context.source_code = self.get_source_code_by_id(problem_id)

        runtime_context = self.base_controller.analyze(judge_context)

        self.assertEqual(
            runtime_context.programming_language,
            ProgrammingLanguage.CPP
        )

    def test_choose_runner1(self):
        cpp_runner = MockCppRunner()
        rc = RuntimeContext(programming_language=ProgrammingLanguage.CPP)

        self.base_controller.add_runner(
            ProgrammingLanguage.CPP,
            cpp_runner
        )

        chosen_runner = self.base_controller.choose_runner(rc)

        self.assertIs(cpp_runner, chosen_runner)
