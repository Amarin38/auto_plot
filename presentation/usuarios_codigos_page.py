import streamlit as st

from config.constants_views import PAG_USUARIOS_CODIGOS
from config.constants_common import TODAY_DATE_FILE_DMY

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from presentation.streamlit_components import ButtonComponents, OtherComponents
from viewmodels.common.usuarios_codigos_vm import UsuariosCodigosVM


@execute_safely
def usuarios_codigos() -> None:
    other = OtherComponents()

    st.title(PAG_USUARIOS_CODIGOS)
    df = UsuariosCodigosVM().get_df()
    ButtonComponents().download_df(CommonUtils().to_excel(df), f"codigos de usuarios {TODAY_DATE_FILE_DMY}.xlsx")

    key="usuarios_codigos"
    df_paginado, paginas = other.paginate(df, 15, key=key)

    st.data_editor(
        df_paginado,
        disabled=True,
        hide_index=True,
        height=600,
        column_order=["UsuariosAntiguos", "UsuariosNuevos", "NombresAntiguos", "NombresNuevos"],
        column_config={
            "UsuariosAntiguos": st.column_config.TextColumn("Usuarios Antiguos", width=30),
            "UsuariosNuevos": st.column_config.TextColumn("Usuarios Nuevos", width=30),
            "NombresAntiguos": st.column_config.TextColumn("Nombres Antiguos", width=80),
            "NombresNuevos": st.column_config.TextColumn("Nombres Nuevos", width=80),
        }
    )

    other.paginate_buttons(paginas, key=key)
