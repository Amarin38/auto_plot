from typing import List, Dict, Optional, Any

import numpy as np
import pandas as pd
from multipledispatch import dispatch
from plotly.graph_objs import Figure


from config.constants_colors import COLORS, HOVER_COLOR
from config.enums import SymbolEnum, DashEnum
from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
import plotly.graph_objects as go

class HoverComponents:
    def __init__(self):
        ...

    @execute_safely
    def hover_junto(self, fig):
        fig.update_layout(
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor=HOVER_COLOR,
                bordercolor="gray",
                font_size=14.5,
                font_family="Arial",
                namelength=-1
            ),
        )

    @execute_safely
    def hover_x(self, fig):
        fig.update_layout(
            hovermode="x",
            hoverlabel=dict(
                bgcolor=HOVER_COLOR,
                bordercolor="gray",
                font_size=16,
                font_family="Arial",
                namelength=-1
            ),
        )

    @execute_safely
    def hover_y(self, fig):
        fig.update_layout(
            hovermode="y",  # 🔹 muestra ambos hovers juntos
            hoverlabel=dict(
                bgcolor="#0E1117",  # color de fondo
                bordercolor="black",
                font_size=14.5,  # 🔹 aumenta el tamaño del texto
                font_family="Arial",
                namelength=-1
            ),
        )

    @execute_safely
    def color_hover_bar_subplot(self, fig):
        for axis in fig.layout:
            if axis.startswith("xaxis"):
                fig.layout[axis].update(
                    showspikes=True,
                    spikemode="across+marker",
                    spikecolor="rgba(255,255,255)",
                    spikethickness=2,
                    spikedash="solid"
                )

    @execute_safely
    def color_hover_bar(self, fig):
        fig.update_xaxes(
            showspikes=True,
            spikemode="across+marker",
            spikesnap="data",
            spikethickness=2,
            spikecolor="rgba(255,255,255)",
            spikedash="solid",
        )

    @execute_safely
    def color_hover_bar_colored(self, fig, color: str):
        fig.update_xaxes(
            showspikes=True,
            spikemode="across+marker",
            spikesnap="data",
            spikethickness=2,
            spikecolor=color,
            spikedash="solid",
        )


    @execute_safely
    def tick_array(self, fig, tickvals, ticktext):
        fig.update_xaxes(
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
        )


class LegendComponents:
    def __init__(self):
        ...

    @execute_safely
    def top_right_legend(self, fig):
        fig.update_layout(
            autosize=True,
            legend=dict(
                orientation='v',
                yanchor='top',
                y=1.15,
                xanchor='right',
                x=1,
                font=dict(size=13),
                bgcolor=COLORS[-1],
                bordercolor=COLORS[5],
            ),
        )


class SliderComponents:
    def __init__(self):
        ...

    @execute_safely
    def range_slider(self, fig):
        fig.update_layout(
            xaxis=dict(
                range=["2024-06-01", "2026-12-01"],
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1 Mes",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6 Meses",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="1 Año",
                             step="year",
                             stepmode="backward"),
                        dict(count=2,
                             label="2 Años",
                             step="year",
                             stepmode="backward"),
                        dict(count=3,
                             label="3 Años",
                             step="year",
                             stepmode="backward"),
                        dict(label="Todo",
                             step="all")
                    ]),
                ),
                rangeslider=dict(
                    visible=True,
                    bgcolor="white",
                    bordercolor="#0e1117",
                    thickness=0.02,
                    borderwidth=2,
                ),
                type="date"
            )
        )


class DropDownComponents:
    def __init__(self):
        ...

    @execute_safely
    def dropdown(self, fig, buttons: List[Dict]):
        fig.update_layout(
            updatemenus=[
                dict(
                    type="dropdown",
                    direction="down",
                    x=0.5,
                    y=1.15,
                    xanchor="center",
                    yanchor="top",
                    font=dict(color="white", size=14),
                    active=0,
                    bgcolor=COLORS[-1],
                    pad=dict(l=1, r=800, t=12, b=5),
                    showactive=True,

                    buttons=buttons
                )
            ]
        )


class PlotComponents:
    def __init__(self):
        self.common = CommonUtils()

    @execute_safely
    def empty(self, fig, nombre: str):
        fig.add_trace(go.Scatter(
            x=[None],  # nada visible
            y=[None],
            mode="markers",
            marker=dict(color="rgba(0,0,0,0)"),  # transparente
            showlegend=True,
            name=nombre,
            legendgroup="ConsumoPrevision"
        ))


    @dispatch(Figure, pd.Series, pd.Series, str, str, pd.Series)
    def cross(self, fig: Figure, x: pd.Series, y: pd.Series, nombre: str, texto: str, custom: Any):
        fig.add_trace(go.Scatter(
            x=x,
            y=[val + 2 for val in y],
            mode="markers",
            name=nombre,
            marker=dict(
                size=10,
                color="#C70039",
                symbol="x",
                line=dict(width=0.5),
            ),
            legendgroup="emoji",
            customdata=custom,
            hovertemplate="""
<b>
<span style='color:#C70039'>{texto}:</span>
%{{customdata}}%
</b>
<extra></extra>
        """.format(texto=texto)
        ))

    @dispatch(Figure, pd.Series, pd.Series, str, str)
    def cross(self, fig: Figure, x: pd.Series, y: pd.Series, nombre: str, texto: str):
        fig.add_trace(go.Scatter(
            x=x,
            y=[val + 2 for val in y],
            mode="markers",
            name=nombre,
            marker=dict(
                size=10,
                color="#C70039",
                symbol="x",
                line=dict(width=0.5),
            ),
            legendgroup="emoji",
            hovertemplate="""
<b>
<span style='color:#C70039'>{texto}</span>
</b>
<extra></extra>
        """.format(texto=texto)
        ))


    @dispatch(Figure, pd.Series, pd.Series, str, str, pd.Series)
    def tick(self, fig: Figure, x: pd.Series, y: pd.Series, nombre: str, texto: str, custom: Any):
        fig.add_trace(go.Scatter(
            x=x,
            y=[val + 2 for val in y],
            mode="markers+text",
            name=nombre,
            marker=dict(
                size=11,
                color="#3A7D44",
                symbol="circle",
                line=dict(width=0.5),
            ),
            text=["✔"] * 12,
            legendgroup="emoji",
            customdata=custom,
            hovertemplate="""
<b>
<span style='color:#3A7D44'>{texto}:</span>
%{{customdata}}%
</b>
<extra></extra>
        """.format(texto=texto)
        ))

    @dispatch(Figure, pd.Series, pd.Series, str, str)
    def tick(self, fig: Figure, x: pd.Series, y: pd.Series, nombre: str, texto: str):
        fig.add_trace(go.Scatter(
            x=x,
            y=[val + 2 for val in y],
            mode="markers+text",
            name=nombre,
            marker=dict(
                size=11,
                color="#3A7D44",
                symbol="circle",
                line=dict(width=0.5),
            ),
            text=["✔"] * 12,
            legendgroup="emoji",
            hovertemplate="""
<b>
<span style='color:#3A7D44'>{texto}</span>
</b>
<extra></extra>
        """.format(texto=texto)
        ))


    @execute_safely
    def mid_line(self, fig: Figure, x, y, nombre: str, texto: str):
        fig.add_trace(go.Scatter(
            x=x,
            y=[val + 1 for val in y],
            mode="markers",
            name=nombre,
            marker=dict(
                size=11,
                color="#F2C14E",
                symbol="line-ew-open",
                line=dict(width=2),
            ),
            legendgroup="emoji",
            hovertemplate="""
<b>
<span style='color:#F2C14E'>{texto}</span>
</b>
<extra></extra>
""".format(texto=texto)
        ))


    @execute_safely
    def heat_map(self, fig: Figure, xyz: pd.DataFrame, n_row: int, n_col: int, color: str, x_pos: float):
        z_numpy     = xyz.to_numpy(dtype=int)
        zmin, zmax  = z_numpy.min(), z_numpy.max()
        ticks       = np.linspace(zmin, zmax, 5).astype(int)
        ticks_texto = [self.common.abreviar_es(v) for v in ticks]
        hover_text  = [[self.common.abreviar_es(v) for v in row] for row in z_numpy]

        fig.add_trace(go.Heatmap(
            x=xyz.columns,
            y=xyz.index,
            z=z_numpy,
            text=hover_text,
            colorscale=color,
            colorbar=dict(
                title="",
                tickmode="array",
                tickvals=ticks,
                ticktext=ticks_texto,
                thickness=15,
                x=x_pos,
                y=0.5,
                len=0.9
            ),
            hovertemplate="""
<b>Cantidad:</b> %{text}
<extra></extra>
""",
        ), row=n_row, col=n_col)

    @execute_safely
    def scatter_gomeria(self, fig: Figure, x, y, name: str, color: str, symbol: SymbolEnum, dash: DashEnum):
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            name=name,
            mode='lines+markers',

            line=dict(color=color, width=2, dash=dash),
            marker=dict(
                color=color,
                size=8,
                symbol=symbol,
            ),
            hovertemplate="""
<b><span style='color:{color}'>{name}</span></b>
<br>
<b>Cantidad:</b> %{{y}}
<extra></extra>
""".format(color=color, name=name)),
        )

    @execute_safely
    def scatter_prevision(self, fig: Figure, x, y, name: str, color: str, color_line: str, symbol: SymbolEnum, dash: DashEnum, custom: Optional[list[str]]):
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            name=name,
            mode='lines+markers',

            text=y,
            textposition='top center',
            textfont=dict(
                size=19,
                color=color
            ),

            line=dict(color=color_line, width=2, dash=dash),
            marker=dict(
                color=color_line,
                size=8,
                symbol=symbol,
            ),
            legendgroup=name,
            customdata=custom,
            hovertemplate="""
<b>
<span style='color:{color}'>{name}:</span>
%{{y}}</b>
<extra></extra>
""".format(color=color_line, name=name),
        ))

    @execute_safely
    def bar_indice_consumo(self, fig: Figure, x, y, name: str, text, color: str, custom):
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            name=name,

            text=text,
            textposition="none",
            textfont=dict(
                size=15,
                color='white',
                family='Arial'
            ),

            marker=dict(color=color),
            customdata=custom,
            hovertemplate="""
<b>
<span style='color:%{customdata[1]}'>%{customdata[0]}:</span>
<span style='color:white'>%{text} </span>
</b>
<extra></extra>
""",
        ))

class DefaultUpdateLayoutComponents:
    def __init__(self):
        ...

    @execute_safely
    def update_layout(self, fig, title: str, x_title: str = None, y_title: str = None, height: Optional[int] = 500,
                      width: Optional[int] = 500):
        fig.update_layout(
            title=title,
            legend=dict(
                orientation='v',
                y=1.02,
                x=1,
                font=dict(size=13)
            ),
            showlegend=True,

            xaxis=dict(
                title=x_title,
                showticklabels=True
            ),

            yaxis=dict(
                title=y_title,
                showticklabels=True
            ),

            height=height,
            width=width,
        )
