import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import (PLACEHOLDER, SELECT_BOX_HEIGHT, DISTANCE_COLS_SELECT_PLOT,
                                  PLOT_BOX_HEIGHT, MULTIPLE_PLOT_BOX_HEIGHT)
from src.config.enums import IndexTypeEnum, RepuestoEnum


class IndexPage:
    @execute_safely
    def show(self) -> None:
        figs = None
        col1, col2 = st.columns(DISTANCE_COLS_SELECT_PLOT)

        with col1.container(height=SELECT_BOX_HEIGHT):
            repuesto = st.selectbox("Selecciona el repuesto: ", RepuestoEnum, index=None, placeholder=PLACEHOLDER)

            with col1.container(height=SELECT_BOX_HEIGHT):
                tipo_indice = st.selectbox("Selecciona el tipo de indice: ", IndexTypeEnum)

                plot = IndexPlotter(tipo_indice, repuesto)
                figs, titulo = plot.create_plot()


        with col2.container(height=MULTIPLE_PLOT_BOX_HEIGHT):
            st.subheader(titulo)

            if figs is not None:
                for fig in figs:
                    with st.container(height=PLOT_BOX_HEIGHT):
                        st.plotly_chart(fig)

