import random
import itertools

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from src.config.constants import COLORS
from src.services.utils.exception_utils import execute_safely

from src.config.dataclasses import PlotConfig
from src.plotting.plot_utils import PlotUtils
from src.services.utils.index_utils import IndexUtils

class AutoIndexPlotter:
    def __init__(self, file: str, directory: str, rows: int, columns: int, index_type: str, tipo_rep: str) -> None:
        self.file = file
        self.n_rows = rows
        self.n_cols = columns
        self.colors = COLORS

        self.df_indices_consumo, self.title = IndexUtils().prepare_data(index_type, self.file, directory, tipo_rep)

        self.iterador_repuestos = iter(tuple(self.df_indices_consumo["Repuesto"].unique())) #type: ignore
        self.iterador_colores = itertools.cycle(self.colors) # ciclo infinito
        self.plot_config = PlotConfig()


    @execute_safely
    def create_figure(self):
        fig, axs = plt.subplots(self.n_rows, self.n_cols, figsize=(self.plot_config.FIG_WIDTH, self.plot_config.FIG_HEIGHT), squeeze=False)

        fig.suptitle(f"Indice {self.title}", fontsize=self.plot_config.SUPTITLE_SIZE, y=self.plot_config.TITLE_POS)
        fig.subplots_adjust(wspace=self.plot_config.WSPACE, hspace=self.plot_config.HSPACE)

        return fig, axs


    @execute_safely
    def single_barplot(self, repuesto):
        """Creates a single barplot by repuesto"""

        fig, axs = self.create_figure()
        ax = axs[0, 0]

        rep_comparado = self.df_indices_consumo["Repuesto"] == repuesto # type:ignore
        
        # Data
        x_cabecera: pd.Series = self.df_indices_consumo.loc[rep_comparado, "Cabecera"] #type: ignore
        y_consumo: pd.Series = self.df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] #type: ignore

        # Bars
        bars = ax.bar(x_cabecera, y_consumo, color=self.colors[random.randint(0, 19)])
        
        self._plot_config(ax, y_consumo, bars, repuesto)

        return fig
        # plt.savefig(f"{OUT_PATH}/{repuesto}.png")
        # plt.show()
        # plt.close("all")


    @execute_safely
    def barplot(self):
        """
        ### Grafica el índice de consumo.\n
        #### Args:\n
            con_motor (bool): \n
                - motor -> indice con motores totales por cabecera\n
                - vehicle -> indice con coches totales por cabecera\n
        #### Returns:
            None
        """
        fig, axs = self.create_figure()

        for ax in axs.flat:
            rep = next(self.iterador_repuestos, None)
            color = next(self.iterador_colores)
            
            rep_comparado: pd.Series[bool] = self.df_indices_consumo["Repuesto"] == rep #type: ignore

            # Data
            x_cabecera: pd.Series = self.df_indices_consumo.loc[rep_comparado, "Cabecera"] #type: ignore
            y_consumo: pd.Series = self.df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] #type: ignore
            
            # Bars
            bars = ax.bar(x_cabecera, y_consumo, color=color)

            self._plot_config(ax, y_consumo, bars, rep) # type: ignore
        return fig
        
        # plt.savefig(f"{OUT_PATH}/{self.file}.png")
        # plt.show()
        # plt.close("all")


    @execute_safely
    def _plot_config(self, ax, y_consumo, bar, repuesto: str):
        ax.bar_label(bar, fontsize=self.plot_config.BAR_SIZE)

         # Mean
        media_sin_cero = round(y_consumo.replace(0, np.nan).mean(), 2)
        PlotUtils._auto_median_line(ax, media_sin_cero)

        # General config.
        ax.legend(["Media sin cero"], fontsize=self.plot_config.LEGEND_SIZE, loc=1)
        ax.axhline(0, color="black")
        ax.set_title(repuesto, fontsize=self.plot_config.PLOT_TITLE_SIZE)
        ax.set_ylabel("Consumo", fontsize=self.plot_config.LABEL_SIZE, labelpad=self.plot_config.LABEL_PAD)

        # Tick params
        ax.tick_params("x", labelsize=self.plot_config.X_TICK_SIZE)
        ax.tick_params("y", labelsize=self.plot_config.Y_TICK_SIZE*2)