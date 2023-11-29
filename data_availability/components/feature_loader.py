""" Module specific to the dashboard features
"""
import logging

import dash_bootstrap_components as dbc
import dash_html_components as html
from django.db.utils import OperationalError

from .chart import FeaturePiechart, FeatureHistogram
from ..models import Feature

logger = logging.getLogger(__name__)


def create_features_layout(app):
    """Function to handle feature layout creation easily

    Args:
        app (DjangoDash): app instance

    Returns:
        html.Div: HTML div that contains the features
    """
    feat_children = []
    try:
        features = list(Feature.objects.filter(filter=False))
        if not features:
            logger.warning("WARNING: No graph features exist, dashboard will misbehave!!")
    except OperationalError:
        logger.error("No 'Filter' table exists...")
        features = []

    for feat in features:
        if feat.type == "continuous":
            feat_children.append(FeatureHistogram(app, feat.name))
        else:
            feat_children.append(FeaturePiechart(app, feat.name))

    div = []
    counter = 0
    while counter < len(feat_children):
        if (counter + 1) < len(feat_children):
            div.append(
                dbc.Row(
                    [
                        dbc.Col(
                            width=6,
                            children=[
                                feat_children[counter],
                            ],
                        ),
                        dbc.Col(
                            width=6,
                            children=[
                                feat_children[counter + 1],
                            ],
                        ),
                    ]
                ),
            )
        else:
            div.append(
                dbc.Row(
                    [
                        dbc.Col(
                            width=6,
                            children=[
                                feat_children[counter],
                            ],
                        ),
                    ]
                ),
            )
        counter += 2
    return div


class FeatureLoader:
    """Class to load custom features added via admin panel"""

    def __new__(cls, app):
        """Function to initialise feature loader

        Args:
            app (dash app object): dash application object for defining callbacks

        Returns:
            loading_comp (dcc.Loading): loading component for the feature histogram figure
        """

        # @app.callback(
        #     [
        #         Output("feature-loader-div", "children"),
        #     ],
        #     [
        #         Input("placeholder", "children"),
        #     ],
        # )
        # def get_feature_histogram(_):
        #     return create_features_layout(app)

        # NOTE: whenever we add a new feature via admin panel, we need to reset the server. This is
        # to do with how dash loads the "app.layout", need to find better way

        return html.Div(
            id="feature-loader-div",
            children=create_features_layout(app),
        )
