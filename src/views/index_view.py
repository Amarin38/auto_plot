import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import SELECT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS
from src.config.enums import IndexTypeEnum, RepuestoEnum


class IndexPage:
    def __init__(self) -> None:
        self.plot = IndexPlotter()


    @execute_safely
    def indice_options(self) -> None:
        figs = None
        repuesto_upper = None

        col1, col2 = st.columns(DISTANCE_COLS)
        
        with col1.container(height=SELECT_BOX_HEIGHT):
            opcion_repuesto_indice = st.selectbox("Selecciona un índice:", RepuestoEnum, index=None, placeholder="------")

            if opcion_repuesto_indice is not None:
                repuesto_upper = opcion_repuesto_indice.upper()

            with col1.container(height=SELECT_BOX_HEIGHT):
                opcion_tipo_indice = st.selectbox("Selecciona un tipo de indice:", IndexTypeEnum)
                    
                match opcion_repuesto_indice:
                    case RepuestoEnum.INYECTOR:
                        figs = self.plot.create_plot(opcion_tipo_indice, repuesto_upper, repuesto_upper)
                    case _:
                        figs = self.plot.create_plot(opcion_tipo_indice, repuesto_upper)


        with col2.container(height=PLOT_BOX_HEIGHT):
            st.subheader(self.plot.devolver_titulo(opcion_repuesto_indice)) # type: ignore

            if figs is not None:
                for fig in figs:
                    st.plotly_chart(fig) 
            
