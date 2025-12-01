import plotly.graph_objects as go

from config.constants_colors import COLORS
from config.enums import ConsumoObligatorioEnum
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, ScatterComponents
from viewmodels.consumo.obligatorio.vm import ConsumoObligatorioVM


class ConsumoObligatorioPlotter:
    def __init__(self, tipo_rep: ConsumoObligatorioEnum) -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.scatter = ScatterComponents()

        self.df = ConsumoObligatorioVM().get_df_repuesto(tipo_rep)

    def create(self) -> go.Figure:
        fig = go.Figure()

        cabeceras = self.df["Cabecera"]
        y2023 = self.df["Año2023"]
        y2024 = self.df["Año2024"]
        y2025 = self.df["Año2025"]

        minimo_viejo = self.df["MinimoAntiguo"]
        minimo_nuevo = self.df["MinimoObligatorio"]

        fecha = self.df["UltimaFecha"][0].strftime("%d/%m/%Y")

        condicion_menor = self.df["Año2025"] < self.df["MinimoObligatorio"]
        condicion_mayor_igual = self.df["Año2025"] >= self.df["MinimoObligatorio"]

        porcentaje = 100 - round((self.df.loc[condicion_menor, "Año2025"] * 100) /
                                 self.df.loc[condicion_menor, "MinimoObligatorio"], 0)

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=minimo_viejo,
            name="Minimo Anterior",
            orientation="v",
            marker=dict(color=COLORS[1], opacity=1),
            legendgroup="A",
            hovertemplate="""
<b>
<span style='color:#FF5733'>Minimo Anterior:</span>
</b>%{y}
<extra></extra>
""",
        ))

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=y2023,
            name="2023",
            marker=dict(color=COLORS[7], opacity=1),
            legendgroup="A",
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
            legendgroup="A",
            hovertemplate = """
<b>
<span style='color:#F78154'>2024:</span>
</b>%{y}
<extra></extra>
""",
        ))

        fig.add_trace(go.Bar(
            x=cabeceras,
            y=minimo_nuevo,
            name="Minimo Actual",
            orientation="v",
            marker=dict(color=COLORS[14], opacity=1),
            legendgroup="B",
            hovertemplate = """
<b>
<span style='color:#5497A7'>Minimo Actual:</span>
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
            legendgroup="B",
            hovertemplate="""
<b>
<span style='color:#4D9078'>2025:</span>
</b>%{y}
<extra></extra>
""",
        ))


        self.scatter.cross(fig, self.df.loc[condicion_menor, "Cabecera"], y2024.loc[condicion_menor],
                           "Falta para el umbral", "Debajo del umbral por", porcentaje)

        self.scatter.tick(fig, self.df.loc[condicion_mayor_igual, "Cabecera"], y2024.loc[condicion_mayor_igual],
                          "Igual o sobre el umbral", "Igual o sobre el umbral")

        self.default.update_layout(fig, f"Ultima fecha: {fecha}", x_title="Cabecera", y_title="Consumo")
        self.hover.hover_junto(fig)

        fig.update_layout(
            margin={"r": 0, "t": 55, "l": 0, "b": 0},
        )

        return fig