from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, DeclarativeBase, sessionmaker
from sqlalchemy import URL, create_engine, text, String
# from sqlalchemy.ext.declarative import declarative_base
from data.config import settings
# import asyncio
from typing import Annotated

async_engine = create_async_engine( #асинхронный движок
    url=settings.db_url,
    echo=True,
    pool_size=5,
    max_overflow=10,
) 

async_session_factory = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

str_256 = Annotated[str, 256]
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)

    }
    
    repr_columns_num = 200
    repr_cols = tuple() #можно указать это как поля у отдельных классов когда делаем модельки через orm

    def __repr__(self): # переделка принта моделей в логах
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_columns_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"==== {self.__class__.__name__} {', '.join(cols)} ===="