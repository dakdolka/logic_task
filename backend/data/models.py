from data.database import Base, str_256
from sqlalchemy import Boolean, Column, Table, Integer, String, MetaData, ForeignKey, and_, func, JSON, ARRAY, UniqueConstraint, Date, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
import enum, datetime
from typing import Annotated, Optional 

class pack(enum.Enum):
    yes = 'yes'
    no = 'no'
    

class Info(Base):
    __tablename__ = "info"
    id: Mapped[str_256] = mapped_column(primary_key=True)
    name: Mapped[str_256]
    h: Mapped[Optional[int]] = mapped_column(default=None)
    w: Mapped[Optional[int]] = mapped_column(default=None)
    l: Mapped[Optional[int]] = mapped_column(default=None)
    is_packed: Mapped[pack]
    


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    

class OrdderConstructor(Base):
    __tablename__ = "order_constructor"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    info_id: Mapped[str_256] = mapped_column(ForeignKey("info.id"), primary_key=True)
    amount: Mapped[int]
    price: Mapped[int]
    

    

    