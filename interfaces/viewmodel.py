from abc import ABC, abstractmethod

import pandas as pd


class ViewModel(ABC):
    @abstractmethod
    def save_df(self, df) -> None:
        pass

    @abstractmethod
    def get_df(self) -> pd.DataFrame:
        pass