import sys, os

import streamlit as st

from src.config.constants import FULL_PLOT_BOX_HEIGHT, TAB_BOX_HEIGHT
from src.db_data.models.services_model.deviation_model import DeviationModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.deviation_plotter import DeviationPlotter
from src.utils.exception_utils import execute_safely
from src.db_data.crud_services import db_to_df

class DeviationPage:
    @execute_safely
    def show(self):
        with st.container(height=TAB_BOX_HEIGHT):
            plot, data = st.tabs([" 📊 Gráfico", " ℹ️ Datos"])

            with plot:
                with st.container(height=FULL_PLOT_BOX_HEIGHT):
                    st.plotly_chart(DeviationPlotter().create_plot())
            with data:
                st.dataframe(db_to_df(DeviationModel), height=FULL_PLOT_BOX_HEIGHT)
