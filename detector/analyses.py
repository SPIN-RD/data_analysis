from .lib.analysis import analysis
from .lib.utils import transform_pyplot_figure_to_base64_png_uri
import numpy as np
import matplotlib.pyplot as plt


# Step 1: Create an Analysis class
class SimplePlotAnalysis:
    def analyze(self, data):
        x = np.linspace(0, 10, 100)
        y = x**2
        plt.plot(x, y)
        base64_image = transform_pyplot_figure_to_base64_png_uri(plt)

        return {
            'image:Random plot': base64_image,
            'Raw data': data,
            'Half-life': '32 days'
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
