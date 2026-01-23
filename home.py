import streamlit as st
import streamlit_authenticator as stauth

from infrastructure import DBBase, db_engine
from presentation.dota_licitaciones_page import dota_licitaciones_page

from presentation.main_page import main
from presentation.cargar_datos_page import cargar_datos
from presentation.coches_cabecera_page import coches_cabecera
from presentation.consumo_obligatorio_page import consumo_obligatorio
from presentation.consumo_prevision_page import consumo_prevision
from presentation.consumo_indice_page import consumo_indice
from presentation.consumo_historial_page import consumo_historial
from presentation.garantias_falla_equipos_page import garantias_falla_equipos
from presentation.gomeria_transferencias_depositos_page import gomeria_transferencias_entre_depositos
from presentation.maximos_minimos_page import maximos_minimos
from presentation.duracion_repuestos_page import duracion_repuestos
from presentation.parque_movil_page import parque_movil
from presentation.sisssa_page import sissa_page
from presentation.streamlit_components import OtherComponents
from viewmodels.autenticacion.usuario_vm import UsuarioVM

from config.constants_views import (PAG_PRINCIPAL, PAG_CARGAR_DATOS, PAG_INDICES, PAG_PREVISION,
                                    PAG_FALLA_GARANTIAS, PAG_MAXIMOS_MINIMOS, PAG_DURACION,
                                    PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, PAG_HISTORIAL, PAG_CONSUMO_OBLIGATORIO,
                                    PAG_COCHES_CABECERA, PAG_PARQUE_MOVIL, PAG_SISSSA, PAG_DOTA_LICITACIONES)

from infrastructure.db.models.coches_cabecera_model import CochesCabeceraModel
from infrastructure.db.models.garantias_consumo_model import GarantiasConsumoModel
from infrastructure.db.models.garantias_datos_model import GarantiasDatosModel
from infrastructure.db.models.garantias_falla_model import GarantiasFallaModel
from infrastructure.db.models.consumo_indice_model import ConsumoIndiceModel
from infrastructure.db.models.consumo_historial_model import ConsumoHistorialModel
from infrastructure.db.models.consumo_obligatorio_model import ConsumoObligatorioModel
from infrastructure.db.models.consumo_prevision_data_model import ConsumoPrevisionDataModel
from infrastructure.db.models.consumo_prevision_model import ConsumoPrevisionModel
from infrastructure.db.models.consumo_desviacion_indices_model import ConsumoDesviacionIndicesModel
from infrastructure.db.models.gomeria_diferencia_mov_dep_model import GomeriaDiferenciaMovEntreDepModel
from infrastructure.db.models.gomeria_transferencias_dep_model import GomeriaTransferenciasEntreDepModel
from infrastructure.db.models.distribucion_normal_model import DistribucionNormalModel
from infrastructure.db.models.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.db.models.maximos_minimos_model import MaximosMinimosModel
from infrastructure.db.models.json_config_model import JSONConfigModel
from infrastructure.db.models.parque_movil_model import ParqueMovilModel
from infrastructure.db.models.conteo_stock_model import ConteoStockModel
from infrastructure.db.models.usuario_model import UsuarioModel

# -----------------------------------------------------------------------------------------------
# CONFIG STREAMLIT
# -----------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Estadísticas Dota",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------------------------
# SESSION STATE INIT
# -----------------------------------------------------------------------------------------------

st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("welcome_shown", False)
st.session_state.setdefault("roles", [])
st.session_state.setdefault("username", None)
st.session_state.setdefault("name", None)

if "credentials" not in st.session_state:
    credentials = UsuarioVM().get_credentials() or {"usernames": {}}
    st.session_state.credentials = credentials

# -----------------------------------------------------------------------------------------------
# AUTHENTICATOR
# -----------------------------------------------------------------------------------------------

authenticator = stauth.Authenticate(
    st.session_state.credentials,
    "cookie",
    "4rfVgy7#",
    cookie_expiry_days=0,
)

# -----------------------------------------------------------------------------------------------
# LOGIN (SOLO SI NO ESTÁ AUTENTICADO)
# -----------------------------------------------------------------------------------------------
aux, centro, aux2 = st.columns(3)

if not st.session_state.authenticated:
    with centro:
        try:
            authenticator.login(location="main",
                            clear_on_submit=True,
                            fields={
                                "Form name": "Iniciar sesión",
                                "Username": "Usuario",
                                "Password": "Contraseña",
                                "Login": "Entrar"
                            }
                            )
        except Exception as e:
            st.error(e)

        auth_status = st.session_state.get("authentication_status")

        if auth_status is True:
            st.session_state.authenticated = True
            st.session_state.username = st.session_state.get("username")
            st.session_state.name = st.session_state.get("name")
            st.rerun()

        elif auth_status is False:
            OtherComponents().flash_alert_error("Usuario o contraseña incorrectos.")
            st.stop()

        else:
            st.warning("Ingrese sus credenciales.")
            st.stop()


# -----------------------------------------------------------------------------------------------
# POST LOGIN (NO SE REEJECUTA)
# -----------------------------------------------------------------------------------------------
with centro:
    if not st.session_state.welcome_shown:
        OtherComponents().flash_alert_success("Accedió correctamente.")
        st.session_state.welcome_shown = True


# Cargar roles solo una vez
if not st.session_state.roles and st.session_state.username:
    user_entity = UsuarioVM().repo.get_by_nombre(st.session_state.username)
    if user_entity and user_entity.Rol:
        st.session_state.roles = [user_entity.Rol]
    else:
        st.session_state.roles = []

roles = st.session_state.roles or []

# -----------------------------------------------------------------------------------------------
# PAGES
# -----------------------------------------------------------------------------------------------

pages = {
    "Inicio": [
        st.Page(main, title=PAG_PRINCIPAL),
        st.Page(sissa_page, title=PAG_SISSSA),
        st.Page(dota_licitaciones_page, title=PAG_DOTA_LICITACIONES),
        st.Page(cargar_datos, title=PAG_CARGAR_DATOS)
    ],
    "Estadísticas de consumo": [
        st.Page(consumo_indice, title=PAG_INDICES),
        st.Page(consumo_prevision, title=PAG_PREVISION),
        st.Page(duracion_repuestos, title=PAG_DURACION),
        st.Page(consumo_historial, title=PAG_HISTORIAL),
        st.Page(consumo_obligatorio, title=PAG_CONSUMO_OBLIGATORIO),
    ],
    "Estadísticas de garantías": [
        st.Page(garantias_falla_equipos, title=PAG_FALLA_GARANTIAS),
    ],
    "Estadísticas de gomería": [
        st.Page(gomeria_transferencias_entre_depositos, title=PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)
    ],
    "Datos": [
        st.Page(maximos_minimos, title=PAG_MAXIMOS_MINIMOS),
        st.Page(coches_cabecera, title=PAG_COCHES_CABECERA),
        st.Page(parque_movil, title=PAG_PARQUE_MOVIL)
    ],
}

# Restricciones por rol
if "user" in roles:
    pages["Inicio"] = pages["Inicio"][:1]
    pages.pop("Datos", None)

# -----------------------------------------------------------------------------------------------
# LOGOUT
# -----------------------------------------------------------------------------------------------
if st.session_state.get("authentication_status"):
    nav = st.navigation(pages, position="sidebar")
    authenticator.logout("Cerrar sesión", "sidebar")

    if st.session_state.get("authentication_status") is None:
        nav = st.navigation({"Inicio": [st.Page(main, title="Inicio")]}, position="sidebar")

        st.session_state.clear()
        st.session_state["authenticated"] = False
        st.session_state["welcome_shown"] = False
        st.session_state["username"] = None
        st.session_state["name"] = None
        st.session_state["roles"] = []

        st.rerun()
    nav.run()

# -----------------------------------------------------------------------------------------------
# NAVIGATION
# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    DBBase.metadata.create_all(db_engine)
