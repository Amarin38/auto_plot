import sys, os

import streamlit as st

from src.config.constants import TODAY_DATE_FILE, DATAFRAME_HEIGHT

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import download_df, to_excel
from src.db_data.crud_services import db_to_df
from src.db_data.models.services_model.maxmin_model import MaxminModel

@execute_safely
def maxmin_page():
    df = db_to_df(MaxminModel)
    download_df(to_excel(df), f"maxmin {TODAY_DATE_FILE}.xlsx")

    st.dataframe(df, height=DATAFRAME_HEIGHT)