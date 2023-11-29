""" Module for handling all things to do with the filters
"""
import logging

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
from django.db.utils import OperationalError
import pandas as pd

from ..data.query_postgres import query
from ..models import Feature, Config

logger = logging.getLogger(__name__)


def create_filters_layout(app):
    """Function to handle filter layout creation easily"""
    cat_filter_list = []
    cont_filter_list = []

    try:
        cat_filters = list(
            Feature.objects.filter(filter=True).filter(type="categorical")
        )
        if not cat_filters:
            logger.warning(
                "WARNING: No Categorical Filters exist, dashboard will misbehave!!"
            )
    except OperationalError:
        logger.error("'Filter' table does not exist...")
        cat_filters = []
    for cat_filter in cat_filters:
        cat_filter_list.append(
            dbc.Col(
                width=2,
                className="align-self-center btn",
                children=[
                    dbc.Form(
                        dbc.FormGroup(
                            [
                                dbc.Label(f"{cat_filter.name}:"),
                                CategoricalFilter(app, cat_filter.name),
                            ]
                        )
                    )
                ],
            ),
        )
    div_children = cat_filter_list + cont_filter_list
    return div_children


class CategoricalFilter:
    """Generic class to handle custom Categorical Filters"""

    def __new__(cls, app, filt):
        """Function to initialise categorical filter component

        Args:
            app (dash app object): dash application object for defining callbacks

        Returns:
            category_dropdown (dcc.Dropdown): dropdown component for the category
        """

        @app.callback(
            [Output(f"{filt}-filter", "options")],
            [
                Input("url", "children"),
                Input("medical-data-store", "data"),
                Input(f"{filt}-filter", "value"),
            ],
        )
        def load_categorical_filter(url_endpoint, *_):

            try:
                data_store_query = (
                    Config.objects.filter(url_endpoint=url_endpoint)
                    .first()
                    .data_store_query
                )
                df_filter = query(data_store_query, url_endpoint)
            except (AttributeError, OperationalError):
                logger.error("No config set, data store is empty...")
                df_filter = pd.DataFrame()

            options_list = []
            for name in list(df_filter[filt].unique()):
                options_list.append(
                    {
                        "label": name,
                        "value": name,
                    }
                )

            return [options_list]

        return dcc.Dropdown(
            id=f"{filt}-filter",
            searchable=False,
            clearable=True,
            multi=True,
            style={"width": "200px"},
        )
