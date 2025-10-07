import sys, os
import streamlit as st

from src.interfaces_abstract_classes.abs_column_view import ColumnView

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import PLACEHOLDER
from src.config.enums import IndexTypeEnum, RepuestoEnum


class IndexPage(ColumnView):
    def __init__(self) -> None:
        super().__init__()


    @execute_safely
    def show(self) -> None:
        with super().container_select():
            repuesto = st.selectbox("Selecciona una Repuesto:", RepuestoEnum, index=None, placeholder=PLACEHOLDER)

            with super().container_select():
                tipo_indice = st.selectbox("Selecciona un Tipo de indice:", IndexTypeEnum)

                plot = IndexPlotter(tipo_indice, repuesto)
                self.figs, titulo = plot.create_plot()


        with super().container_plot():
            st.subheader(titulo)

            if self.figs is not None:
                for fig in self.figs:
                    st.plotly_chart(fig)

