"""
Models to be used in the dashboard
"""
from django.db import models

from data_availability.components.constants import FEATURE_TYPES


class Dashboard(models.Model):
    """Model to handle permission to the dashboard"""

    class Meta:
        permissions = (
            ("access_data_availability_dash", "### Access Head and Neck Dashboard ###"),
            (
                "admin_access_data_availability_dash",
                "### Admin Access Head and Neck Dashboard ###",
            ),
        )


class Centre(models.Model):
    """Class for managing Centre information

    Args:
        name (str): centre name
        description (str): centre description

    """

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):
    """Class for managing Patient information

    Args:
        centre_name (Centre.Id): centre name
        patient_id (str): patient id
        name (str): patient's name
        age (int): patient's age
        sex (str): patient's sex
        primary_site (str): patient's primary site
        t_stage (str): patient's T stage
        m_stage (str): patient's M stage
        n_stage (str): patient's N stage
        hpv_status (boolean): patient's HVP status

    """

    centre_name = models.ForeignKey(Centre, null=True, on_delete=models.SET_NULL)

    patient_id = models.CharField(
        max_length=15,
        help_text="Patient ID",
        blank=False,
        null=False,
    )

    age = models.IntegerField(
        help_text="Age",
        blank=True,
        null=True,
    )

    sex = models.CharField(
        max_length=16,
        help_text="Patient's sex",
        blank=False,
        null=False,
    )

    primary_site = models.CharField(
        max_length=32,
        help_text="Patient's cancer primary site ",
        blank=False,
        null=False,
    )

    t_stage = models.CharField(
        max_length=32,
        help_text="Patient's T-stage",
        blank=True,
        null=True,
    )

    n_stage = models.CharField(
        max_length=32,
        help_text="Patient's N-stage",
        blank=True,
        null=True,
    )

    m_stage = models.CharField(
        max_length=32,
        help_text="Patient's M-stage",
        blank=True,
        null=True,
    )

    hpv_status = models.BooleanField(
        help_text="Patient's HPV status",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.patient_id}"


class Config(models.Model):
    """Head and Neck Cancer Data Dashboard Configuration

    Args:
        centres ([Centre.Id]): list of centres defined for the Head and Neck dashboard

    """

    url_endpoint = models.CharField(
        max_length=16, help_text="Dashboard URL endpoint", null=True, blank=True
    )

    data_store_query = models.CharField(
        max_length=256, help_text="Feature query", null=True, blank=True
    )

    dashboard_title = models.CharField(
        max_length=64, help_text="Dashboard title", null=True, blank=True
    )

    db_name = models.CharField(
        max_length=64, help_text="Database name", null=True, blank=True
    )

    db_username = models.CharField(
        max_length=64, help_text="Database username", null=True, blank=True
    )

    db_password = models.CharField(
        max_length=64, help_text="Database password", null=True, blank=True
    )

    db_servername = models.CharField(
        max_length=64, help_text="Database server name", null=True, blank=True
    )

    db_port = models.CharField(
        max_length=64, help_text="Database port", null=True, blank=True
    )

    def __str__(self):
        return self.dashboard_title


class Feature(models.Model):
    """Class for tracking different clinical features to be displayed on the dashboard

    Args:
        name (str): feature name
        type (str): type of feature, either continuous or categorical
        filter (bool): boolean to check if this feature will be used as a filter
    """

    name = models.CharField(
        max_length=15,
        help_text="Feature name",
        blank=False,
        null=False,
    )

    type = models.CharField(
        max_length=12,
        help_text="Feature type",
        choices=FEATURE_TYPES,
        blank=False,
        null=False,
    )

    filter = models.BooleanField(
        help_text="Feature filter",
        blank=False,
        null=False,
    )

    config = models.ForeignKey(Config, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, **kwargs):
        """Function to create a new Feature instance

        Returns:
            _type_: _description_
        """
        feature = cls.objects.get_or_create(
            name=kwargs["fields"]["name"],
            type=kwargs["fields"]["type"],
            filter=kwargs["fields"]["filter"],
        )
        return feature
