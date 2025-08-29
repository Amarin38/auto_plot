from typing import List
from config.dataclasses import PlotConfig


class PlotUtils:
    @staticmethod
    def _auto_annotate_on_line(x_data: List[str], y_data: List[str], axs, color: str, divisor: float) -> None:
        """
            ### Returns an axs.annotate object with the data and color entered
            ### displayed above the offset points.\n
            #### Args:\n
                x_data (List[str]) -> Data from the x axis\n
                y_data (List[str]) -> Data from the y axis\n
                axs (plt.subplots) -> The ax selected for annotation\n
                color (str) -> The color used in the line\n
                divisor (float) -> Number to divide the size number on the line
            #### Returns:\n
                axs.annotate 
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


    @staticmethod
    def _auto_reshape_2D(axs, x1: int, x2: int) -> None:
        """
        Automatically reshapes the plot if its 1D.
        
        if axs.ndim == 1:
            axs = _auto_reshape_2D(axs, x1, x2)

        """
        if x1 == 1 and x2 != 1:
            axs = axs.reshape(-1, x2)
        elif x1 != 1 and x2 == 1:
            axs =  axs.reshape(x1, -1)
        else:
            axs =  axs.reshape(-1, -1)
        return axs


    @staticmethod
    def _auto_median_line(ax, median_data: float, additional_text = "") -> None:
        """Creates a straight line with the median next to it"""
        
        ax.axhline(y=median_data, linestyle="--", color="#922D50")
        ax.text(x=1.01, 
                y=median_data, 
                s=f"{median_data}{additional_text}", 
                color="black", 
                va="center", 
                transform=ax.get_yaxis_transform(), 
                fontsize=PlotConfig.text_font_size)
    
