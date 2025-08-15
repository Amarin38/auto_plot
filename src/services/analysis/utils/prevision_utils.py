import pandas as pd

class PrevisionUtils:
    @staticmethod
    def _calcular_fecha_tendencia(meses_en_adelante: int) -> pd.PeriodIndex:
        fecha_actual: pd.Timestamp = pd.Timestamp(pd.to_datetime('today').strftime("%Y-%m"))

        dias_en_adelante: int = 30 * (meses_en_adelante + 1)
        fecha_inicio: pd.Timestamp = fecha_actual + pd.Timedelta(days=1)
        fecha_final: pd.Timestamp = fecha_actual + pd.Timedelta(days=dias_en_adelante)

        return pd.date_range(fecha_inicio, fecha_final, freq="ME").to_period("M")


    @staticmethod
    def _fecha_completa_a(tipo: str, fecha_completa: str) -> int:
        fecha: pd.Timestamp = pd.to_datetime(fecha_completa, format="%Y-%m")
        
        if tipo == "año":
            return fecha.year
        elif tipo == "mes":
            return fecha.month
        else:
            return fecha.day