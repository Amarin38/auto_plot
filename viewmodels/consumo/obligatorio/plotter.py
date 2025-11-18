import plotly.graph_objects as go

from config.constants import COLORS
from config.enums import ConsumoObligatorioEnum
from utils.streamlit_utils import update_layout, hover
from viewmodels.consumo.obligatorio.vm import ConsumoObligatorioVM


class ConsumoObligatorioPlotter:
    def __init__(self, tipo_rep: ConsumoObligatorioEnum) -> None:
        self.df = ConsumoObligatorioVM().get_df_repuesto(tipo_rep)

    def create(self) -> go.Figure:
        fig = go.Figure()

        cabeceras = self.df["Cabecera"]
        y2023 = self.df["Año2023"]
        y2024 = self.df["Año2024"]
        y2025 = self.df["Año2025"]
        minimo = self.df["MinimoObligatorio"]
        fecha = self.df["UltimaFecha"][0].strftime("%d/%m/%Y")

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=y2023,
            name="2023",
            marker=dict(color=COLORS[7], opacity=1),
            hovertemplate="""
<b>
<span style='color:#F2C14E'>2023:</span>
</b>%{y}
<extra></extra>
""",
        ))

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=y2024,
            name="2024",
            marker = dict(color=COLORS[8], opacity=1),
            hovertemplate = """
<b>
<span style='color:#F78154'>2024:</span>
</b>%{y}
<extra></extra>
""",
        ))

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=y2025,
            name="2025",
            orientation="v",
            marker = dict(color=COLORS[9], opacity=1),
            hovertemplate="""
<b>
<span style='color:#4D9078'>2025:</span>
</b>%{y}
<extra></extra>
""",
        ))

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=minimo,
            name="Minimo Obligatorio",
            orientation="v",
            marker=dict(color=COLORS[2], opacity=1),
            hovertemplate = """
<b>
<span style='color:#C70039'>Minimo:</span>
</b>%{y}
<extra></extra>
""",
        ))

        update_layout(fig, f"Ultima fecha: {fecha}", x_title="Cabecera", y_title="Consumo")
        hover(fig)

        fig.update_layout(
            margin={"r": 0, "t": 55, "l": 0, "b": 0},
        )

        # TODO: agregar alerta cuando está por arriba del 10% de diferencia
        # TODO: agregar otra barra que tenga el Mínimo obligatorio antiguo para comparar con 2023 y 2024
        return fig