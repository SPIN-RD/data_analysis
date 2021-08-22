import matplotlib.pyplot as plt
import numpy as np
import zfit
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from plotly.graph_objs import Histogram, Scatter
from plotly.offline import plot
from rest_framework import generics, status, views
from rest_framework.response import Response
from tensorflow.python.platform.tf_logging import error

from .models import Measurement
from .serializers import MeasurementSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = MeasurementSerializer


class MeasurementRetrieveView(generics.RetrieveAPIView):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()

    def get(self, request, device_id, mode):
        qs = (
            Measurement.objects.filter(device_id=device_id, mode=mode)
            .order_by("-created_at")
            .first()
        )
        if not qs:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        measurement_data = MeasurementSerializer(qs).data["measurement_data"]

        if request.GET.get("download"):
            response = JsonResponse(measurement_data, safe=False)
            response["Content-Disposition"] = "attachment; filename=data.json"
            return response

        return Response(measurement_data)


def index(request):
    context = {}
    return render(request, "detector/index.html", context)


def energy_spectrum_analysis(request, device_id):
    np.random.seed(42)
    hist_data = np.random.normal(loc=0, scale=1, size=10000)
    n_bins = 100
    x, y, fit_params = fitting_energy_spectrum(hist_data, n_bins=n_bins)
    plot_div = plot(
        [
            Histogram(
                x=hist_data,
                xbins=dict(
                    start=np.min(hist_data),
                    end=np.max(hist_data),
                    size=np.abs((max(hist_data) - min(hist_data))) / n_bins,
                ),
                autobinx=False,
                name="Data",
                opacity=0.4,
                marker=dict(color="blue"),
            ),
            Scatter(
                x=x,
                y=y,
                mode="lines",
                name="Fit",
                opacity=0.8,
                marker_color="red",
            ),
        ],
        output_type="div",
    )

    latest_measurement = (
        Measurement.objects.filter(device_id=device_id, mode="Count")
        .order_by("-created_at")
        .first()
    )

    if not latest_measurement:
        raise Http404()

    json_data = latest_measurement.measurement_data

    context = {
        "device_id": device_id,
        "json_data": json_data,
        "plot_div": plot_div,
        "title": "Plot",
        "fit_params": fit_params,
    }

    return render(request, "detector/half_life_analysis.html", context)


N_runs = 0


def fitting_energy_spectrum(np_data, n_bins):
    global N_runs
    obs = zfit.Space("x", limits=(np.min(np_data), np.max(np_data)))
    data = zfit.Data.from_numpy(obs=obs, array=np_data)

    # create the model
    mu = zfit.Parameter(f"mu_{N_runs}", 0, np.min(np_data), np.max(np_data))
    sigma = zfit.Parameter(f"sigma_{N_runs}", 1, 0, 10)
    N_runs += 1
    gauss = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sigma)

    # build the loss
    nll = zfit.loss.UnbinnedNLL(model=gauss, data=data)

    # minimize
    minimizer = zfit.minimize.Minuit()
    result = minimizer.minimize(nll)

    # plot fitted model afterwards
    x = np.linspace(np.min(np_data), np.max(np_data), 1000)
    scale = len(np_data) / n_bins * obs.area()

    y = gauss.pdf(x).numpy() * scale
    errors = result.hesse()
    fit_params = {
        "mu": result.params[mu]["value"],
        "mu_err": errors[mu]["error"],
        "sigma": result.params[sigma]["value"],
        "sigma_err": errors[mu]["error"],
    }
    return x, y, fit_params


def half_life_analysis(request, device_id):
    latest_measurement = (
        Measurement.objects.filter(device_id=device_id, mode="Count")
        .order_by("-created_at")
        .first()
    )

    if not latest_measurement:
        raise Http404()

    json_data = latest_measurement.measurement_data

    counts = json_data['counts']
    bin_time = json_data['binTime']

    # np.random.seed(42)
    # np.random.exponential(scale=5, size=10000)
    hist_data = np.asarray(counts)
    n_bins = int(bin_time)
    x, y, fit_params = fitting_halflife(hist_data, n_bins=n_bins)
    plot_div = plot(
        [
            Histogram(
                x=hist_data,
                xbins=dict(
                    start=np.min(hist_data),
                    end=np.max(hist_data),
                    size=np.abs((max(hist_data) - min(hist_data))) / n_bins,
                ),
                autobinx=False,
                name="Data",
                opacity=0.4,
                marker=dict(color="blue"),
            ),
            Scatter(
                x=x,
                y=y,
                mode="lines",
                name="Fit",
                opacity=0.8,
                marker_color="red",
            ),
        ],
        output_type="div",
    )

    context = {
        "device_id": device_id,
        "json_data": json_data,
        "plot_div": plot_div,
        "title": "Plot",
        "fit_params": fit_params,
    }

    return render(request, "detector/half_life_analysis.html", context)


def fitting_halflife(np_data, n_bins):
    global N_runs
    obs = zfit.Space("x", limits=(np.min(np_data), np.max(np_data)))
    data = zfit.Data.from_numpy(obs=obs, array=np_data)

    # create the model
    lam = zfit.Parameter(f"lam_{N_runs}", -1, -10, 0)
    N_runs += 1
    expo = zfit.pdf.Exponential(obs=obs, lam=lam)

    # build the loss
    nll = zfit.loss.UnbinnedNLL(model=expo, data=data)

    # minimize
    minimizer = zfit.minimize.Minuit()
    result = minimizer.minimize(nll)

    # plot fitted model afterwards
    x = np.linspace(np.min(np_data), np.max(np_data), 1000)
    scale = len(np_data) / n_bins * obs.area()

    y = expo.pdf(x).numpy() * scale
    errors = result.hesse()
    fit_params = {
        "lam": result.params[lam]["value"],
        "lam_err": errors[lam]["error"],
    }
    return x, y, fit_params
