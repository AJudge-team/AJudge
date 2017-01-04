from .runner import Runner
from sandbox import Sandbox
from dto import RuntimeContext

class CppRunner(Runner):
    def prepare(self, runtime_context: RuntimeContext) -> Sandbox:
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
        user_outputs = {}
        run_info = {}
        cmd_holder = "/workdir/judge_client {0} {1} ".format(runtime_context.problem_metadata.memory_limit,\
                                                             runtime_context.problem_metadata.time_limit)
        cmd_holder = cmd_holder + "/workdir/{0} " + \
                     "/workdir/outputs/{1}.out " + \
                     "/workdir/{1}.err /workdir/solution"

        for input_name, input in runtime_context.problem_metadata.inputs.items():
            basename = input_name.split('.')[0]
            cmd = cmd_holder.format(input_name, basename)
            run_info[basename+".out"] = sandbox.exec(cmd).get('Output')

        outputs = sandbox.get_files_from_sandbox("/workdir/outputs/")
        for name, output in outputs:
            user_outputs[name] = str(output, 'UTF-8')

        return {'RunInfo': run_info, 'UserOutput': user_outputs}

