import streamlit as st

from config.constants_views import DATAFRAME_HEIGHT, PAG_MAXIMOS_MINIMOS
from config.constants_common import TODAY_DATE_FILE_DMY

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from presentation.streamlit_components import ButtonComponents, OtherComponents
from viewmodels.common.maximos_minimos_vm import MaximosMinimosVM


@execute_safely
def maximos_minimos():
    common = CommonUtils()
    buttons = ButtonComponents()
    other = OtherComponents()

    st.title(PAG_MAXIMOS_MINIMOS)
    df = MaximosMinimosVM().get_df()
    buttons.download_df(common.to_excel(df), f"maximos y minimos {TODAY_DATE_FILE_DMY}.xlsx")

    key="maximos_minimos"

    df_paginado, paginas = other.paginate(df, 15, key=key)

    st.data_editor(
        df_paginado,
        disabled=True,
        hide_index=True,
        height=600,
        column_order=["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"],
        column_config={
            "Familia": st.column_config.NumberColumn("Familia", width=1),
            "Articulo": st.column_config.NumberColumn("Artículo", width=1),
            "Repuesto": st.column_config.TextColumn("Repuesto", width=500),
            "Minimo": st.column_config.NumberColumn("Mínimo", width=300),
            "Maximo": st.column_config.NumberColumn("Máximo", width=300),
        }
    )

    other.paginate_buttons(paginas, key=key)
