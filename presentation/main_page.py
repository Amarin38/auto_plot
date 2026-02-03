import streamlit as st

from config.enums_colors import CustomMetricColorsEnum
from config.constants_views import PAG_PRINCIPAL, CONTEO_BOX_HEIGHT, CONTEO_STATS_HEIGHT
from presentation.streamlit_components import OtherComponents
from viewmodels.conteo_stock.plotter import ConteoStockPlotter
from viewmodels.conteo_stock.vm import ConteoStockVM, calcular_porcentaje
from utils.common_utils import CommonUtils


@st.cache_data(ttl=300, show_spinner=False)
def _generar_datos():
    return ConteoStockVM().calcular_datos()

@st.cache_data(ttl=300, show_spinner="Cargando información...", show_time=True)
def _generar_grafico():
    return ConteoStockPlotter().create_plot()


def main():
    roles = st.session_state.get("roles") or []
    components = OtherComponents()
    utils = CommonUtils()

    st.title(PAG_PRINCIPAL)

    if "admin" in roles:
        datos, fig = utils.run_in_threads([_generar_datos, _generar_grafico], max_workers=2) # multithreading

        st.subheader("Conteo Stock 2025")

        pie, stats = st.columns([0.8, 1])

        with pie.container(height=CONTEO_BOX_HEIGHT):
            st.plotly_chart(fig)

        with stats.container(height=CONTEO_BOX_HEIGHT):
            rep_totales = 5894
            rep_contados = datos[5]
            porcentaje = calcular_porcentaje(rep_totales, rep_contados)
            precio_faltante = utils.num_parser(datos[0])
            precio_sobrante = utils.num_parser(datos[1])
            precio_abs_anterior = utils.num_parser(datos[2])
            precio_abs_actual = utils.num_parser(datos[3])
            porcentaje_perdida_stock = datos[4]
            porcentaje_error = round(((-datos[0] - datos[1]) * 100) / datos[3], 2)

            aux, medio, aux2 = st.columns([1, 2, 1])

            with medio.container(height=CONTEO_STATS_HEIGHT):
                aux5, interno, aux6 = st.columns([1, 1, 1])

                components.custom_metric(interno, "CONTEO", rep_contados, "white", "white",
                                         f"{porcentaje}%", "green")
                st.progress(int(porcentaje), str(rep_totales))

            # Datos de conteo
            col1, col2 = st.columns([1, 1])
            components.custom_metric(col1, "Precio faltante", precio_faltante,
                                     CustomMetricColorsEnum.ROJO, CustomMetricColorsEnum.ROJO)
            components.custom_metric(col2, "Precio sobrante", precio_sobrante,
                                     CustomMetricColorsEnum.AZUL, CustomMetricColorsEnum.AZUL)
            col1.divider()
            col2.divider()
            components.custom_metric(col1, "Precio absoluto anterior", precio_abs_anterior,
                                     CustomMetricColorsEnum.AMARILLO, CustomMetricColorsEnum.AMARILLO)
            components.custom_metric(col2, "Precio absoluto actual", precio_abs_actual,
                                     CustomMetricColorsEnum.VIOLETA, CustomMetricColorsEnum.VIOLETA)

            st.space(3)

            aux, izq, der, aux2 = st.columns([0.8, 1, 1, 0.8])

            components.custom_metric(izq, "Porcentaje perdida stock", f"{porcentaje_perdida_stock}%",
                                     CustomMetricColorsEnum.VERDE, CustomMetricColorsEnum.VERDE)
            components.custom_metric(der, "Porcentaje de error", f"{porcentaje_error}%",
                                     CustomMetricColorsEnum.ROJO, CustomMetricColorsEnum.ROJO)


