"""Head and Neck Data availability Dashboard
"""
import logging

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash

from .components.filter import create_filters_layout
from .components.table import PatientDataTable
from .components.data import MedicalStore
from .components.feature_loader import FeatureLoader
from .components.info_box import InfoBox

from .models import Config

logger = logging.getLogger(__name__)

app = DjangoDash("HeadNeck", serve_locally=True, add_bootstrap_links=True)


@app.callback(Output("title", "children"), Input("url", "children"))
def set_title(url_endpoint):
    """Callback to set the title of the dashboard based on the passed config

    Args:
        url_endpoint (Str): URL of the accessed dashboard

    Returns:
        Str: Dashboard title
    """
    conf = Config.objects.filter(url_endpoint=url_endpoint).first()
    return conf.dashboard_title


app.layout = html.Div(
    children=[
        MedicalStore(app),
        html.Div(id="url", style={"visibility": "hidden"}),
        html.Div(
            id="content",
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            width=3,
                            children=[
                                html.H3(
                                    children="Data availablility",
                                    style={"textAlign": "center", "margin-top": "20px"},
                                ),
                                html.H6(
                                    id="title",
                                    style={"textAlign": "center"},
                                ),
                            ],
                        )
                    ]
                    + create_filters_layout(app)
                ),
                dbc.Row(dbc.Col(html.Div(InfoBox(app)), width=10)),
                FeatureLoader(app),
                PatientDataTable(app),
            ],
        ),
    ]
)
