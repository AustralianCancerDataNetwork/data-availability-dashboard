from django.http import Http404

from .views import custom_404_view


class Custom404Middleware:
    """
    Class for the "Page not found" middleware for the DataAvailability dashboard
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Http404:
            return custom_404_view(request)
        return response
