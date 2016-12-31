#!/usr/bin/env python

from controller import *
from provider import ProblemProvider
from validator import StringValidator
import cli.app
from dto import *
from os import path
from consts import *
from runner import Runner
from sandbox import SandboxMixin


def fill_judge_context(judge_context, params):
    judge_context.problem_id = params.problem
    judge_context.programming_language = params.language

    file_path = None

    if path.isabs(params.source):
        file_path = params.source
    else:
        file_path = path.join(path.dirname(__file__), params.source)

    file = open(file_path, "r")
    content = "".join(file.readlines())

    judge_context.source_code = content
    file.close()


class MockSandbox(SandboxMixin):
    def exec(self, cmd: str):
        print("[Mock sandbox] cmd '{0}'".format(cmd))


class MockCppRunner(Runner):
    def prepare(self, runtime_context: RuntimeContext) -> SandboxMixin:
        print("[Mock cpp runner] '{0}' is prepared.".format(
            runtime_context.programming_language.name
        ))

        mock_sandbox = MockSandbox()

        return mock_sandbox

    def run(self, runtime_context: RuntimeContext, sandbox: SandboxMixin):
        print("[Mock cpp runner] '{0}' is run.".format(
            runtime_context.programming_language.name
        ))

        sandbox.exec("{0} {1}".format(
            runtime_context.programming_language.name,
            runtime_context.problem_metadata.problem_id
        ))

        problem_provider = ProblemProvider()

        return problem_provider.get_problem_metadata_by_id(
            runtime_context.problem_metadata.problem_id
        ).outputs


@cli.app.CommandLineApp
def start(app):
    if app.params.source is None:
        print("Source code should exist.")
        return

    if app.params.language is None:
        print("Language should exist.")
        return

    if app.params.problem is None:
        print("Problem id should exist")
        return

    base_controller = BaseController()
    problem_provider = ProblemProvider()
    validator = StringValidator()

    base_controller\
        .set_problem_provider(problem_provider)\
        .set_validator(validator)\
        .add_runner(
            ProgrammingLanguage.CPP,
            MockCppRunner()
        )

    judge_context = JudgeContext()

    try:
        fill_judge_context(judge_context, app.params)
    except FileNotFoundError:
        print("No such source file.")
        return

    try:
        base_controller.handle(judge_context)
    except Exception as e:
        print(e)


start.add_param("-s", "--source", help="source code location", default=None, type=str)
start.add_param("-l", "--language", help="programming language", default=None, type=str)
start.add_param("-p", "--problem", help="problem id", default=None, type=str)

if __name__ == "__main__":
    start.run()
