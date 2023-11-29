""" Module for handling the information box at the top of the dashboard
"""
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html

from ..models import Config, Feature


class InfoBox:
    """Generic class to hold helpful information and guide the user on what's being shown on the
    dashboard"""

    def __new__(cls, app):
        """Function to initialise InfoBox component

        Args:
            app (dash app object): dash application object for defining callbacks

        Returns:
            list (dcc components): list of dcc components for the infobox
        """

        @app.callback(
            [
                Output("query-infobox", "children"),
                Output("features-infobox", "children"),
            ],
            Input("url", "children"),
            Input("medical-data-store", "data"),
        )
        def populate_infoboxes(url, _):
            config = Config.objects.filter(url_endpoint=url).first()
            query = html.B(config.data_store_query)
            feats = list(Feature.objects.all())
            features = []
            for feat in feats:
                features.append(html.B(feat.name))
                features.append(html.Br())
            return [query, features]

        @app.callback(
            Output("infobox-collapse", "is_open"),
            [Input("infobox-btn", "n_clicks")],
            [State("infobox-collapse", "is_open")],
        )
        def toggle_collapse(n, is_open):  # pylint: disable=invalid-name
            if n:
                return not is_open
            return is_open

        return [
            dbc.Button(
                "Open Summary",
                id="infobox-btn",
                className="mb-3",
                color="secondary",
            ),
            dbc.Collapse(
                [
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.CardBody(
                                                "The following query is used to grab the data:"
                                            ),
                                            dbc.CardBody(
                                                id="query-infobox",
                                                style={
                                                    "text-align": "Left",
                                                    "font-family": "Tahoma",
                                                    "font-style": "normal",
                                                    "font-weight": "normal",
                                                    "font-size": 11,
                                                    "color": "#000000",
                                                },
                                            ),
                                        ],
                                        width=5,
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            html.Hr(), style={"padding-top": "50%"}
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.CardBody(
                                                "The following features are being visualised:"
                                            ),
                                            dbc.CardBody(id="features-infobox"),
                                        ],
                                        width=5,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                id="infobox-collapse",
                is_open=False,
            ),
        ]
