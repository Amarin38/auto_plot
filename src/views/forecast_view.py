import sys, os

import streamlit as st

from src.config.enums import RepuestoEnum
from src.interfaces_abstract_classes.abs_column_view import ColumnView

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.forecast_plotter import ForecastPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import (PLACEHOLDER, SELECT_BOX_HEIGHT, DISTANCE_COLS_SELECT_PLOT,
                                  MULTIPLE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT)


class ForecastPage:
    @execute_safely
    def show(self):
        figs = None
        col1, col2 = st.columns(DISTANCE_COLS_SELECT_PLOT)

        with col1.container(height=SELECT_BOX_HEIGHT):
            repuesto = st.selectbox("Selecciona el repuesto para prevision: ", RepuestoEnum, index=None, placeholder=PLACEHOLDER)

            plot = ForecastPlotter(repuesto)
            figs, titulo = plot.create_plot()


        with col2.container(height=MULTIPLE_PLOT_BOX_HEIGHT):
            st.subheader(titulo)

            if figs is not None:
                for fig in figs:
                    with st.container(height=PLOT_BOX_HEIGHT):
                        st.plotly_chart(fig)
