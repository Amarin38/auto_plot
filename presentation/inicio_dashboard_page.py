import streamlit as st

from config.enums_colors import CustomMetricColorsEnum
from config.constants_views import PAG_PRINCIPAL, CONTEO_BOX_HEIGHT, CONTEO_STATS_HEIGHT, REP_TOTALES_CONTEO
from presentation.streamlit_components import OtherComponents
from viewmodels.consumo.conteo_stock.plotter import ConteoStockPlotter
from viewmodels.consumo.conteo_stock.vm import ConteoStockVM
from utils.common_utils import CommonUtils

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
        with st.spinner("Cargando gráfico..."):
            df = _cargar_df()
            datos = _cargar_datos()

        st.subheader("Conteo Stock 2025")

        pie, stats = st.columns([0.8, 1])

        with pie.container(height=CONTEO_BOX_HEIGHT):
            if not df.empty:
                fig = ConteoStockPlotter(df).create_plot()
                st.plotly_chart(fig)

        with (stats.container(height=CONTEO_BOX_HEIGHT)):
            precio_faltante_raw         = datos[0]
            precio_sobrante_raw         = datos[1]
            precio_abs_anterior_raw     = datos[2]
            precio_abs_actual_raw       = datos[3]
            porcentaje_perdida_stock    = datos[4]
            rep_contados                = datos[5]

            precio_faltante             = utils.num_parser(precio_faltante_raw)
            precio_sobrante             = utils.num_parser(precio_sobrante_raw)
            precio_abs_anterior         = utils.num_parser(precio_abs_anterior_raw)
            precio_abs_actual           = utils.num_parser(precio_abs_actual_raw)
            porcentaje                  = vm.calcular_porcentaje(REP_TOTALES_CONTEO, rep_contados)
            porcentaje_error            = vm.calcular_porcentaje_error(precio_faltante_raw,
                                                                       precio_sobrante_raw,
                                                                       precio_abs_actual_raw)

            aux, medio, aux2 = st.columns([1, 2, 1])

            with medio.container(height=CONTEO_STATS_HEIGHT):
                aux5, interno, aux6 = st.columns([1, 1, 1])

                components.custom_metric(interno, "CONTEO", rep_contados, "white", "white",
                                         f"{porcentaje}%", "green")
                st.progress(int(porcentaje), str(REP_TOTALES_CONTEO))

            # Datos de conteo
            col1, col2 = st.columns([1, 1])

            components.custom_metric(col1, "Precio faltante",
                                     precio_faltante,
                                     CustomMetricColorsEnum.ROJO,
                                     CustomMetricColorsEnum.ROJO)
            components.custom_metric(col2, "Precio sobrante",
                                     precio_sobrante,
                                     CustomMetricColorsEnum.AZUL,
                                     CustomMetricColorsEnum.AZUL)
            col1.divider()
            col2.divider()
            components.custom_metric(col1, "Precio absoluto anterior",
                                     precio_abs_anterior,
                                     CustomMetricColorsEnum.AMARILLO,
                                     CustomMetricColorsEnum.AMARILLO)
            components.custom_metric(col2, "Precio absoluto actual",
                                     precio_abs_actual,
                                     CustomMetricColorsEnum.VIOLETA,
                                     CustomMetricColorsEnum.VIOLETA)

            st.space(3)

            aux, izq, der, aux2 = st.columns([0.8, 1, 1, 0.8])

            components.custom_metric(izq, "Porcentaje perdida stock",
                                     f"{porcentaje_perdida_stock}%",
                                     CustomMetricColorsEnum.VERDE,
                                     CustomMetricColorsEnum.VERDE)
            components.custom_metric(der, "Porcentaje de error",
                                     f"{porcentaje_error}%",
                                     CustomMetricColorsEnum.ROJO,
                                     CustomMetricColorsEnum.ROJO)


