""" Module for handling the in-depth table at the bottom of the dashboard
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


class PatientDataTable:
    """_summary_"""

    def __new__(cls, app):
        """_summary_

        Args:
            app (_type_): _description_

        Returns:
            _type_: _description_
        """

        @app.callback(
            [
                dash.dependencies.Output("datatable-div", "children"),
            ],
            [
                dash.dependencies.Input("medical-data-store", "data"),
            ],
        )
        def get_clinic_datatable(medical_data_store):
            # pylint: disable=E1101
            df_patients = pd.DataFrame(medical_data_store)
            return [
                dbc.Table.from_dataframe(
                    df_patients,
                    striped=True,
                    bordered=True,
                    hover=True,
                    index=True,
                    className="table-responsive",
                    style={
                        "max-height": "500px",
                        "width": "80%",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                )
            ]

        return dcc.Loading(
            id="loading_table", type="circle", children=[html.Div(id="datatable-div")]
        )
