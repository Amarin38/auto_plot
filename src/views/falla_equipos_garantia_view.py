import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely

from src.plot.falla_garantias_plotter import FallasGarantiasPlotter

from src.config.constants import , PLACEHOLDER, DISTANCE_COLS_DUAL_PLOT, SELECT_BOX_HEIGHT, \
    PIE_PLOT_BOX_HEIGHT
from src.config.enums import CabecerasEnum

from src.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


class FallaEquiposGarantiaPage:
    @execute_safely
    def show(self):
        col1, col2 = st.columns(DISTANCE_COLS_DUAL_PLOT)

        with col1.container(height=SELECT_BOX_HEIGHT):
            cabecera = st.selectbox("Selecciona una cabecera: ", CabecerasEnum, index=None, placeholder=PLACEHOLDER)
            fallas = FallasGarantiasPlotter(cabecera)

        with col1.container(height=PIE_PLOT_BOX_HEIGHT):
            pie_plot = fallas.create_plot()

            st.plotly_chart(pie_plot)

        with col2.container(height=):
            consumo_plot = ConsumoGarantiasPlotter().create_plot()
            st.plotly_chart(consumo_plot)
