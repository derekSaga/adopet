from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedClassProtocol
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    def get_filter_by_constraints_from_table_model(
        cls, table_model: MappedClassProtocol, instance_filter: Base
    ):
        inst = inspect(table_model)
        filters = [
            (getattr(table_model, c_attr.key) == getattr(instance_filter, c_attr.key))
            for c_attr in inst.mapper.column_attrs
            if c_attr.class_attribute.unique
        ]
        return filters
