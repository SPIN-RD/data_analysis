from .lib.analysis import analysis


# Step 1: Create an Analysis class
class SimplePlotAnalysis:
    def analyze(self, data):
        return {
            'plot': 'base64encoded',
            'data': data
        }


# Step 2: Register the Analysis class here
analyses = [
    analysis(name="simple_plot", mode="Linear", cls=SimplePlotAnalysis),
]


def find_analysis(name):
    for analysis_wrapper in analyses:
        if analysis_wrapper.name == name:
            analysis_cls = analysis_wrapper.cls
            mode = analysis_wrapper.mode
            return analysis_cls, mode

    return None
