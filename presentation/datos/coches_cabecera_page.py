import streamlit as st

from config.constants_views import PAG_COCHES_CABECERA
from presentation.streamlit_components import Paginate
from viewmodels.datos_vm import CochesCabeceraVM


def coches_cabecera():
    paginate = Paginate()
    st.title(PAG_COCHES_CABECERA)

    df = CochesCabeceraVM().get_df()
    key = "coches_cabecera"

    df_paginado, paginas = paginate.create_pagination(df, 15, key)

    st.data_editor(
        df_paginado,
        disabled=True,
        hide_index=True,
        height=600,
        column_order=["Cabecera", "CochesDuermen", "CochesDuermenNuevo", "CochesSinScania"],
        column_config={
            "Cabecera": st.column_config.TextColumn("Cabecera"),
            "CochesDuermen": st.column_config.NumberColumn("Coches Duermen"),
            "CochesDuermenNuevo": st.column_config.NumberColumn("Coches Duermen Nuevo"),
            "CochesSinScania": st.column_config.NumberColumn("Coches Sin Scania"),
        }
    )

    paginate.create_buttons(paginas, key=key)