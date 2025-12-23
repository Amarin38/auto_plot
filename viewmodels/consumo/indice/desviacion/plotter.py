from typing import Optional

import pandas as pd
import plotly.graph_objects as go

from config.constants_common import FILE_STRFTIME_DMY
from config.constants_colors import COLORS, FALLAS_GARANTIAS_COLORS
from config.enums import RepuestoEnum

from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, LegendComponents, HoverComponents
from viewmodels.consumo.indice.desviacion.vm import DesviacionIndicesVM


class DeviationPlotter:
    def __init__(self, tipo_rep: Optional[RepuestoEnum]) -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.legend = LegendComponents()
        self.hover = HoverComponents()

        self.tipo_rep = tipo_rep

        if tipo_rep:
            self.color = FALLAS_GARANTIAS_COLORS[3]
            self.df = DesviacionIndicesVM().get_df_by_tipo_rep(tipo_rep)
        else:
            self.color = COLORS[9]
            self.df = DesviacionIndicesVM().get_df().drop_duplicates(subset=[
                "Cabecera", "MediaCabecera", "MediaDeMedias",
                "Diferencia", "Desviacion", "DesviacionPor", "FechaCompleta"
            ])
            self.tipo_rep = " "


    @execute_safely
    def create_plot(self) -> go.Figure:
        x_data = self.df["Cabecera"] 
        y_data = self.df["Desviacion"]

        y_porcentual = self.df["Desviacion"].astype(str) + "%"

        fecha = pd.to_datetime(self.df["FechaCompleta"].iloc[0]).strftime(FILE_STRFTIME_DMY)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            name=f"Desviación de índices",
            
            text=y_porcentual,
            textposition="outside",
            textfont=dict(
                size=11,
                color='white', 
                family='Arial'  
            ),
            marker=dict(color=self.color),
            hovertemplate="""
<b>
<span style='color:{color}'>Desviación:</span>
%{{text}}
</b>
<extra></extra>
""".format(color=self.color)
        ))


        fig.add_trace(go.Scatter(
            x=x_data,
            y=[0] * len(x_data),
            mode='lines',

            name="Centro de desviaciones (Media)",
            line=dict(color='orange', dash='dash'),
            hovertemplate="""
<b>
<span style='color:orange'>Media</span>
</b>
<extra></extra>
"""
        ))


        for cab in x_data:
            y0 = y_data.min() - 50
            y1 = y_data.max() + 50

            fig.add_shape(type="line",
                x0=cab, y0=y0, x1=cab, y1=y1,
                line=dict(color=self.color, width=1), opacity=0.6)


        self.default.update_layout(fig, f"Desviacion {self.tipo_rep} {fecha}", 'Cabecera',
                                   'Desviacion de la media en %', 600, 200)

        self.legend.top_right_legend(fig)
        self.hover.hover_junto(fig)
        self.hover.color_hover_bar_colored(fig, self.color)
        return fig