"""Module for handling different data components
"""
import logging

import dash_core_components as dcc
from dash.dependencies import Input, Output
from django.db.utils import OperationalError
import pandas as pd

from ..data.query_postgres import query
from ..models import Config, Feature

logger = logging.getLogger(__name__)


class MedicalStore:
    """Store to hold medical table data"""

    def __new__(cls, app):
        """Function to medical store when category dropdown changes

        Args:
            app (dash app object): dash application object for defining callbacks

        Returns:
            medical_table (dcc.Store): dcc store component for storing medical table data
        """

        try:
            filters = list(Feature.objects.filter(filter=True))
            if not filters:
                logger.warning("WARNING: No Filters exist, dashboard will misbehave!!")
        except OperationalError:
            logger.error("'Filter' table does not exist...")
            filters = []

        @app.callback(
            [Output("medical-data-store", "data")],
            [Input("url", "children")]
            + [Input(f"{filt.name}-filter", "value") for filt in filters],
        )
        def update_medical_store(url_endpoint, *filter_values):
            try:
                data_store_query = (
                    Config.objects.filter(url_endpoint=url_endpoint)
                    .first()
                    .data_store_query
                )
                df_medical = query(data_store_query, url_endpoint)
            except AttributeError:
                logger.error("No config set, data store is empty...")
                df_medical = pd.DataFrame()
            for filt_val_list, filt in zip(filter_values, filters):
                if filt_val_list is not None:
                    if len(filt_val_list) > 0:
                        df_medical = df_medical[
                            df_medical[filt.name].isin(filt_val_list)
                        ]
            return [df_medical.to_dict()]

        return dcc.Store(id="medical-data-store")
