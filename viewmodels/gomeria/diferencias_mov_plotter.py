import numpy as np
import plotly.graph_objects as go

from typing import Union

from plotly.subplots import make_subplots

from config.constants_colors import COLORS
from utils.exception_utils import execute_safely
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.plotly_components import HoverComponents


class DiferenciaMovimientosEntreDepositosPlotter:
    def __init__(self) -> None:
        self.df = DiferenciaMovimientosEntreDepositosVM().get_df()

    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df.empty:
            df = self.df.set_index("Repuesto")

            df_costos = df[["Costo2024", "Costo2025"]]
            df_consumos = df[["Consumo2024", "Consumo2025"]]

            df_diferencias_consumos = df[["DiferenciaConsumos"]]
            df_diferencias_costos = df[["DiferenciaCostos"]]

            df_costos = df_costos.rename(columns={"Costo2024": "2024", "Costo2025": "2025"})
            df_consumos = df_consumos.rename(columns={"Consumo2024": "2024", "Consumo2025": "2025"})
            df_diferencias_consumos = df_diferencias_consumos.rename(columns={"DiferenciaConsumos": "Diferencia Consumos"})
            df_diferencias_costos = df_diferencias_costos.rename(columns={"DiferenciaCostos": "Diferencia Costos"})



            zmin_costo = df_costos.values.min()
            zmax_costo = df_costos.values.max()
            zmin_consumo = df_consumos.values.min()
            zmax_consumo = df_consumos.values.max()
            zmin_diferencia_costos = df_diferencias_costos.values.min()
            zmax_diferencia_costos = df_diferencias_costos.values.max()
            zmin_diferencia_consumo = df_diferencias_consumos.values.min()
            zmax_diferencia_consumo = df_diferencias_consumos.values.max()

            # Valores para la colorbar
            ticks_costo = np.linspace(zmin_costo, zmax_costo, 5).astype(int)
            ticks_consumo = np.linspace(zmin_consumo, zmax_consumo, 5).astype(int)
            ticks_dif_costo = np.linspace(zmin_diferencia_costos, zmax_diferencia_costos, 5).astype(int)
            ticks_dif_consumo = np.linspace(zmin_diferencia_consumo, zmax_diferencia_consumo, 5).astype(int)

            # Texto para la colorbar formateado a español
            ticks_texto_costo = [abreviar_es(v) for v in ticks_costo]
            ticks_texto_consumo = [abreviar_es(v) for v in ticks_consumo]
            ticks_texto_dif_costo = [abreviar_es(v) for v in ticks_dif_costo]
            ticks_texto_dif_consumo = [abreviar_es(v) for v in ticks_dif_consumo]

            # Texto abreviado para la colorbar
            hover_text_costo = np.vectorize(abreviar_es)(df_costos.values.astype(int))
            hover_text_consumo = np.vectorize(abreviar_es)(df_consumos.values.astype(int))
            hover_text_dif_costo = np.vectorize(abreviar_es)(df_diferencias_costos.values.astype(int))
            hover_text_dif_consumo = np.vectorize(abreviar_es)(df_diferencias_consumos.values.astype(int))


            fig = make_subplots(cols=7, rows=1,
                                subplot_titles=("Consumos", "", "Costos", "", "Diferencias consumos", "", "Diferencias costos"),
                                column_widths=[0.30, 0.15, 0.30, 0.20, 0.20, 0.15, 0.20],
                                shared_yaxes=True,)

            # Posiciones relativas al gráfico
            pos_consumos = fig.layout.xaxis.domain[1]
            pos_costos = fig.layout.xaxis3.domain[1]
            pos_diferencias_consumo = fig.layout.xaxis5.domain[1]
            pos_diferencias_costo = fig.layout.xaxis7.domain[1]


            fig.add_trace(go.Heatmap(
                x=df_consumos.columns.astype(str),
                y=df_consumos.index.astype(str),
                z=df_consumos.values.astype(int),
                text=hover_text_consumo,
                colorscale="Viridis",
                colorbar=dict(
                    title="",
                    tickmode="array",
                    tickvals=ticks_consumo,
                    ticktext=ticks_texto_consumo,
                    thickness=15,
                    x=pos_consumos + 0.001,
                    y=0.5,
                    len=0.9
                ),
                hovertemplate = """
<b>Cantidad:</b> %{text}
<extra></extra>
""",
            ), row=1, col=1)


            fig.add_trace(go.Heatmap(
                x=df_costos.columns.astype(str),
                y=df_costos.index.astype(str),
                z=df_costos.values.astype(int),
                text=hover_text_costo,
                colorscale="YlOrRd",
                colorbar=dict(
                    title="",
                    tickmode="array",
                    tickvals=ticks_costo,
                    ticktext=ticks_texto_costo,
                    thickness=15,
                    x=pos_costos + 0.001,
                    y=0.5,
                    len=0.9
                ),
                hovertemplate="""
<b>Cantidad:</b> %{text}
<extra></extra>
""",
            ), row=1, col=3)


            fig.add_trace(go.Heatmap(
                x=df_diferencias_consumos.columns.astype(str),
                y=df_diferencias_consumos.index.astype(str),
                z=df_diferencias_consumos.values.astype(int),
                text=hover_text_dif_consumo,
                colorscale="Viridis",
                colorbar=dict(
                    title="",
                    tickmode="array",
                    tickvals=ticks_dif_consumo,
                    ticktext=ticks_texto_dif_consumo,
                    thickness=15,
                    x=pos_diferencias_consumo + 0.001,
                    y=0.5,
                    len=0.9
                ),
                hovertemplate="""
<b>Cantidad:</b> %{text}
<extra></extra>
""",
            ), row=1, col=5)

            fig.add_trace(go.Heatmap(
                x=df_diferencias_costos.columns.astype(str),
                y=df_diferencias_costos.index.astype(str),
                z=df_diferencias_costos.values.astype(int),
                text=hover_text_dif_costo,
                colorscale="YlOrRd",
                colorbar=dict(
                    title="",
                    tickmode="array",
                    tickvals=ticks_dif_costo,
                    ticktext=ticks_texto_dif_costo,
                    thickness=15,
                    x=pos_diferencias_costo + 0.001,
                    y=0.5,
                    len=0.9
                ),
                hovertemplate="""
<b>Cantidad:</b> %{text}
<extra></extra>
""",
            ), row=1, col=7)


            fig.update_xaxes(
                tickmode="array",
                tickvals=["2024", "2025", "DiferenciaConsumos", "DiferenciaCostos"],
                ticktext=["Año 2024", "Año 2025", "Diferencia Consumos", "Diferencia Costos"]
            )

            fig.update_yaxes(
                tickfont=dict(size=13)
            )

            fig.update_layout(
                margin=dict(l=1, r=1, b=1, t=70),
                height=700,
                width=900,
                title=dict(
                    text="ℹ️ Diferencias de movimientos",
                    y=0.98
                )

            )

            HoverComponents().hover_junto(fig)
            return fig
        return None


def abreviar_es(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f} mil M"

    if n >= 1_000_000:
        return f"{n/1_000_000:.1f} M"

    if n >= 1_000:
        return f"{n/1_000:.0f} mil"

    return f"{int(n)}"
