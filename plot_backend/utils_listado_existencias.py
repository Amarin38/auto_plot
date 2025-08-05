import json
import pandas as pd
from typing import Dict, Union, List, Optional



class UtilsListadoExistencias:
    def __init__(self, file: str):
        self.file = file


    # --- UPDATE --- #
    def update_single_column(self, xlsx_file: str, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        df: pd.DataFrame = self.check_filetype(xlsx_file)

        df[column] = df[column].replace(old_name, new_name)
        
        df.to_excel(f"excel/{self.file}.xlsx")
        return df


    def update_column_by_dict(self, xlsx_file: Union[str, pd.DataFrame], archivo_json: str) -> pd.DataFrame:
        with open(f"json/{archivo_json}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file) 

        df: pd.DataFrame = self.check_filetype(xlsx_file)
        return df.rename(columns=data)


    def update_rows_by_dict(self, xlsx_file: Union[str, pd.DataFrame], json_file: str, column: str ) -> pd.DataFrame:
        with open(f"json/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file)
        
        df: pd.DataFrame = self.check_filetype(xlsx_file)
        df[column] = df[column].replace(data)
        print(df)

        return df


    # --- DELETE --- #
    def delete_unnamed_cols(self):
        df: pd.DataFrame = self.check_filetype(self.file)
        df = df.loc[:, ~df.columns.str.contains("Unnamed")]
        df = df.loc[:, ~df.columns.str.contains("Columna")]

        df.to_excel(f"excel/{self.file}.xlsx")


    def delete_rows(self, delete_type: str, delete_by: List[str]) -> pd.DataFrame:
        """
        Deletes the row by entered string.\n
        Delete types: repuesto, fechacompleta.\n
        Delete by: List[str]
        """
        
        df: pd.DataFrame = self.check_filetype(self.file)

        match delete_type:
            case "repuesto":
                for delete in delete_by:
                    df = df.loc[-df.Repuesto.str.contains(delete, na=False)] # guardo indices de los elementos para borrar
            case "fechacompleta":
                for delete in delete_by:
                    df = df.loc[-df.FechaCompleta.str.contains(delete, na=False)]
            case "interno":
                for delete in delete_by:
                    df = df.loc[-df.Interno.str.contains(delete, na=False)]
            case _:
                return  pd.DataFrame()
        
        df.to_excel(f"excel/{self.file}.xlsx")
        return df


    def separar_internos_cabecera(self) -> pd.DataFrame:
        df: pd.DataFrame = self.check_filetype(self.file)
        cabeceras = df["Cabecera"].unique()

        list_internos: List[Dict[str, int]] = []

        for cab in cabeceras:
            internos_cabecera: List[int] = df.loc[df["Cabecera"] == cab, "Interno"].dropna().unique().tolist() # type: ignore

            for inter in internos_cabecera:
                list_internos.append({
                    "Cabecera":cab,
                    "Interno":inter
                })

        df_internos: pd.DataFrame = pd.DataFrame(list_internos)
        df_internos.to_excel("internos_cabecera.xlsx")
        return df
    

    # --- UTILS --- #
    def check_filetype(self, file: Union[str, pd.DataFrame]):
        if isinstance(file, str):
            df: pd.DataFrame = pd.read_excel(f"excel/{file}.xlsx", engine="calamine")
        else:
            df: pd.DataFrame = pd.DataFrame(file)
        
        return df
