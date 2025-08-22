from dataclasses import dataclass

@dataclass
class TextColors():
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    MAGENTA = '\033[35m' 
    
    RESET = '\033[0m'