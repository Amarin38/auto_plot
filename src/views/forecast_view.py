import sys, os

import streamlit as st

from src.config.enums import RepuestoEnum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.forecast_plotter import ForecastPlotter

# from src.views.streamlit_utils import StreamlitUtils 
from src.utils.exception_utils import execute_safely

from src.config.constants import SELECT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS

class ForecastPage:
    def __init__(self) -> None:
        self.plot = ForecastPlotter()
        # self.utils = StreamlitUtils()

    @execute_safely
    def prevision_options(self):
        figs = None
        repuesto_upper = None

        col1, col2 = st.columns(DISTANCE_COLS)


        with col1.container(height=SELECT_BOX_HEIGHT):
            opcion_prevision = st.selectbox("Selecciona una previsión:", RepuestoEnum, index=None, placeholder="------")

            if opcion_prevision is not None:
                repuesto_upper = opcion_prevision.upper()

            figs = self.plot.create_plot(repuesto_upper)


        with col2.container(height=PLOT_BOX_HEIGHT):
            st.subheader(self.plot.devolver_titulo(opcion_prevision))
            
            if figs is not None:
                for fig in figs[0]:
                    st.plotly_chart(fig)
