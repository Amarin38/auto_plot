import pandas as pd
import matplotlib.pyplot as plt

from numpy import ndarray
from typing import List, Dict, Union

from src.config.constants import COLORS, MAIN_PATH
from src.services import RateUtils, RateByMotor, RateByVehicle
from src.services import InventoryDataCleaner, InventoryUpdate, InventoryDelete 


# TODO modificar para simplificar más
class AutoRatePlotter:
    def __init__(self, file: str, dir: str, rows: int, columns: int, 
                 font_size: int = 15, width: int = 70, height: int = 70) -> None:
        self.file = file
        self.dir = dir
        self.x1 = rows
        self.x2 = columns

        self._arreglar = InventoryDataCleaner(self.file, self.dir)
        self._update = InventoryUpdate(self.file, self.dir)
        self._delete = InventoryDelete(self.file)

        self.divisor = 0.3*self.x2
        self.font_size = font_size
        self.width = width
        self.height = height


    def plot(self, stacked_barplot: bool, con_motor: bool) -> None:
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
        
        self._arreglar.run_all()
        
        if con_motor:
            df_rows = self._update.update_rows_by_dict(self.file, "motores")
            df_rows.to_excel(f"{MAIN_PATH}/out/{self.file}-S.xlsx")
            lista_indice: List[Union[pd.DataFrame, str]] = RateByMotor(self.file, self.dir).calcular() # calculo el indice por motores
        else:
            lista_indice: List[Union[pd.DataFrame, str]] = RateByVehicle(self.file, self.dir).calcular() # calculo el indice por coche
        
        df_indices_consumo: Union[pd.DataFrame, str] = lista_indice[0]

        # ---------------------------- GRAFICO ---------------------------- #
        iterador_repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique())) # type: ignore
        iterador_colores = iter(COLORS)
        
        if stacked_barplot:
            fig, ax = plt.subplots(figsize=(self.width, self.height), squeeze=False)
            
            y_dict_consumo: Dict[str, ndarray] = {}
            
            for rep in iterador_repuestos:
                rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                x_cabecera: List[str] = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                y_dict_consumo.update({
                    rep:df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    })

            for repuesto, y_consumo in y_dict_consumo.items():  
                zorder: int = round((100/max(y_consumo))*10, 0) 
            
                try:
                    color = next(iterador_colores) # itero sobre los colores
                except StopIteration:
                    pass
                
                bars = ax.bar(x_cabecera, y_consumo, label=repuesto, color=color, zorder=zorder) # type: ignore
                
                ax.bar_label(bars, fontsize=15) # type: ignore
            
            # --- Configuración --- #
            ax.legend(loc="upper right", fontsize=18) # type: ignore
            ax.tick_params("x", labelsize=11.5/self.divisor) # type: ignore
            ax.tick_params("y", labelsize=15) # type: ignore

        else:
            fig, axs = plt.subplots(self.x1, self.x2, figsize=(self.width, self.height), squeeze=False)
            
            for i in range(axs.shape[0]):
                for j in range(axs.shape[1]):
                    try:
                        rep = next(iterador_repuestos)
                        color = next(iterador_colores)
                    except StopIteration:
                        pass
                    
                    rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                    x_cabecera: ndarray = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                    y_consumo: ndarray = df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    
                    bars = axs[i,j].bar(x_cabecera, y_consumo, color=color) # type: ignore
                    axs[i,j].bar_label(bars, fontsize=17)

                    media_con_cero = RateUtils._calculate_average(y_consumo.tolist(), con_cero=True)
                    axs[i,j].axhline(y=media_con_cero, linestyle="--", color="#618B4A")
                    axs[i,j].text(x=1.01, y=media_con_cero, s=f"{media_con_cero}", color="black", va="center", 
                                  transform=axs[i,j].get_yaxis_transform(), fontsize=self.font_size*2)

                    media_sin_cero = RateUtils._calculate_average(y_consumo.tolist(), con_cero=False)
                    axs[i,j].axhline(y=media_sin_cero, linestyle="--", color="#922D50")
                    axs[i,j].text(x=1.01, y=media_sin_cero, s=f"{media_sin_cero}", color="black", va="center", 
                                  transform=axs[i,j].get_yaxis_transform(), fontsize=self.font_size*2)

                    axs[i,j].legend(["Media con cero","Media sin cero"], fontsize=self.font_size, loc=1)
                    axs[i,j].axhline(0, color="black")
                    axs[i,j].set_title(rep, fontsize=25)
                    axs[i,j].set_ylabel("Consumo", fontsize=20, labelpad=20)

                    axs[i,j].tick_params("x", labelsize=self.font_size)
                    axs[i,j].tick_params("y", labelsize=self.font_size*2)

        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=40, y=0.93)
        fig.subplots_adjust(wspace=0.10, hspace=0.3)
