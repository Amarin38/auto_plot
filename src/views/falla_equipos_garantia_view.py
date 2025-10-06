import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely

from src.plot.falla_garantias_plotter import FallasGarantiasPlotter

from src.config.constants import FULL_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, SELECT_BOX_HEIGHT, DISTANCE_COLS, \
    PIE_PLOT_BOX_HEIGHT
from src.config.enums import CabecerasEnum

from src.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


class FallaEquiposGarantiaPage:
    def __init__(self):
        self.fallas = FallasGarantiasPlotter()

    @execute_safely
    def show(self):
        col1, col2 = st.columns(DISTANCE_COLS)

        with col1.container(height=SELECT_BOX_HEIGHT):
            cabecera = st.selectbox("Cabecera", CabecerasEnum, index=None, placeholder="------")

        with col2.container(height=PIE_PLOT_BOX_HEIGHT):
            pie_plot = self.fallas.create_plot(cabecera)
            st.subheader(self.fallas.devolver_titulo(cabecera))

            st.plotly_chart(pie_plot)

        with st.container(height=PLOT_BOX_HEIGHT):
            consumo_plot = ConsumoGarantiasPlotter().create_plot()
            st.plotly_chart(consumo_plot)