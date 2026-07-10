import streamlit as st

from config.enums_colors import CustomMetricColorsEnum
from config.constants_views import PAG_PRINCIPAL, CONTEO_BOX_HEIGHT, REP_TOTALES_CONTEO
from presentation.streamlit_components import OtherComponents
from plotters.conteo_stock_plotter import ConteoStockPlotter
from utils.common_utils import CommonUtils
from viewmodels.consumo_vm import ConteoStockVM

vm = ConteoStockVM()

@st.cache_data(ttl=300, show_spinner=True)
def _cargar_datos():
    return vm.calcular_datos()

@st.cache_data(ttl=300, show_time=True)
def _cargar_df():
    return vm.get_df()


def main():
    roles = st.session_state.get("roles") or []
    components = OtherComponents()
    utils = CommonUtils()

    st.title(PAG_PRINCIPAL)

    if "admin" in roles:
        with st.spinner("Cargando conteo stock..."):
            df = _cargar_df()
            datos = _cargar_datos()

        st.subheader("Conteo Stock 2025 📈")

        pie, stats = st.columns([0.8, 1])

        with pie.container(height=CONTEO_BOX_HEIGHT):
            if len(df):
                fig = ConteoStockPlotter(df).create_plot()
                st.plotly_chart(fig)

        with (stats.container(height=CONTEO_BOX_HEIGHT)):
            precio_faltante_raw         = datos["precio_faltante"]
            precio_sobrante_raw         = datos["precio_sobrante"]
            precio_abs_anterior_raw     = datos["precio_anterior"]
            precio_abs_actual_raw       = datos["precio_actual"]
            porcentaje_perdida_stock    = datos["porcentaje_dif"]
            rep_contados                = datos["contados"]

            precio_faltante             = utils.num_parser(precio_faltante_raw)
            precio_sobrante             = utils.num_parser(precio_sobrante_raw)
            precio_abs_anterior         = utils.num_parser(precio_abs_anterior_raw)
            precio_abs_actual           = utils.num_parser(precio_abs_actual_raw)
            porcentaje                  = vm.calcular_porcentaje(REP_TOTALES_CONTEO, rep_contados)
            porcentaje_error            = vm.calcular_porcentaje_error(precio_faltante_raw,
                                                                       precio_sobrante_raw,
                                                                       precio_abs_actual_raw)

            _, medio, _ = st.columns([1, 1, 1])

            components.custom_metric(
                col=medio,
                label="CONTEO",
                value=rep_contados,
                border_color="white",
                val_color="white",
                delta=f"{porcentaje}%",
            )
            medio.space(1)

            # Datos de conteo
            col1, col2 = st.columns([1, 1])

            components.custom_metric(
                col=col1,
                label="Precio faltante",
                value=precio_faltante,
                border_color=CustomMetricColorsEnum.ROJO,
                val_color=CustomMetricColorsEnum.ROJO
            )
            components.custom_metric(
                col=col2,
                label="Precio sobrante",
                value=precio_sobrante,
                border_color=CustomMetricColorsEnum.AZUL,
                val_color=CustomMetricColorsEnum.AZUL
            )

            col1.divider()
            col2.divider()

            components.custom_metric(
                col=col1,
                label="Precio absoluto anterior",
                value=precio_abs_anterior,
                border_color=CustomMetricColorsEnum.AMARILLO,
                val_color=CustomMetricColorsEnum.AMARILLO
            )
            components.custom_metric(
                col=col2,
                label="Precio absoluto actual",
                value=precio_abs_actual,
                border_color=CustomMetricColorsEnum.VIOLETA,
                val_color=CustomMetricColorsEnum.VIOLETA
            )

            st.space(1)

            _, izq, der, _ = st.columns([0.6, 1, 1, 0.6])

            components.custom_metric(
                col=izq,
                label="Porcentaje perdida stock",
                value=f"{porcentaje_perdida_stock}%",
                border_color=CustomMetricColorsEnum.VERDE,
                val_color=CustomMetricColorsEnum.VERDE
            )
            components.custom_metric(
                col=der,
                label="Porcentaje de error",
                value=f"{porcentaje_error}%",
                border_color=CustomMetricColorsEnum.ROJO,
                val_color=CustomMetricColorsEnum.ROJO
            )


