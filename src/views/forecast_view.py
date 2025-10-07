import sys, os

import streamlit as st

from src.config.enums import RepuestoEnum
from src.interfaces_abstract_classes.abs_column_view import ColumnView

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.forecast_plotter import ForecastPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import PLACEHOLDER


class ForecastPage(ColumnView):
    def __init__(self) -> None:
        super().__init__()

    @execute_safely
    def show(self):
        with super().container_select():
            repuesto = st.selectbox("Selecciona una repuesto:", RepuestoEnum, index=None, placeholder=PLACEHOLDER)

            plot = ForecastPlotter(repuesto)
            self.figs, titulo = plot.create_plot()


        with super().container_plot():
            st.subheader(titulo)

            if self.figs is not None:
                for fig in self.figs:
                    st.plotly_chart(fig)
