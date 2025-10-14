import sys, os

import streamlit as st

from src.utils.streamlit_utils import select_box

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely

from src.plot.falla_garantias_plotter import FallasGarantiasPlotter

from src.config.constants import FALLA_TAB_BOX_HEIGHT
from src.config.enums import CabecerasEnum, RepuestoEnum

from src.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


@execute_safely
def falla_equipos_garantias_page():
    with (st.container(height=FALLA_TAB_BOX_HEIGHT)):
        pie, bar = st.tabs([" 🚫 Falla Equipos Garantías", " 📊 Consumos Garantias y Transferencias"])

        with pie:
            aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

            cabecera = select_box(cabecera_col, "Selecciona una cabecera para ver su falla: ", CabecerasEnum)
            tipo_repuesto = select_box(repuesto_col, "Selecciona un tipo de repuesto para ver su falla: ", RepuestoEnum)

            pie_plot = FallasGarantiasPlotter(cabecera, tipo_repuesto).create_plot()
            st.plotly_chart(pie_plot)

        with bar:
            consumo_plot = ConsumoGarantiasPlotter().create_plot()
            st.plotly_chart(consumo_plot)