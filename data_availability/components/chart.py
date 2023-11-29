import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


class TNMBarchart:
    """A bar chart for a TNM features"""

    def __new__(cls, app):
        """Function to initialise TNM bar chart

        Args:
            app (dash app object): dash application object for defining callbacks

        Returns:
            loading_comp (dcc.Loading): loading component for the TNM bar chart figure
        """

        @app.callback(
            [
                dash.dependencies.Output("tnm-barchart-div", "children"),
            ],
            [
                dash.dependencies.Input("medical-data-store", "data"),
            ],
        )
        def get_tnm_barchart(medical_data_store):
            df_patients = pd.DataFrame(medical_data_store).filter(
                items=["t_stage", "n_stage", "m_stage"]
            )
            # df_final = pd.DataFrame([], columns=["Stage", "Type", "Freq"])
            df_final = pd.DataFrame([])

            for col in df_patients.columns:

                df_grouped = df_patients.groupby(col).size()
                df_temp = pd.DataFrame(df_grouped).reset_index()
                df_final = pd.concat([df_final, df_temp])
                # df_final.columns = ["Feature", "Frequency"]

                # df_temp = df_patients.groupby(col).size()
                # for i, index in enumerate(list(df_temp.index)):
                #     df_final = df_final.append(
                #         {
                #             "Stage": col,
                #             "Type": index,
                #             "Freq": df_temp[i],
                #         },
                #         ignore_index=True,
                #     )

            fig = px.bar(df_final, x="Stage", y="Freq", color="Type", barmode="group")
            return [dcc.Graph(figure=fig)]

        return dcc.Loading(
            id="loading-barchart",
            type="circle",
            children=[html.H3("TNM distribution"), html.Div(id="tnm-barchart-div")],
            style={
                "width": "100px",
            },
        )


class FeaturePiechart:
    """A pie chart for a boolean/multi valued feature"""

    def __new__(cls, app, feature):
        """Function to initialise feature pie chart

        Args:
            app (dash app object): dash application object for defining callbacks
            feature (str): feature name

        Returns:
            loading_comp (dcc.Loading): loading component for the feature pie chart figure
        """

        @app.callback(
            [
                dash.dependencies.Output(f"{feature}-piechart-div", "children"),
            ],
            [
                dash.dependencies.Input("medical-data-store", "data"),
            ],
        )
        def get_feature_piechart(medical_table_store):
            df_patients = pd.DataFrame(medical_table_store).filter(items=[feature])

            df_temp = df_patients.groupby(feature).size()
            df_final = pd.DataFrame(df_temp).reset_index()
            df_final.columns = ["Feature", "Frequency"]

            fig = px.pie(df_final, values="Frequency", names="Feature")
            return [dcc.Graph(figure=fig)]

        return dcc.Loading(
            id="loading-piechart",
            type="circle",
            children=[
                html.H3(f"{feature} distribution"),
                html.Div(id=f"{feature}-piechart-div"),
            ],
            style={
                "width": "100px",
            },
        )


class FeatureHistogram:
    """A histogram for a boolean/multi valued feature"""

    def __new__(cls, app, feature):
        """Function to initialise feature histogram

        Args:
            app (dash app object): dash application object for defining callbacks
            feature (str): feature name

        Returns:
            loading_comp (dcc.Loading): loading component for the feature histogram figure
        """

        @app.callback(
            [
                dash.dependencies.Output(f"{feature}-histogram-div", "children"),
            ],
            [
                dash.dependencies.Input("medical-data-store", "data"),
            ],
        )
        def get_feature_histogram(medical_table_store):
            df_patients = pd.DataFrame(medical_table_store)
            fig = px.histogram(df_patients, x=feature)
            return [dcc.Graph(figure=fig)]

        return dcc.Loading(
            id="loading-histogram",
            type="circle",
            children=[
                html.H3(f"{feature} distribution"),
                html.Div(id=f"{feature}-histogram-div"),
            ],
            style={
                "width": "100px",
            },
        )
