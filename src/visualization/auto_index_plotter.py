import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from typing import List, Dict, Union
from enum import Enum
from dataclasses import dataclass

from src.config.constants import COLORS, MAIN_PATH, DIVISOR_FACTOR, ZORDER_MULTIPLIER, ZORDER_BASE
from src.services import IndexUtils, IndexByMotor, IndexByVehicle
from src.services import InventoryDataCleaner, InventoryUpdate 


class PlotType(Enum):
    STACKED = "stacked"
    UNSTACKED = "unstacked"

class IndexType(Enum):
    BY_MOTOR = "motor"
    BY_VEHICLE = "vehicle"

@dataclass
class PlotConfig():
    font_size = 15
    figure_width = 70
    figure_height = 70


# TODO modificar para simplificar más
class AutoIndexPlotter:
    def __init__(self, file: str, dir: str, rows: int, columns: int) -> None:
        self.file = file
        self.dir = dir
        self.n_rows = rows
        self.n_cols = columns
        
        self.divisor = DIVISOR_FACTOR*self.n_cols
        
        self.iterador_colores = iter(COLORS)


    def create_plot(self, plot_type: PlotType, index_type: IndexType) -> None:
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
        prepared_data = self.prepare_data(index_type)
        
        if plot_type == PlotType.STACKED:
            self.create_stacked_barplot(prepared_data)
        elif plot_type == PlotType.UNSTACKED:
            self.create_unstacked_barplot(prepared_data)
        else:
            raise ValueError(f"Tipo de grafico no soportado: {plot_type}")

    def prepare_data(self, index_type: IndexType) -> List[pd.DataFrame | str]:
        if index_type == IndexType.BY_MOTOR:
            df_rows = InventoryUpdate().update_rows_by_dict(self.file, "motores")
            df_rows.to_excel(f"{MAIN_PATH}/out/{self.file}-S.xlsx")
            lista_indice: List[Union[pd.DataFrame, str]] = IndexByMotor(self.file, self.dir).calculate_index()
        
        elif index_type == IndexType.BY_VEHICLE:
            lista_indice: List[Union[pd.DataFrame, str]] = IndexByVehicle(self.file, self.dir).calculate_index()
        
        else:
            raise ValueError(f"Tipo de indice no soportado: {index_type}")

        return lista_indice


    def create_stacked_barplot(self, lista_indice) -> None:
        df_indices_consumo: pd.DataFrame = lista_indice[0]
        iterador_repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique())) # type: ignore

        fig, ax = plt.subplots(figsize=(PlotConfig.figure_width, PlotConfig.figure_height), squeeze=False)
        
        y_dict_consumo: Dict[str, np.ndarray] = {}
        
        for rep in iterador_repuestos:
            rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

            x_cabecera: List[str] = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
            y_dict_consumo.update({
                rep:df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                })

        for repuesto, y_consumo in y_dict_consumo.items():  #type: ignore 
            zorder: int = round((ZORDER_BASE/max(y_consumo))*ZORDER_MULTIPLIER, 0) #type: ignore
            try:
                color = next(self.iterador_colores) # itero sobre los colores
            except StopIteration:
                pass
            
            bars = ax.bar(x_cabecera, y_consumo, label=repuesto, color=color, zorder=zorder) # type: ignore
            
            ax.bar_label(bars, fontsize=15) # type: ignore
        
        # --- Configuración --- #
        ax.legend(loc="upper right", fontsize=18) # type: ignore
        ax.tick_params("x", labelsize=11.5/self.divisor) # type: ignore
        ax.tick_params("y", labelsize=15) # type: ignore

        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=40, y=0.93)
        fig.subplots_adjust(wspace=0.10, hspace=0.3)


    def create_unstacked_barplot(self, lista_indice) -> None:
        df_indices_consumo: Union[pd.DataFrame, str] = lista_indice[0]
        iterador_repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique())) # type: ignore

        fig, axs = plt.subplots(self.n_rows, self.n_cols, figsize=(PlotConfig.figure_width, PlotConfig.figure_height), squeeze=False)
        
        for i in range(axs.shape[0]):
            for j in range(axs.shape[1]):
                try:
                    rep = next(iterador_repuestos)
                    color = next(self.iterador_colores)
                except StopIteration:
                    pass
                
                rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                x_cabecera: pd.DataFrame = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                y_consumo: pd.DataFrame = df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                
                bars = axs[i,j].bar(x_cabecera, y_consumo, color=color) # type: ignore
                axs[i,j].bar_label(bars, fontsize=17)

                media_con_cero = y_consumo.mean()
                # media_con_cero = IndexUtils._calculate_average(y_consumo.tolist(), with_zero=True)
                axs[i,j].axhline(y=media_con_cero, linestyle="--", color="#618B4A")
                axs[i,j].text(x=1.01, y=media_con_cero, s=f"{media_con_cero}", color="black", va="center", 
                                transform=axs[i,j].get_yaxis_transform(), fontsize=PlotConfig.font_size*2)

                media_sin_cero = y_consumo.replace(0, np.nan).mean()
                # media_sin_cero = IndexUtils._calculate_average(y_consumo.tolist(), with_zero=False)
                axs[i,j].axhline(y=media_sin_cero, linestyle="--", color="#922D50")
                axs[i,j].text(x=1.01, y=media_sin_cero, s=f"{media_sin_cero}", color="black", va="center", 
                                transform=axs[i,j].get_yaxis_transform(), fontsize=PlotConfig.font_size*2)

                axs[i,j].legend(["Media con cero", "Media sin cero"], fontsize=PlotConfig.font_size, loc=1)
                axs[i,j].axhline(0, color="black")
                axs[i,j].set_title(rep, fontsize=25)
                axs[i,j].set_ylabel("Consumo", fontsize=20, labelpad=20)

                axs[i,j].tick_params("x", labelsize=PlotConfig.font_size)
                axs[i,j].tick_params("y", labelsize=PlotConfig.font_size*2)
                
        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=40, y=0.93)
        fig.subplots_adjust(wspace=0.10, hspace=0.3)