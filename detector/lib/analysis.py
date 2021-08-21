class AnalysisWrapper:
    def __init__(self, name, mode, cls):
        self.name = name
        self.mode = mode
        self.cls = cls


def analysis(name, mode, cls):
    return AnalysisWrapper(name, mode, cls)
