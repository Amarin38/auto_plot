import streamlit as st

from config.constants_views import PAG_USUARIOS_CODIGOS
from config.constants_common import TODAY_DATE_FILE_DMY

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from presentation.streamlit_components import ButtonComponents
from viewmodels.common.usuarios_codigos_vm import UsuariosCodigosVM


@execute_safely
def usuarios_codigos() -> None:
    common = CommonUtils()
    buttons = ButtonComponents()

    st.title(PAG_USUARIOS_CODIGOS)
    df = UsuariosCodigosVM().get_df()
    buttons.download_df(common.to_excel(df), f"codigos de usuarios {TODAY_DATE_FILE_DMY}.xlsx")

    st.data_editor(
        df,
        disabled=True,
        hide_index=True,
        height=600,
        # num_rows="dynamic",
        column_order=["UsuariosAntiguos", "UsuariosNuevos", "NombresAntiguos", "NombresNuevos"],
        column_config={
            "UsuariosAntiguos": st.column_config.TextColumn("Usuarios Antiguos", width=30),
            "UsuariosNuevos": st.column_config.TextColumn("Usuarios Nuevos", width=30),
            "NombresAntiguos": st.column_config.TextColumn("Nombres Antiguos", width=80),
            "NombresNuevos": st.column_config.TextColumn("Nombres Nuevos", width=80),
        }
    )