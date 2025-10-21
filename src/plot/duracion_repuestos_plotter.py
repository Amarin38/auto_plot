import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff

from src.db_data.crud_common import db_to_df
from src.db_data.models.services_model.distribucion_normal_model import DistribucionNormalModel
from src.db_data.models.services_model.duracion_repuestos_model import DuracionRepuestosModel


class DuracionRepuestosPlotter:
    def __init__(self):
        self.df_duracion = db_to_df(DuracionRepuestosModel)
        self.df_distribucion = db_to_df(DistribucionNormalModel)

    def create_plot(self):
        fig = go.Figure()

        # fig.add_trace(ff.create_distplot())