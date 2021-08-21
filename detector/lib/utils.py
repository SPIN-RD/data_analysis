import io
import base64


def transform_pyplot_figure_to_base64_png_uri(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
