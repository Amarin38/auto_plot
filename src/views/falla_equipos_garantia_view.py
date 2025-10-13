import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely

from src.plot.falla_garantias_plotter import FallasGarantiasPlotter

from src.config.constants import (PLACEHOLDER, DISTANCE_COLS_DUAL_PLOT, SELECT_BOX_HEIGHT,
                                  PIE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, PIE_PLOT_WIDTH, BARPLOT_WIDTH, TAB_BOX_HEIGHT,
                                  PIE_PLOT_BOX_WIDTH, SELECT_BOX_WIDTH, BARPLOT_BOX_HEIGHT, BARPLOT_BOX_WIDTH,
                                  FALLA_TAB_BOX_HEIGHT)
from src.config.enums import CabecerasEnum, RepuestoEnum

from src.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


class FallaEquiposGarantiaPage:
    @execute_safely
    def show(self):

        # pie, bar = st.columns(DISTANCE_COLS_DUAL_PLOT)
        with st.container(height=FALLA_TAB_BOX_HEIGHT):
            pie, bar = st.tabs([" 🚫 Falla Equipos Garantías", " 📊 Consumos Garantias y Transferencias"])

            with pie:
            # with pie.container(height=PIE_PLOT_BOX_HEIGHT, width=PIE_PLOT_BOX_WIDTH):
                with pie.container(height=SELECT_BOX_HEIGHT, width=SELECT_BOX_WIDTH):
                    col_cabecera, col_repuesto = st.columns(2)

                with col_cabecera:
                    cabecera = st.selectbox("Selecciona una cabecera: ", CabecerasEnum, index=None,
                                            placeholder=PLACEHOLDER)

                with col_repuesto:
                    tipo_repuesto = st.selectbox("Selecciona un tipo de repuesto: ", RepuestoEnum, index=None,
                                                 placeholder=PLACEHOLDER)

                fallas = FallasGarantiasPlotter(cabecera, tipo_repuesto)
                pie_plot = fallas.create_plot()

                st.plotly_chart(pie_plot)


            with bar:
                consumo_plot = ConsumoGarantiasPlotter().create_plot()
                st.plotly_chart(consumo_plot)