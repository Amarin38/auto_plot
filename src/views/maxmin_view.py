import sys, os

import streamlit as st
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.services.analysis.maxmin import MaxMin
from src.services.utils.exception_utils import execute_safely


class MaxminPage:
    @execute_safely
    def show_table(self):
        maxmin = MaxMin()
        
        today_date = datetime.today().strftime("%d-%m-%Y")
        
        df = maxmin.create_maxmin()
        archivo = maxmin.to_excel(df) 
        
        # TODO: evitar que se recargue la página al presionar el botón  

        st.download_button(
            label="Descargar 💾",
            data=archivo,
            file_name=f"maxmin {today_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        

        st.table(df)