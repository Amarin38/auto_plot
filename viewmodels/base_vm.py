from datetime import date
import streamlit as st
from typing import List, TypeVar, Generic, Type, Dict, Any, Callable

import pandas as pd

from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


TEntity = TypeVar("TEntity")


class BaseVM(Generic[TEntity]):
    def __init__(self, entity_cls: Type[TEntity], repository_name: str, columns_df: List[str],
                       uow_constructor: Callable[[], SQLAlchemyUnitOfWork] = SQLAlchemyUnitOfWork) -> None:
        self.entity_cls         = entity_cls
        self.repository_name    = repository_name
        self.columns_df         = columns_df
        self.uow                = uow_constructor


    # ------- entidades -> DataFrame -------
    def get_data(self, entities) -> pd.DataFrame:
        if not entities:
            return pd.DataFrame(columns=self.columns_df)
        return pd.DataFrame([
            {column: getattr(entity, column) for column in self.columns_df}
            for entity in entities
        ])


    def get_df(self) -> pd.DataFrame:
        with self.uow() as uow:
            entities = getattr(uow, self.repository_name).get_all() # obtengo los datos de la entidad
        return self.get_data(entities) if entities else pd.DataFrame()


    def get_entity(self) -> List[TEntity]:
        with self.uow() as uow:
            return getattr(uow, self.repository_name).get_all()


    def get_df_by_filters(self, columns_filters: Dict[str, Any]) -> pd.DataFrame:
        with self.uow() as uow:
            entities = getattr(uow, self.repository_name).get_by_n_columns(columns_filters)

        return self.get_data(entities) if entities else pd.DataFrame()


    def get_entity_by_filters(self, columns_filters: Dict[str, Any]) -> List[TEntity]:
        with self.uow() as uow:
            return getattr(uow, self.repository_name).get_by_n_columns(columns_filters)


    def get_min_date(self, date_column: str) -> date:
        with self.uow() as uow:
            fecha = getattr(uow, self.repository_name).get_min_date(date_column)
        return fecha


    def get_max_date(self, date_column: str) -> date:
        with self.uow() as uow:
            fecha = getattr(uow, self.repository_name).get_max_date(date_column)
        return fecha


    def get_df_between_dates(self, date_column: str, start_date: date, end_date: date) -> pd.DataFrame:
        with self.uow() as uow:
            return getattr(uow, self.repository_name).get_between_dates(date_column, start_date, end_date)


    def get_distinct(self, column: str) -> pd.Series:
        with self.uow() as uow:
            return getattr(uow, self.repository_name).get_distinct_series(column)


    # ------- DataFrame -> entidades -------
    def _row_to_entity(self, row: dict, **overrides) -> TEntity:
        data = {**row, **overrides}
        return self.entity_cls(**data)

    def save(self, entity) -> None:
        if isinstance(entity, pd.DataFrame):
            entity = [self._row_to_entity(record, id=None) for record in entity.to_dict("records")]

        with self.uow() as uow:
            getattr(uow, self.repository_name).insert_many(entity)


    # DELETE
    def delete_all(self) -> None:
        with self.uow() as uow:
            getattr(uow, self.repository_name).delete()