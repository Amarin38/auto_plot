import plotly.graph_objects as go

from typing import Union

from config.constants_colors import COLORS
from utils.exception_utils import execute_safely
from viewmodels.gomeria.transferencias_dep_vm import TransferenciasEntreDepositosVM


class TransferenciasEntreDepositosPlotter:
    def __init__(self, cabecera: str) -> None:
        self.cabecera = cabecera
        self.df_transfer = TransferenciasEntreDepositosVM().get_df_by_cabecera(cabecera)

    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df_transfer.empty:
            df_2024 = self.df_transfer.loc[self.df_transfer["Año"] == 2024]
            df_2025 = self.df_transfer.loc[self.df_transfer["Año"] == 2025]

            x_2024 = df_2024["Repuesto"]
            y_2024 = df_2024["Cantidad"]

            x_2025 = df_2025["Repuesto"]
            y_2025 = df_2025["Cantidad"]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_2024,
                y=y_2024,
                name="2024",
                mode='lines+markers',

                line = dict(color=COLORS[12], width=2),
                marker = dict(
                    color=COLORS[12],
                    size=8,
                    symbol='circle',
                ),

                hovertemplate="""
<b><span style='color:#3F7CAC'>2024</span></b>
<br>
<b>Cantidad:</b> %{y}
<extra></extra>
""",
            ))

            fig.add_trace(go.Scatter(
                x=x_2025,
                y=y_2025,
                name="2025",
                mode = 'lines+markers',

                line = dict(color=COLORS[2], width=2, dash='dot'),
                marker = dict(
                    color=COLORS[2],
                    size=8,
                    symbol='square',
                ),

                hovertemplate="""
<b><span style='color:#C70039'>2025</span></b>
<br>
<b>Cantidad:</b> %{y}
<extra></extra>
""",
            ))

            fig.update_layout(
                hovermode="x unified",  # 🔹 muestra ambos hovers juntos
                hoverlabel=dict(
                    bgcolor="#0E1117",  # color de fondo
                    bordercolor="black",
                    font_size=14.5,  # 🔹 aumenta el tamaño del texto
                    font_family="Arial",
                    namelength=-1
                ),
                height=500
            )
            return fig
        return None