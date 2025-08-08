import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

from pathlib import Path
from numpy import ndarray
from typing import List, Dict, Union

try:
    from plot_backend.prevision_compra import PrevisionCompra
    from plot_backend.indice_consumo import IndiceConsumo
    from plot_backend.arreglar_listado_existencias import ArreglarListadoExistencias
    from plot_backend.utils_listado_existencias import UtilsListadoExistencias
except ModuleNotFoundError:
    from prevision_compra import PrevisionCompra
    from indice_consumo import IndiceConsumo
    from arreglar_listado_existencias import ArreglarListadoExistencias
    from utils_listado_existencias import UtilsListadoExistencias


class Autografico:
    def __init__(self, nombre_archivo_nuevo: str, carpeta_datos: str, filas: int, columnas: int, 
                 tamaño_letra: float, tamaño_grafico: int = 60, meses_en_adelante: int = 6):
        self.nombre_archivo = nombre_archivo_nuevo
        self.meses_en_adelante = meses_en_adelante
        self.x1 = filas
        self.x2 = columnas
        self._main_path = Path.cwd()

        self.arreglar = ArreglarListadoExistencias(self.nombre_archivo, carpeta_datos)
        self.utils = UtilsListadoExistencias(f"{self.nombre_archivo}-S")
        self.indice = IndiceConsumo(self.nombre_archivo)

        self.divisor = 0.3*self.x2
        self.tamaño_letra = tamaño_letra
        self.tamaño_grafico = tamaño_grafico
        self.colores = iter(("#FFC300", "#FF5733", "#C70039", "#900C3F", "#5C6D70", 
                             "#2C2C54", "#5FAD56", "#F2C14E", "#F78154", "#4D9078",
                             "#4A1942", "#823329", "#3F7CAC", "#899878", "#5497A7", 
                             "#883677", "#3A7D44", "#254D32", "#F7CE5B", "#F7B05B"))


    # ---- PLOTS ---- #
    def prevision_plot(self, con_cero: bool) -> None:
        prevision = PrevisionCompra(self.nombre_archivo, con_cero, self.meses_en_adelante)

        try:
            self.arreglar.append_df()
            self.arreglar.basic_filter("salidas")
        except (pd.errors.InvalidIndexError, AttributeError, KeyError) as e:
            print(f"Error --> {e}")
            pass
        finally:
            prevision.calcular_prevision_compra()

        # ------------- Graficos ---------------
        fig, axs = plt.subplots(self.x1, self.x2, figsize=(40,20), squeeze=False)
        fig.subplots_adjust(wspace=0.10, hspace=0.15)


        # if axs.ndim == 1:
        #     axs = auto_reshape_2D(axs, x1, x2)

        if con_cero:
            df_tendencia = pd.read_excel(f"{self._main_path}/excel/tendencia-ConCero.xlsx")
            df_data = pd.read_excel(f"{self._main_path}/excel/data-ConCero.xlsx")
            fig.suptitle(f"Prevision de compras con cero a {self.meses_en_adelante} meses", fontsize=30, y=0.94)
        else:
            df_tendencia = pd.read_excel(f"{self._main_path}/excel/tendencia-SinCero.xlsx")
            df_data = pd.read_excel(f"{self._main_path}/excel/data-SinCero.xlsx")
            fig.suptitle(f"Prevision de compras sin cero a {self.meses_en_adelante} meses", fontsize=30, y=0.94)

        repuestos = iter(tuple(df_tendencia["Repuesto"].unique()))

        # ------------------------ Cargo los graficos recursivamente ---------------------------
        try:
            for i in range(axs.shape[0]): 
                for j in range(axs.shape[1]):
                    rep = next(repuestos) # itero en los repuestos
                    
                    x_data = df_data.loc[df_data["Repuesto"] == rep, "TotalMes"]
                    y_data = df_data.loc[df_data["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
                    y_data: pd.DatetimeIndex = pd.to_datetime(y_data, format="%Y-%m")

                    if con_cero:
                        x_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "TendenciaEstacionalConCero"]
                    else:
                        x_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "TendenciaEstacionalSinCero"]

                    y_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
                    y_tendencia: pd.DatetimeIndex = pd.to_datetime(y_tendencia, format="%Y-%m")
                    
                    axs[i,j].plot(y_data, x_data, color="#2e7d32", marker="o", linestyle="-")
                    axs[i,j].plot(y_tendencia, x_tendencia, color="#c62828", marker="s", linestyle="--")
                    
                    auto_annotate_on_line(x_data, y_data, axs[i,j], '#2e7d32', self.divisor) # type: ignore
                    auto_annotate_on_line(x_tendencia, y_tendencia, axs[i,j], '#c62828', self.divisor) # type: ignore
                    
                    bbox = dict(boxstyle ="round", fc ="0.8")
                    axs[i,j].legend(["Consumo temporal","Tendencia de consumo"], fontsize=20/self.divisor, loc=2)
                    axs[i,j].axhline(0, color="black")
                    axs[i,j].set_title(rep, fontsize=16)
                    axs[i,j].set_ylabel("Consumo", fontsize=20, labelpad=20)
                    axs[i,j].tick_params("x", labelsize=11.25)
                    axs[i,j].tick_params("y", labelsize=15)
                    axs[i,j].xaxis.set_major_locator(pltdates.DayLocator(interval=90))
                    axs[i,j].xaxis.set_major_formatter(pltdates.DateFormatter("%Y-%m"))
                    axs[i,j].text(0.995, 0.99, f"Tendencia total: {x_tendencia.sum()}", transform=axs[i,j].transAxes, va="top", ha="right", fontsize=18/self.divisor, bbox=bbox) # type: ignore
        except StopIteration:
            rep = ""


    # ---- BARPLOTS ---- #
    def indice_barplot(self, stacked_barplot: bool, con_motor: bool) -> None:
        """
        nombre_archivo --> str (archivo a usar)\n
        stacked_barplot --> True/False (grafico apilado)\n
        con_motor --> True/False (usar el indice en base a motores o no)\n
                    --> Si es False, por defecto usa cantidad de coches\n
        x1, x2 --> int, int (cantidad de graficos)\n
        """
        
        try:
            self.arreglar.append_df()
            self.arreglar.basic_filter("salidas")
            
            df_rows = self.utils.update_rows_by_dict(f"{self.nombre_archivo}-S", "motores", "Repuesto")
            df_rows.to_excel(f"{self._main_path}/excel/{self.nombre_archivo}-S.xlsx")

            # self.utils.delete_rows("repuesto", ["CAÑO", "BOMBA"])

        except (pd.errors.InvalidIndexError, AttributeError) as e:
            print(f"ERROR: {e}")
        except KeyError:
            print("ERROR: No existen las columnas, no se puede concatenar")    
        
        if con_motor:
            lista_indice: List[Union[pd.DataFrame, str]] = self.indice.calcular_indice_por_motores() # calculo el indice por motores
        else:
            lista_indice: List[Union[pd.DataFrame, str]] = self.indice.calcular_indice_por_coche() # calculo el indice por coche
        
        df_indices_consumo: Union[pd.DataFrame, str] = lista_indice[0]

        # ---------------------------- GRAFICO ---------------------------- #
        repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique())) # type: ignore

        if stacked_barplot:
            fig, ax = plt.subplots(figsize=(40,30), squeeze=False)
            
            y_dict_consumo: Dict[str, int] = {}
            
            for rep in repuestos:
                rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                x_cabecera: List[str] = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                y_dict_consumo.update({
                    rep:df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    })

            for repuesto, y_consumo in y_dict_consumo.items():  # type: ignore
                zorder: int = round((100/max(y_consumo))*10, 0) # type: ignore
            
                try:
                    color = next(self.colores) # itero sobre los colores
                except StopIteration:
                    pass
                
                bars = ax.bar(x_cabecera, y_consumo, label=repuesto, color=color, zorder=zorder) # type: ignore
                
                ax.bar_label(bars, fontsize=15) # type: ignore
            
            # --- Configuración --- #
            ax.legend(loc="upper right", fontsize=18) # type: ignore
            ax.tick_params("x", labelsize=11.5/self.divisor) # type: ignore
            ax.tick_params("y", labelsize=15) # type: ignore

        else:
            fig, axs = plt.subplots(self.x1, self.x2, figsize=(self.tamaño_grafico, self.tamaño_grafico), squeeze=False)#figsize=(45*self.x1,80/self.x2), squeeze=False)
            
            # if axs.ndim == 1: # Numero de dimensiones
                # axs = auto_reshape_2D(axs, x1, x2)
            
            for i in range(axs.shape[0]):
                for j in range(axs.shape[1]):
                    try:
                        rep = next(repuestos) # itero en los repuestos
                        color = next(self.colores) # itero sobre los colores
                    except StopIteration:
                        rep = ""
                    
                    rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                    x_cabecera: ndarray = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                    y_consumo: ndarray = df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    
                    bars = axs[i,j].bar(x_cabecera, y_consumo, color=color) # type: ignore
                    axs[i,j].bar_label(bars, fontsize=17)

                    media_con_cero = self.indice.media_consumo(y_consumo.tolist(), con_cero=True)
                    axs[i,j].axhline(y=media_con_cero, linestyle="--", color="#618B4A")
                    axs[i,j].text(x=1.01, y=media_con_cero, s=f"{media_con_cero}", color="black", va="center", transform=axs[i,j].get_yaxis_transform(), fontsize=self.tamaño_letra*2)

                    media_sin_cero = self.indice.media_consumo(y_consumo.tolist(), con_cero=False)
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
            
        
    # ---------------- UTILS ---------------- #
    def auto_annotate_on_line(self, x_data: List[str], y_data: List[str], axs, color: str, divisor: float) -> None:
        """
            Returns an axs.annotate object with the data and color entered
            displayed above the offset points.
        """

        for y, x in zip(y_data, x_data): # labels tendencia
                    axs.annotate(
                        f"{x:.0f}",      
                        xy=(y, x), # type: ignore
                        xytext=(0, 5),   
                        textcoords='offset points',
                        ha='center',
                        va='bottom',
                        fontsize=15/divisor,
                        color=color
                    )

    def auto_reshape_2D(self, axs, x1: int, x2: int) -> None:
        """
        Automatically reshapes the plot if its 1D.
        """
        if x1 == 1:
            axs = axs.reshape(-1, x2)
        elif x2 == 1:
            axs =  axs.reshape(x1, -1)
        else:
            axs =  axs.reshape(-1, -1)
        return axs

 

if __name__ == "__main__":
    # plot = Autografico("todas-herramientas", "todas herramientas", 2, 2)
    # plot.indice_barplot(False, False)
    # plot.prevision_plot(True)
    ...