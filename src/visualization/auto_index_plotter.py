import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from typing import Dict
from enum import Enum

from config.constants import COLORS
from services import InventoryDataCleaner, IndexUtils
from visualization import PlotConfig


class PlotTypeEnum(Enum):
    STACKED = "stacked"
    UNSTACKED = "unstacked"


class AutoIndexPlotter:
    def __init__(self, file: str, dir: str, rows: int, columns: int, 
                 plot_type: PlotTypeEnum, index_type: str) -> None:
        self.file = file
        self.dir = dir
        self.n_rows = rows
        self.n_cols = columns
        self.plot_type = plot_type 
        self.index_type = index_type

        self.divisor = PlotConfig.divisor_factor*self.n_cols
        self.iterador_colores = iter(COLORS)


    def create_plot(self) -> None:
        """
        ### Grafica el índice de consumo.\n
        #### Args:\n
            stacked_barplot (bool):\n
                - True -> un solo grafico apilado\n
                - False -> multiples graficos\n
            con_motor (bool): \n
                - True -> indice con motores totales por cabecera\n
                - False -> indice con coches totales por cabecera\n
        #### Returns:
            None
        """
        InventoryDataCleaner(self.file, self.dir).run_all()
        
        if self.plot_type == PlotTypeEnum.STACKED:
            self.barplot_stacked(IndexUtils._prepare_data(self.index_type, self.file, self.dir))
        elif self.plot_type == PlotTypeEnum.UNSTACKED:
            self.barplot_unstacked(IndexUtils._prepare_data(self.index_type, self.file, self.dir))
        else:
            raise ValueError(f"Tipo de grafico no soportado: {self.plot_type}")


    def barplot_stacked(self, lista_indice) -> None:
        df_indices_consumo: pd.DataFrame = lista_indice[0]
        iterador_repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique()))

        fig, ax = plt.subplots(figsize=(PlotConfig.figure_width, PlotConfig.figure_height), squeeze=False)
        
        y_dict_consumo: Dict[str, np.ndarray] = {}
        
        for rep in iterador_repuestos:
            rep_comparado: bool = df_indices_consumo["Repuesto"] == rep

            x_cabecera = df_indices_consumo.loc[rep_comparado, "Cabecera"]
            y_dict_consumo.update({rep:df_indices_consumo.loc[rep_comparado, "IndiceConsumo"]})


        for repuesto, y_consumo in y_dict_consumo.items():
            zorder: int = round((PlotConfig.zorder_base/max(y_consumo))*PlotConfig.zorder_multiplier, 0)
            try:
                color = next(self.iterador_colores) # itero sobre los colores
            except StopIteration:
                pass
            
            bars = ax.bar(x_cabecera, y_consumo, label=repuesto, color=color, zorder=zorder) # type: ignore
            
            ax.bar_label(bars, fontsize=PlotConfig.label_fontsize) # type: ignore
        
        ax.legend(loc="upper right", fontsize=PlotConfig.legend_fonsize) # type: ignore
        ax.tick_params("x", labelsize=PlotConfig.x_tick_fontsize/self.divisor) # type: ignore
        ax.tick_params("y", labelsize=PlotConfig.y_tick_fontsize) # type: ignore

        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=PlotConfig.suptitle_font_size, y=0.93)
        fig.subplots_adjust(wspace=PlotConfig.wspace, hspace=PlotConfig.hspace)


    def barplot_unstacked(self, lista_indice) -> None:
        df_indices_consumo: pd.DataFrame = lista_indice[0]
        iterador_repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique()))

        fig, axs = plt.subplots(self.n_rows, self.n_cols, figsize=(PlotConfig.figure_width, PlotConfig.figure_height), squeeze=False)
        
        for i in range(axs.shape[0]):
            for j in range(axs.shape[1]):
                try:
                    rep = next(iterador_repuestos)
                    color = next(self.iterador_colores)
                except StopIteration:
                    pass
                
                rep_comparado: pd.Series[bool] = df_indices_consumo["Repuesto"] == rep

                x_cabecera = df_indices_consumo.loc[rep_comparado, "Cabecera"]
                y_consumo = df_indices_consumo.loc[rep_comparado, "IndiceConsumo"]
                
                bars = axs[i,j].bar(x_cabecera, y_consumo, color=color)
                axs[i,j].bar_label(bars, fontsize=17)

                media_con_cero = y_consumo.mean()
                # media_con_cero = IndexUtils._calculate_average(y_consumo.tolist(), with_zero=True)
                axs[i,j].axhline(y=media_con_cero, linestyle="--", color="#618B4A")
                axs[i,j].text(x=1.01, 
                              y=media_con_cero, 
                              s=f"{media_con_cero}", 
                              color="black", 
                              va="center", 
                              transform=axs[i,j].get_yaxis_transform(), 
                              fontsize=PlotConfig.text_font_size*2)

                media_sin_cero = y_consumo.replace(0, np.nan).mean()
                # media_sin_cero = IndexUtils._calculate_average(y_consumo.tolist(), with_zero=False)
                axs[i,j].axhline(y=media_sin_cero, linestyle="--", color="#922D50")
                axs[i,j].text(x=1.01, 
                              y=media_sin_cero, 
                              s=f"{media_sin_cero}", 
                              color="black", 
                              va="center", 
                              transform=axs[i,j].get_yaxis_transform(), 
                              fontsize=PlotConfig.text_font_size*2)

                axs[i,j].legend(["Media con cero", "Media sin cero"], fontsize=PlotConfig.legend_fonsize, loc=1)
                axs[i,j].axhline(0, color="black")
                axs[i,j].set_title(rep, fontsize=PlotConfig.plot_title_fontsize)
                axs[i,j].set_ylabel("Consumo", fontsize=PlotConfig.label_fontsize, labelpad=20)

                axs[i,j].tick_params("x", labelsize=PlotConfig.x_tick_fontsize)
                axs[i,j].tick_params("y", labelsize=PlotConfig.y_tick_fontsize*2)
                
        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=PlotConfig.suptitle_font_size, y=0.93)
        fig.subplots_adjust(wspace=PlotConfig.wspace, hspace=PlotConfig.hspace)