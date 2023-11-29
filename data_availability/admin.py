# pylint: disable=<super-with-arguments>
import logging
import json

from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.core import serializers
from django.http import HttpResponseRedirect

from .models import Config, Feature

logger = logging.getLogger(__name__)


class ConfigAdminForm(forms.ModelForm):
    """
    Class to manage the Admin form for the "Config" model
    """

    class Meta:
        model = Config
        widgets = {
            "db_password": forms.PasswordInput(render_value=True),
        }

        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ConfigAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        config = super(ConfigAdminForm, self).save(commit=False)

        if commit:
            config.save()

        return config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    """
    Class to manage the Admin interface for the "Config" model
    """

    form = ConfigAdminForm

    actions = []

    fieldsets = ()


class FeatureForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_

    Returns:
        _type_: _description_
    """

    class Meta:
        """_summary_"""

        model = Feature
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """_summary_"""
        super(FeatureForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """summary"""
        config = super(FeatureForm, self).save(commit=False)

        if commit:
            config.save()

        return config


def export_features_to_json(request):
    """
    This function will export the Features currently on configured for a Dashboard instance to a
    JSON file in a file named `features.json`

    Limitation: this saves a file of the name to the location `/exports/features.json`

    Args:
        request (HttpRequest): The request that initiated this export step.

    Returns:
        HttpRequest: The request to redirect the user back to the same admin page where the request
        was initiated from
    """
    logger.info("Exporting features to JSON file...")
    objects = Feature.objects.all()
    with open(r"/exports/features.json", "w", encoding="utf-8") as out:
        mast_point = serializers.serialize("json", objects)
        out.write(mast_point)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def import_features_from_json(request):
    """
    This function will import Features from a JSON file.

    Limitation: this requires a file of the name to the location `/exports/features.json`

    Args:
        request (HttpRequest): The request that initiated this export step.

    Returns:
        HttpRequest: The request to redirect the user back to the same admin page where the request
        was initiated from
    """
    logger.info("Importing features from JSON file...")

    try:
        with open(r"/exports/features.json", "r", encoding="utf-8") as input_file:
            json_feats = json.load(input_file)
            for feat in json_feats:
                Feature.create(**feat)
    except FileNotFoundError:
        logger.error("JSON does not exist...")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """
    Class to handle the admin interface for the "Features" model.
    """

    form = FeatureForm

    actions = []

    list_display = ("name", "type", "filter", "config")

    def get_urls(self):
        urls = super(FeatureAdmin, self).get_urls()
        my_urls = [
            url(r"^export/$", export_features_to_json),
            url(r"^import/$", import_features_from_json),
        ]
        return my_urls + urls
