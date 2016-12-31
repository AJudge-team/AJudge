from . controller_mixin import ControllerMixin
from dto import JudgeContext, RuntimeContext, JudgeResult
from runner import Runner
from consts import ProgrammingLanguage
from provider import ProblemProvider
from typing import Dict
from validator import ValidatorMixin


# class implementation for controller interface
class BaseController(ControllerMixin):
    def __init__(self,
                 problem_provider: ProblemProvider=None,
                 runners: Dict[ProgrammingLanguage, Runner]={},
                 validator: ValidatorMixin=None):

        self.__problem_provider = problem_provider
        self.__runners = runners
        self.__validator = validator

    def set_validator(self, validator: ValidatorMixin) -> 'ControllerMixin':
        self.__validator = validator

        return self

    def set_problem_provider(self, problem_provider: ProblemProvider) -> 'ControllerMixin':
        self.__problem_provider = problem_provider

        return self

    def add_runner(self, runner_name: ProgrammingLanguage, runner: Runner) -> 'ControllerMixin':
        if runner_name in self.__runners:
            raise ValueError("Existing runner name '{0}'".format(runner_name))

        self.__runners[runner_name] = runner

        return self

    def analyze(self, judge_context: JudgeContext) -> RuntimeContext:
        runtime_context = RuntimeContext()

        runtime_context.programming_language = \
            ProgrammingLanguage.get_proper_programming_language(
                judge_context.programming_language
            )

        runtime_context.problem_metadata = \
            self.__problem_provider.get_problem_metadata_by_id(
                judge_context.problem_id
            )

        return runtime_context

    def choose_runner(self, runtime_context: RuntimeContext) -> Runner:
        runner = self.__runners[runtime_context.programming_language]

        return runner

    def handle(self, judge_context: JudgeContext) -> JudgeResult:
        runtime_context = self.analyze(judge_context)

        runner = self.choose_runner(runtime_context)

        sandbox = runner.prepare(runtime_context)

        judge_result = runner.run(runtime_context, sandbox)

        return judge_result
