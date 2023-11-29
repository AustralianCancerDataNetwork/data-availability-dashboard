from django.urls import re_path

from .views import dashboard_view

# Set the app name to refer to URLs in templates
app_name = "data_availability"
urlpatterns = [
    re_path(r"", dashboard_view, name="dashboard"),
]
