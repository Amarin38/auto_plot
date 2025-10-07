import sys, os

import streamlit as st

from src.interfaces_abstract_classes.abs_column_view import ColumnView

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely

from src.plot.falla_garantias_plotter import FallasGarantiasPlotter

from src.config.constants import PLOT_BOX_HEIGHT, PLACEHOLDER
from src.config.enums import CabecerasEnum

from src.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


class FallaEquiposGarantiaPage(ColumnView):
    def __init__(self):
        super().__init__()

    @execute_safely
    def show(self):
        with super().container_select():
            cabecera = st.selectbox("Selecciona una Cabecera:", CabecerasEnum, index=None, placeholder=PLACEHOLDER)
            fallas = FallasGarantiasPlotter(cabecera)

        with super().container_pie():
            pie_plot, titulo = fallas.create_plot()

            st.subheader(titulo)
            st.plotly_chart(pie_plot)

        with st.container(height=PLOT_BOX_HEIGHT):
            consumo_plot = ConsumoGarantiasPlotter().create_plot()
            st.plotly_chart(consumo_plot)