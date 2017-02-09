from . controller_mixin import ControllerMixin
from dto import JudgeContext, RuntimeContext, JudgeResult
from runner import Runner
from consts import ProgrammingLanguage
from provider import ProblemProvider
from typing import Dict
from validator import ValidatorMixin
import json
from exception import *


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

        runtime_context.source_code = judge_context.source_code
        return runtime_context

    def choose_runner(self, runtime_context: RuntimeContext) -> Runner:
        runner = self.__runners[runtime_context.programming_language]

        return runner

    def handle(self, judge_context: JudgeContext) -> JudgeResult:
        runtime_context = self.analyze(judge_context)
        runner = self.choose_runner(runtime_context)

        judge_result = JudgeResult()

        user_outputs = None

        try:
            sandbox = runner.prepare(runtime_context)
            run_info = runner.run(runtime_context, sandbox)
            user_outputs = run_info.get('UserOutput')
            run_info = run_info.get('RunInfo')

            for output_name,run_info_json in run_info.items():
                _run_info = json.loads(run_info_json.decode("utf-8"))
                if _run_info['OK'] is not True:
                    raise Exception('Judge Failed')
                if _run_info['Signaled'] is True:
                    raise Exception('Runtime Error : ' + str(_run_info['Signal']) +"("+_run_info['SignalStr']+")")

                if judge_result.peak_memory < _run_info['PeakMemory']:
                    judge_result.peak_memory = _run_info['PeakMemory']

                user_time = _run_info['UserTime'][0] + (_run_info['UserTime'][1]/(1e+6))
                sys_time = _run_info['SysTime'][0] + (_run_info['SysTime'][1]/(1e+6))
                if judge_result.used_time < (user_time + sys_time):
                    judge_result.used_time = (user_time + sys_time)


            if len(user_outputs) is not len(runtime_context.problem_metadata.outputs):
                raise Exception('Wrong answer')


            for output_name, output_content in user_outputs.items():
                result = self.__validator.validate(
                    output_content,
                    runtime_context.problem_metadata.outputs[output_name]
                )

                if result is False:
                    raise Exception("Wrong Answer at " + output_name)

            judge_result.is_accepted = True

        except Exception as e:
            judge_result.is_accepted = False
            judge_result.message = e

        return judge_result
