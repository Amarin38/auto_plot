import pandas as pd
import matplotlib.pyplot as plt

from numpy import ndarray
from typing import List, Dict, Union

from src.config.constants import COLORES, MAIN_PATH
from src.services import IndiceUtils, IndicePorMotor, IndicePorCoche
from src.services import ArreglarListadoExistencias, UpdateListadoExistencias, DeleteListadoExistencias 

class AutoIndicePlot:
    def __init__(self, nombre_archivo_nuevo: str, carpeta_datos: str, filas: int, columnas: int, 
                 tamaño_letra: int = 15, ancho: int = 60, largo: int = 60) -> None:
        self.nombre_archivo = nombre_archivo_nuevo
        self.carpeta_datos = carpeta_datos
        self.x1 = filas
        self.x2 = columnas

        self._arreglar = ArreglarListadoExistencias(self.nombre_archivo, self.carpeta_datos)
        self._update = UpdateListadoExistencias(self.nombre_archivo, self.carpeta_datos)
        self._delete = DeleteListadoExistencias(self.nombre_archivo)

        self.divisor = 0.3*self.x2
        self.tamaño_letra = tamaño_letra
        self.ancho = ancho
        self.largo = largo


    def graficar(self, stacked_barplot: bool, con_motor: bool) -> None:
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
        
        self._arreglar.arreglar_listado()
        
        if con_motor:
            df_rows = self._update.update_rows_by_dict(self.nombre_archivo, "motores")
            df_rows.to_excel(f"{MAIN_PATH}/out/{self.nombre_archivo}-S.xlsx")
            lista_indice: List[Union[pd.DataFrame, str]] = IndicePorMotor(self.nombre_archivo).calcular() # calculo el indice por motores
        else:
            lista_indice: List[Union[pd.DataFrame, str]] = IndicePorCoche(self.nombre_archivo).calcular() # calculo el indice por coche
        
        df_indices_consumo: Union[pd.DataFrame, str] = lista_indice[0]

        # ---------------------------- GRAFICO ---------------------------- #
        iterador_repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique())) # type: ignore
        iterador_colores = iter(COLORES)
        
        if stacked_barplot:
            fig, ax = plt.subplots(figsize=(self.ancho, self.largo), squeeze=False)
            
            y_dict_consumo: Dict[str, int] = {}
            
            for rep in iterador_repuestos:
                rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                x_cabecera: List[str] = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                y_dict_consumo.update({
                    rep:df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    })

            for repuesto, y_consumo in y_dict_consumo.items():  # type: ignore
                zorder: int = round((100/max(y_consumo))*10, 0) # type: ignore
            
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
            fig, axs = plt.subplots(self.x1, self.x2, figsize=(self.ancho, self.largo), squeeze=False)
            
            for i in range(axs.shape[0]):
                for j in range(axs.shape[1]):
                    try:
                        rep = next(iterador_repuestos)
                        color = next(iterador_colores)
                    except StopIteration:
                        rep = ""
                    
                    rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                    x_cabecera: ndarray = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                    y_consumo: ndarray = df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    
                    bars = axs[i,j].bar(x_cabecera, y_consumo, color=color) # type: ignore
                    axs[i,j].bar_label(bars, fontsize=17)

                    media_con_cero = IndiceUtils._media_consumo(y_consumo.tolist(), con_cero=True)
                    axs[i,j].axhline(y=media_con_cero, linestyle="--", color="#618B4A")
                    axs[i,j].text(x=1.01, y=media_con_cero, s=f"{media_con_cero}", color="black", va="center", transform=axs[i,j].get_yaxis_transform(), fontsize=self.tamaño_letra*2)

                    media_sin_cero = IndiceUtils._media_consumo(y_consumo.tolist(), con_cero=False)
                    axs[i,j].axhline(y=media_sin_cero, linestyle="--", color="#922D50")
                    axs[i,j].text(x=1.01, y=media_sin_cero, s=f"{media_sin_cero}", color="black", va="center", transform=axs[i,j].get_yaxis_transform(), fontsize=self.tamaño_letra*2)

                    axs[i,j].legend(["Media con cero","Media sin cero"], fontsize=self.tamaño_letra, loc=1)
                    axs[i,j].axhline(0, color="black")
                    axs[i,j].set_title(rep, fontsize=25)
                    axs[i,j].set_ylabel("Consumo", fontsize=20, labelpad=20)

                    axs[i,j].tick_params("x", labelsize=self.tamaño_letra)
                    axs[i,j].tick_params("y", labelsize=self.tamaño_letra*2)

        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=40, y=0.93)
        fig.subplots_adjust(wspace=0.10, hspace=0.3)
