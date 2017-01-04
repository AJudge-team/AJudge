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
        inputfiles = [("solution.cc",str.encode(runtime_context.source_code))]
        idx = 0
        for input in runtime_context.problem_metadata.inputs:
            inputfiles.append(("input{0}.in".format(idx),str.encode(input)))
            idx+=1
            print("copy")

        res = sandbox.write_files_in_sandbox(inputfiles,"/workdir")
        if res is False:
            raise Exception
        else:
            print("write")

        res = sandbox.exec("mkdir /workdir/outputs")
        if res.get('ExitCode') is not 0:
            raise Exception
        else :
            print ("mkdir")

        res = sandbox.exec("g++ -std=c++11 -O2 -Wall /workdir/solution.cc -o /workdir/solution")
        if res.get('ExitCode') is not 0:
            raise Exception
        else:
            print ("compile")

        return sandbox

    def run(self, runtime_context: RuntimeContext, sandbox: Sandbox):
        print("[Mock cpp runner] run")
        user_outputs = []
        results = []
        cmd = "/workdir/judge_client 512 5 /workdir/input{0}.in /workdir/outputs/output{1}.in /workdir/error{2}.log /workdir/solution"

        for idx in range(0, len(runtime_context.problem_metadata.inputs)):
            results.append(sandbox.exec(cmd.format(idx,idx,idx)))

        outputs = sandbox.get_files_from_sandbox("/workdir/outputs/")
        for n, output in outputs:
            user_outputs.append(output.encode('utf8'))

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
        base_controller.handle(judge_context)
    except Exception as e:
        print(e)


start.add_param("-s", "--source", help="source code location", default=None, type=str)
start.add_param("-l", "--language", help="programming language", default=None, type=str)
start.add_param("-p", "--problem", help="problem id", default=None, type=str)

if __name__ == "__main__":
    start.run()
