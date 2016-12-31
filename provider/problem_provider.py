from dto import ProblemMetadata


class ProblemProvider:
    def __init__(self):
        pass

    def get_problem_metadata_by_id(self, problem_id: str) -> ProblemMetadata:
        return ProblemMetadata()
