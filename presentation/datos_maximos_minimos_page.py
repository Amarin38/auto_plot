import streamlit as st

from config.constants_views import PAG_MAXIMOS_MINIMOS

from utils.exception_utils import execute_safely
from presentation.streamlit_components import OtherComponents
from viewmodels.datos.maximos_minimos_vm import MaximosMinimosVM


@execute_safely
def maximos_minimos():
    other = OtherComponents()

    st.title(PAG_MAXIMOS_MINIMOS)
    df = MaximosMinimosVM().get_df()

    key="maximos_minimos"

    df_paginado, paginas = other.paginate(df, 15, key)

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
