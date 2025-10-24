import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from src.db_data.crud_services import db_to_df_by_repuesto_and_tipo_repuesto
from src.db_data.models.services_model.distribucion_normal_model import DistribucionNormalModel
from src.db_data.models.services_model.duracion_repuestos_model import DuracionRepuestosModel
from src.utils.streamlit_utils import update_layout


class DuracionRepuestosPlotter:
    def __init__(self, repuesto: str, tipo_rep: str):
        self.df_duracion = db_to_df_by_repuesto_and_tipo_repuesto(DuracionRepuestosModel, repuesto, tipo_rep)
        self.df_distribucion = db_to_df_by_repuesto_and_tipo_repuesto(DistribucionNormalModel, repuesto, tipo_rep)

    def create_plot(self):
        fecha_min = self.df_duracion["FechaCambio"].min()
        fecha_max = self.df_duracion["FechaCambio"].max()
        cambios = self.df_distribucion["Cambio"].unique()
        rows: int = 3
        cols: int = 2

        fig = make_subplots(rows=rows, cols=cols, x_title="Duración en años", y_title="Frecuencia relativa en %",
                            horizontal_spacing=0.1,
                            specs=[
                                [{"secondary_y": True}, {"secondary_y": True}],
                                [{"secondary_y": True}, {"secondary_y": True}],
                                [{"secondary_y": True}, {"secondary_y": True}]
                            ],
                            subplot_titles=("Cambio 1", "Cambio 2",
                                            "Cambio 3", "Cambio 4",
                                            "Cambio 5", "Cambio 6"),
                            )

        cambios_iter = iter(cambios)
        cambio = next(cambios_iter, None)

        for c in range(1, cols + 1):
            for r in range(1, rows + 1):
                df_distri_cambio = self.df_distribucion.loc[self.df_distribucion["Cambio"] == cambio]
                df_duracion_cambio = self.df_duracion.loc[self.df_duracion["Cambio"] == cambio]


                # Campana de gauss
                x = df_distri_cambio["Años"]
                y = df_distri_cambio["DistribucionNormal"]

                # Histograma
                data = df_duracion_cambio["DuracionEnAños"]

                fig.add_trace(go.Histogram(
                    x=data,
                    name="Frecuencia de aparición anual",
                    histnorm="percent",
                    nbinsx=10,
                    nbinsy=10,
                    opacity=0.4,
                    legendgroup=f"Cambio: {cambio}"
                ), col=c, row=r, secondary_y=False)

                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers",
                    name="Distribucion",
                    legendgroup=f"Cambio: {cambio}"
                ), col=c, row=r, secondary_y=True)

                cambio = next(cambios_iter, None)

        fig.update_yaxes(title_text="", secondary_y=False) # Histograma
        fig.update_yaxes(title_text="Distribución en %", secondary_y=True) # Campana de gauss

        update_layout(fig, f"Duración repuestos ({fecha_min} | {fecha_max})",  height=725)
        fig.update_layout(
            barmode="overlay",
            showlegend=False,
            margin=dict(l=60, r=0, b=60, t=100),
        )
        return fig

    def create_plot2(self):
        fecha_min = self.df_duracion["FechaCambio"].min()
        fecha_max = self.df_duracion["FechaCambio"].max()
        cambios = self.df_distribucion["Cambio"].unique()
        rows: int = 3
        cols: int = 2
        lista_distri = []

        fig = make_subplots(rows=rows, cols=cols, subplot_titles=("Cambio 1", "Cambio 2",
                                                                  "Cambio 3", "Cambio 4",
                                                                  "Cambio 5", "Cambio 6"))

        print(cambios)
        for ca in cambios:
            df_distri_cambio = self.df_distribucion.loc[self.df_distribucion["Cambio"] == ca]
            print(df_distri_cambio)
            df_distri_cambio["DistribucionNormal"] = float(df_distri_cambio["DistribucionNormal"])

            ff.create_distplot([df_distri_cambio["DistribucionNormal"]], ["Distribucion"])


        update_layout(fig, f"Duracion repuestos ({fecha_min} | {fecha_max})", "",
                      "Duracion en años", 700, 600)

        return fig

