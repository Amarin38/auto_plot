import streamlit as st

from config.constants import TODAY_DATE_FILE, DATAFRAME_HEIGHT, PAG_MAXMIN
from utils.exception_utils import execute_safely
from utils.streamlit_utils import download_df, to_excel
from db_data.crud_services import ServiceRead
from db_data.models.services_model.maxmin_model import MaxminModel

@execute_safely
def maxmin_page():
    st.title(PAG_MAXMIN)
    df = ServiceRead.all_df(MaxminModel)
    download_df(to_excel(df), f"maxmin {TODAY_DATE_FILE}.xlsx")

    st.dataframe(df, height=DATAFRAME_HEIGHT)