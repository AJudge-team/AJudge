from dto import ProblemMetadata
from os import path
import os
import glob
import json


class ProblemProvider:
    def __init__(self):
        pass

    def get_problem_metadata_by_id(self, problem_id: str) -> ProblemMetadata:

        problem_metadata = ProblemMetadata()

        problem_metadata.problem_id = problem_id

        dir_path = path.join(path.dirname(__file__), "../samples/"+problem_id)

        inputs = {}
        outputs = {}

        for file in glob.iglob(dir_path+"/*.in"):
            basename = path.basename(file)
            file_name = basename
            basename = basename.split('.')[0]
            idx = int(basename.split('d')[1])

            inputs[file_name] = "".join(open(file, "r").readlines())

        for file in glob.iglob(dir_path+"/*.out"):
            basename = path.basename(file)
            file_name = basename
            basename = basename.split('.')[0]
            idx = int(basename.split('d')[1])

            outputs[file_name] = "".join(open(file, "r").readlines())

        problem_metadata.inputs = inputs
        problem_metadata.outputs = outputs

        with open(os.path.join(dir_path,"problem_info.json")) as f:
            problem_limits = json.load(f)

        problem_metadata.time_limit = problem_limits["TimeLimit"]
        problem_metadata.memory_limit = problem_limits["MemoryLimit"]
        return problem_metadata
