from dto import ProblemMetadata


class ProblemProvider:
    def __init__(self):
        pass

    def get_problem_metadata_by_id(self, problem_id: str) -> ProblemMetadata:

        problem_metadata = ProblemMetadata()

        problem_metadata.problem_id = problem_id

        return problem_metadata
