import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from typing import Dict
from enum import Enum

from config.constants import COLORS, OUT_PATH
from config.dataclasses import PlotConfig
from visualization.plot_utils import PlotUtils
from services.utils.index_utils import IndexUtils
from services.utils.exception_utils import execute_safely

class AutoIndexPlotter:
    def __init__(self, file: str, dir: str, rows: int, columns: int, index_type: str) -> None:
        self.file = file
        self.dir = dir
        self.n_rows = rows
        self.n_cols = columns

        self.lista_indices: pd.DataFrame = IndexUtils._prepare_data(index_type, file, dir) #type:ignore
        self.df_indices_consumo = self.lista_indices[0]
        self.title = self.lista_indices[1]
        self.iterador_repuestos = iter(tuple(self.df_indices_consumo["Repuesto"].unique()))

        self.divisor = PlotConfig.divisor_factor*self.n_cols
        self.iterador_colores = iter(COLORS)


    @execute_safely
    def barplot(self) -> None:
        """
        ### Grafica el índice de consumo.\n
        #### Args:\n
            con_motor (bool): \n
                - motor -> indice con motores totales por cabecera\n
                - vehicle -> indice con coches totales por cabecera\n
        #### Returns:
            None
        """
        fig, axs = plt.subplots(self.n_rows, self.n_cols, figsize=(PlotConfig.figure_width, PlotConfig.figure_height), squeeze=False)
        fig.suptitle(f"Indice {self.title}", fontsize=PlotConfig.suptitle_font_size, y=PlotConfig.title_position)
        fig.subplots_adjust(wspace=PlotConfig.wspace, hspace=PlotConfig.hspace)

        for i in range(axs.shape[0]):
            for j in range(axs.shape[1]):
                try:
                    rep = next(self.iterador_repuestos)
                    color = next(self.iterador_colores)
                except StopIteration:
                    continue
                
                rep_comparado: pd.Series[bool] = self.df_indices_consumo["Repuesto"] == rep

                # Data
                x_cabecera = self.df_indices_consumo.loc[rep_comparado, "Cabecera"]
                y_consumo = self.df_indices_consumo.loc[rep_comparado, "IndiceConsumo"]
                
                # Bars
                bars = axs[i,j].bar(x_cabecera, y_consumo, color=color)
                axs[i,j].bar_label(bars, fontsize=PlotConfig.bar_fontsize)

                # Mean
                media_sin_cero = round(y_consumo.replace(0, np.nan).mean(), 2)
                PlotUtils._auto_median_line(axs[i,j], media_sin_cero)

                # General config.
                axs[i,j].legend(["Media sin cero"], fontsize=PlotConfig.legend_fonsize, loc=1)
                axs[i,j].axhline(0, color="black")
                axs[i,j].set_title(rep, fontsize=PlotConfig.plot_title_fontsize)
                axs[i,j].set_ylabel("Consumo", fontsize=PlotConfig.label_fontsize, labelpad=20)

                # Tick params
                axs[i,j].tick_params("x", labelsize=PlotConfig.x_tick_fontsize)
                axs[i,j].tick_params("y", labelsize=PlotConfig.y_tick_fontsize*2)
                
        plt.savefig(f"{OUT_PATH}/{self.file}.png")
        plt.show()