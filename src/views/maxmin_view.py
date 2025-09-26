import sys, os

import streamlit as st
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely
from src.views.streamlit_utils import StreamlitUtils
from src.db_data.crud_services import db_to_df

class MaxminPage:
    @execute_safely
    def show_table(self):
        utils = StreamlitUtils()
        today_date = datetime.today().strftime("%d-%m-%Y")
        
        df = db_to_df("maxmin")
        utils.download_df(utils.to_excel(df), f"maxmin {today_date}.xlsx")
        
        st.dataframe(df, height=600)