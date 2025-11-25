import streamlit as st

from config.constants import TODAY_DATE_FILE, DATAFRAME_HEIGHT, PAG_MAXIMOS_MINIMOS
from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from presentation.streamlit_components import ButtonComponents
from viewmodels.maximos_minimos.vm import MaximosMinimosVM


@execute_safely
def maximos_minimos():
    common = CommonUtils()
    buttons = ButtonComponents()

    st.title(PAG_MAXIMOS_MINIMOS)
    df = MaximosMinimosVM().get_df()
    buttons.download_df(common.to_excel(df), f"maximos_minimos {TODAY_DATE_FILE}.xlsx")

    st.dataframe(df, height=DATAFRAME_HEIGHT)