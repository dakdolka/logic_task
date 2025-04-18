from data.database import Base, str_256
from sqlalchemy import Boolean, Column, Table, Integer, String, MetaData, ForeignKey, and_, func, JSON, ARRAY, UniqueConstraint, Date, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
import enum, datetime
from typing import Annotated, Optional 

class pack(enum.Enum):
    yes = 'Да'
    no = 'Нет'
    

class Info(Base):
    __tablename__ = "info"
    id: Mapped[str_256] = mapped_column(primary_key=True)
    name: Mapped[str_256]
    h: Mapped[Optional[float]] = mapped_column(default=None)
    w: Mapped[Optional[float]] = mapped_column(default=None)
    l: Mapped[Optional[float]] = mapped_column(default=None)
    is_packed: Mapped[pack]
    orders: Mapped[list['OrdderConstructor']] = relationship(back_populates="info")
    


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_constructor: Mapped[list['OrdderConstructor']] = relationship(back_populates="order")
    

class OrdderConstructor(Base):
    __tablename__ = "order_constructor"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    info_id: Mapped[str_256] = mapped_column(ForeignKey("info.id"), primary_key=True)
    amount: Mapped[int]
    price: Mapped[int]
    order: Mapped[Order] = relationship(back_populates="order_constructor")
    info: Mapped[Info] = relationship(back_populates="orders")
    

    

    