import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.deviation_plotter import DeviationPlotter
from src.views.streamlit_utils import StreamlitUtils
from src.utils.exception_utils import execute_safely
from src.db.crud import sql_to_df

class DeviationPage:
    @execute_safely
    def show_deviation(self):
        plot, data = st.tabs(["Gráfico", "Datos"])
        
        with plot:
            with st.container(height=640):
                st.plotly_chart(DeviationPlotter().create_plot())
        with data:
            st.dataframe(sql_to_df("deviation"))
        