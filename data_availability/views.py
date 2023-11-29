from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render

from .app import app  # pylint: disable=unused-import
from .models import Config


def custom_404_view(request):
    """
    This function will return the 404 oage when an incorrect URL is passed to the dashboard

    Args:
        request (HttpResponse): the request that triggered this 404 error

    Returns:
        HttpResponse: Redircetion to the 404 error page
    """
    return render(request, "404.html", status=404)


@login_required
@permission_required("data_availability.access_data_availability_dash", raise_exception=True)
def dashboard_view(request, config_url):
    """
    Render the view for the Treatment Dashboard
    """
    context = {}
    conf = Config.objects.filter(url_endpoint=config_url).first()
    try:
        if conf:
            context["dashboard_config"] = {"url": {"children": conf.url_endpoint}}
        else:
            return custom_404_view(request)
    except Http404:
        return custom_404_view(request)
    return render(request, "data_availability/dashboard.html", context)
