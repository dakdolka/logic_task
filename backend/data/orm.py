from fastapi import HTTPException
from sqlalchemy import text, insert, select, func, cast, Integer, and_, update
# from db.models import metadata_obj
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from data.database import Base, async_engine, async_session_factory
from data.models import Info, OrdderConstructor, Order
import pandas as pd


class Orm:
    @staticmethod
    async def create_all():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print('tables created')
            
            async_engine.echo = True
    
    @staticmethod
    async def insert_or_upd_info(info):
        async with async_session_factory() as session:
            print(info.columns)
            info = info[['Наименование', 'Артикул', 'Упаковка высота (мм)', "Упаковка длина (см)", "Упаковка ширина (см)", "УПАКОВКА FBO (Общие)" ]]
            data = info.values.tolist()
            for i in range(len(data)):
                data[i] = {
                    'id': data[i][1],
                    'name': data[i][0],
                    'h': data[i][2] if not pd.isna(data[i][2]) else None,
                    'w': data[i][4] if not pd.isna(data[i][4]) else None,
                    'l': data[i][3] if not pd.isna(data[i][3]) else None,
                    'is_packed': data[i][5]
                }
            temp_inf = await session.execute(select(Info.id))
            temp_inf = temp_inf.scalars().all()
            for row in data:
                if row['id'] in temp_inf:
                    await session.execute(update(Info).where(Info.id == row['id']).values(row))
                else:
                    await session.execute(insert(Info).values(row))
            await session.commit()
            
    @staticmethod
    async def insert_order(order):
        async with async_session_factory() as session:
            order = order[['Артикул', 'Количество', 'Сумма с НДС']]
            order_id = await session.execute(func.count(Order.id))
            order_id = order_id.scalar() + 1
            await session.execute(insert(Order).values({'id': order_id}))
            await session.flush()
            data = order.values.tolist()
            for i in range(len(data)):
                data[i] = {
                    'order_id': order_id,
                    'info_id': data[i][0],
                    'amount': data[i][1],
                    'price': data[i][2]
            } 
            temp_inf = await session.execute(select(Info.id))
            temp_inf = temp_inf.scalars().all()
            print(temp_inf)
            for row in data:
                print(row)
                if row['info_id'] in temp_inf:
                    await session.execute(insert(OrdderConstructor).values(row))
            await session.commit()
            
            