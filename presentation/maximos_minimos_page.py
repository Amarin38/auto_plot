import streamlit as st

from config.constants import TODAY_DATE_FILE, DATAFRAME_HEIGHT, PAG_maximos_minimos
from utils.exception_utils import execute_safely
from utils.streamlit_utils import download_df, to_excel
from infrastructure.repositories.services.crud_services import ServiceRead
from infrastructure.db.models.services.maximos_minimos_model import MaximosMinimosModel

@execute_safely
def maximos_minimos():
    st.title(PAG_maximos_minimos)
    df = ServiceRead.all_df(MaximosMinimosModel)
    download_df(to_excel(df), f"maximos_minimos {TODAY_DATE_FILE}.xlsx")

    st.dataframe(df, height=DATAFRAME_HEIGHT)