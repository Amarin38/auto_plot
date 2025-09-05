from dataclasses import dataclass

@dataclass
class TextColors():
    T_RED = '\033[91m'
    T_LIGHT_RED = '\033[31m'
    T_GREEN = '\033[92m'
    T_LIGHT_GREEN = '\033[32m'
    T_YELLOW = '\033[33m'
    T_BLUE = '\033[94m'
    T_PURPLE = '\033[95m'
    T_CYAN = '\033[96m'
    T_WHITE = '\033[97m'
    T_BLACK = '\033[90m'
    T_MAGENTA = '\033[35m' 
    T_GRAY = '\033[90m'
    T_ORANGE = '\033[38;5;208m'
    T_FUCHSIA = '\033[38;5;170m'
    
    B_RED = '\033[41m'
    B_ORANGE = '\033[48;5;208m'

    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    DIMM = '\033[22m'

    RESET = '\033[0m'


@dataclass
class PlotConfig:
    FIG_WIDTH: int = 50
    FIG_HEIGHT: int = 30

    TEXT_SIZE: int = 25
    SUPTITLE_SIZE: int = 30
    PLOT_TITLE_SIZE: int = 25
    LEGEND_SIZE: int = 20
    LABEL_SIZE: int = 30
    X_TICK_SIZE: float = 18
    Y_TICK_SIZE: int = 15
    BAR_SIZE: int = 25

    TITLE_POS: float = 0.93
    WSPACE: float = 0.1
    HSPACE: float = 0.3
    DIV_FACTOR: float = 0.3
    LABEL_PAD: int = 20
    