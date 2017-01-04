#!/usr/bin/env python

from controller import *
from provider import ProblemProvider
from validator import StringValidator
import cli.app
from dto import *
from os import path
from consts import *
from runner import Runner
from sandbox import Sandbox


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


class MockCppRunner(Runner):
    def prepare(self, runtime_context: RuntimeContext) -> Sandbox:
        print("[Mock cpp runner] '{0}' is prepared.".format(
            runtime_context.programming_language.name
        ))

        sandbox = Sandbox(54321)
        input_files = [("solution.cc", str.encode(runtime_context.source_code))]
        for input_name, input_content in runtime_context.problem_metadata.inputs.items():
            input_files.append((input_name, str.encode(input_content)))

        res = sandbox.write_files_in_sandbox(input_files, "/workdir")
        if res is False:
            raise Exception

        res = sandbox.exec("mkdir /workdir/outputs")
        if res.get('ExitCode') is not 0:
            raise Exception

        res = sandbox.exec("g++ -std=c++11 -O2 -Wall /workdir/solution.cc -o /workdir/solution")
        if res.get('ExitCode') is not 0:
            print('compile error')
            raise Exception

        return sandbox

    def run(self, runtime_context: RuntimeContext, sandbox: Sandbox):
        print("[Mock cpp runner] run")
        user_outputs = {}
        results = []
        cmd_holder = "/workdir/judge_client 512 5 /workdir/{0}" + \
                     " /workdir/outputs/{1}.out" + \
                     " /workdir/{1}.err /workdir/solution"

        for input_name, input in runtime_context.problem_metadata.inputs.items():
            basename = input_name.split('.')[0]
            cmd = cmd_holder.format(input_name, basename)
            results.append(sandbox.exec(cmd))

        outputs = sandbox.get_files_from_sandbox("/workdir/outputs/")
        for name, output in outputs:
            user_outputs[name] = str(output, 'UTF-8')

        return user_outputs


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
        judge_result = base_controller.handle(judge_context)
        print(judge_result.is_accepted)
        print(judge_result.message)
    except Exception as e:
        print(e)


start.add_param("-s", "--source", help="source code location", default=None, type=str)
start.add_param("-l", "--language", help="programming language", default=None, type=str)
start.add_param("-p", "--problem", help="problem id", default=None, type=str)

if __name__ == "__main__":
    start.run()
