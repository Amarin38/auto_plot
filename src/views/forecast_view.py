import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.forecast_plotter import ForecastPlotter

# from src.views.streamlit_utils import StreamlitUtils 
from src.utils.exception_utils import execute_safely

from src.config.constants import REPUESTOS_OPT, SELECT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS

class ForecastPage:
    def __init__(self) -> None:
        self.plot = ForecastPlotter()
        # self.utils = StreamlitUtils()

    @execute_safely
    def prevision_options(self):
        figs = None
        col1, col2 = st.columns(DISTANCE_COLS)


        with col1.container(height=SELECT_BOX_HEIGHT):
            opcion_prevision = st.selectbox("Selecciona una previsión:", REPUESTOS_OPT)

            match opcion_prevision:
                case "Inyectores": ...
                case "Bombas inyectoras": ...
                case "Bombas urea": ...
                case "Calipers": ...
                case "Camaras": ...
                case "DVRs": ...
                case "Electroválvulas 5 vias": ...
                case "Flotantes de gasoil": ...
                case "Herramientas": ...
                case "Retenes": figs = self.plot.create_plot("RETEN")
                case "Sensores": ...
                case "Taladros": ...
            
            # with col1.container(height=SELECT_BOX_HEIGHT):
            #     self.utils.download_df(self.utils.to_excel(figs[1]), "data.xlsx") # type: ignore
            #     self.utils.download_df(self.utils.to_excel(figs[2]), "trend.xlsx") # type: ignore

        with col2.container(height=PLOT_BOX_HEIGHT):
            if opcion_prevision != REPUESTOS_OPT[0]:
                st.subheader(self.plot._devolver_titulo(opcion_prevision))
            
            if figs is not None:
                for fig in figs[0]:
                    st.plotly_chart(fig)

    