from datetime import date
from typing import Generic, TypeVar, List, Type, Any, Dict

import pandas as pd
import streamlit as st
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from infrastructure.mapper import Mapper


TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")

class BaseRepository(Generic[TEntity, TModel]):
    entity_cls: Type[TEntity]
    model_cls: Type[TModel]

    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_one(self, entity: TEntity) -> None:
        model = Mapper.to_model(entity, self.model_cls)
        self.session.add(model)


    def insert_many(self, entities: List[TEntity]) -> None:
        models = [Mapper.to_model(entity, self.model_cls) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[TEntity]:
        models = self.session.scalars(
            select(self.model_cls)
        ).all()

        return [Mapper.to_entity(model, self.entity_cls) for model in models]


    def get_by_id(self, _id: int) -> TEntity:
        model = self.session.scalars(
            select(self.model_cls)
            .where(self.model_cls.id == _id)
        ).first()

        return Mapper.to_entity(model, self.entity_cls)


    def get_by_n_columns(self, columns_filters: Dict[str, Any]) -> List[TEntity]:
        conditions = []

        for column_name, value in columns_filters.items():
            found_column = self.col_exists(column_name)

            if value is None:
                conditions.append(found_column is None)
            elif isinstance(value, (list, tuple, set)):
                if len(value) > 0:
                    conditions.append(found_column.in_(value))
                else:
                    conditions.append(found_column is None)
            else:
                conditions.append(found_column == value)

        models = self.session.scalars(
            select(self.model_cls).where(*conditions)
        ).all()

        return [Mapper.to_entity(model, self.entity_cls) for model in models]


    def get_between_dates(self, date_column: str, start_date: date, end_date: date) -> List[TEntity]:
        column = self.col_exists(date_column)

        models = self.session.scalars(
            select(self.model_cls)
            .where(column.between(start_date, end_date))
        ).all()

        return [Mapper.to_entity(model, self.entity_cls) for model in models]


    def get_min_date(self, date_column: str) -> date:
        column = self.col_exists(date_column)

        return self.session.query(func.min(column)).scalar()


    def get_max_date(self, date_column: str) -> date:
        column = self.col_exists(date_column)

        return self.session.query(func.max(column)).scalar()


    def get_distinct_series(self, column: str) -> pd.Series:
        found_column = self.col_exists(column)

        series = self.session.scalars(
            select(found_column).distinct()
        ).all()

        return pd.Series(series)


    # Update -------------------------------------------
    def update(self, _id: int, entity: TEntity) -> None:
        old_model = self.get_model(_id)
        new_model = Mapper.to_model(entity, self.model_cls)

        for column in self.model_cls.__table__.columns.keys():
            if column != "id":
                setattr(old_model, column, getattr(new_model, column))


    def update_fields(self,_id: int, fields: dict) -> None:
        old_model = self.get_model(_id)
        for field_name, value in fields.items():
            self.col_exists(field_name)
            setattr(old_model, field_name, value)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(self.model_cls, _id)
        if row:
            self.session.delete(row)


    def delete(self) -> None:
        self.session.query(self.model_cls).delete()

    # ------------------------------------------------------------------------------------------------------------
    def col_exists(self, column: str):
        if not hasattr(self.model_cls, column):  # veo si la clase tiene la columna
            raise AttributeError(
                f"'{self.model_cls.__name__}' no tiene la columna '{column}'"
            )  # si no la tiene salta AttributeError

        return getattr(self.model_cls, column)  # Si existe la obtengo


    def get_model(self, _id: int) -> TModel:
        model = self.session.get(self.model_cls, _id)

        if model is None:
            raise ValueError(f"No existe {self.model_cls.__name__} con id={_id}")

        return model


