import streamlit as st

from config.constants_common import TODAY_DATE_FILE_DMY
from config.constants_views import PAG_COCHES_CABECERA
from presentation.streamlit_components import ButtonComponents, OtherComponents
from utils.common_utils import CommonUtils
from viewmodels.common.coches_cabecera_vm import CochesCabeceraVM


def coches_cabecera():
    other = OtherComponents()
    st.title(PAG_COCHES_CABECERA)

    df = CochesCabeceraVM().get_df()
    ButtonComponents().download_df(CommonUtils().to_excel(df), f"coches por cabecera {TODAY_DATE_FILE_DMY}.xlsx")

    key = "coches_cabecera"

    df_paginado, paginas = other.paginate(df, 15, key=key)

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

    other.paginate_buttons(paginas, key=key)